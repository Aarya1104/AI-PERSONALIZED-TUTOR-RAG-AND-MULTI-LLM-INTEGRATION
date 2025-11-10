import sys
# Fix SQLite version for ChromaDB
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import torch
from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict
from config import (EMBEDDING_MODEL, CHROMA_DB_DIR, DEVICE, 
                   USE_HYBRID_SEARCH, HYBRID_ALPHA, USE_RERANKING, RERANK_TOP_K)
from rank_bm25 import BM25Okapi
import numpy as np

try:
    from flashrank import Ranker, RerankRequest
    FLASHRANK_AVAILABLE = True
except ImportError:
    FLASHRANK_AVAILABLE = False
    print("FlashRank not available. Install with: pip install flashrank", end="\n")

class VectorStore:
    def __init__(self):
        print("Initializing Vector Store...", end="\n")
        
        print(f"Loading embedding model: {EMBEDDING_MODEL}", end="\n")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL, device=DEVICE)
        print(f"Embedding model loaded on {DEVICE}", end="\n")
        
        self.client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
        
        try:
            self.collection = self.client.get_collection(name="documents")
            print("Loaded existing collection", end="\n")
        except:
            self.collection = self.client.create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
            print("Created new collection", end="\n")
        
        self.bm25 = None
        self.bm25_corpus = []
        self.bm25_ids = []
        
        if USE_RERANKING and FLASHRANK_AVAILABLE:
            print("Loading reranker...", end="\n")
            self.reranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")
        else:
            self.reranker = None
        
        self._rebuild_bm25_index()
        print(f"Vector store initialized. Current documents: {self.collection.count()}", end="\n")
    
    def _rebuild_bm25_index(self):
        """Rebuild BM25 index from existing documents"""
        if not USE_HYBRID_SEARCH:
            return
        
        count = self.collection.count()
        if count > 0:
            print(f"Rebuilding BM25 index for {count} documents...", end="\n")
            results = self.collection.get()
            self.bm25_corpus = [doc.lower().split() for doc in results['documents']]
            self.bm25_ids = results['ids']
            self.bm25 = BM25Okapi(self.bm25_corpus)
            print("BM25 index rebuilt", end="\n")
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts"""
        print(f"Generating embeddings for {len(texts)} texts...", end="\n")
        embeddings = self.embedding_model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        print("Embeddings generated successfully", end="\n")
        return embeddings.tolist()
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """Add documents to vector store"""
        if not documents:
            print("No documents to add", end="\n")
            return
        
        print(f"Adding {len(documents)} documents to vector store...", end="\n")
        
        texts = [doc['text'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        embeddings = self.embed_texts(texts)
        
        existing_count = self.collection.count()
        ids = [f"doc_{existing_count + i}" for i in range(len(documents))]
        
        self.collection.add(
            embeddings=embeddings,  # type: ignore
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        if USE_HYBRID_SEARCH:
            for text, doc_id in zip(texts, ids):
                self.bm25_corpus.append(text.lower().split())
                self.bm25_ids.append(doc_id)
            self.bm25 = BM25Okapi(self.bm25_corpus)
        
        print(f"Successfully added {len(documents)} documents. Total: {self.collection.count()}", end="\n")
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """Search vector store"""
        if USE_HYBRID_SEARCH and self.bm25:
            return self._hybrid_query(query_text, n_results)
        else:
            return self._semantic_query(query_text, n_results)
    
    def _semantic_query(self, query_text: str, n_results: int = 5) -> Dict:
        """Pure semantic search"""
        print(f"Semantic querying: '{query_text}'", end="\n")
        
        query_embedding = self.embed_texts([query_text])[0]
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        print(f"Found {len(results['documents'][0])} results", end="\n")
        
        return {
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0]
        }
    
    def _hybrid_query(self, query_text: str, n_results: int = 5) -> Dict:
        """Hybrid semantic + keyword search"""
        print(f"Hybrid querying: '{query_text}'", end="\n")
        
        retrieve_count = RERANK_TOP_K if USE_RERANKING else n_results
        
        query_embedding = self.embed_texts([query_text])[0]
        semantic_results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=retrieve_count
        )
        
        tokenized_query = query_text.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        
        bm25_top_indices = np.argsort(bm25_scores)[::-1][:retrieve_count]
        
        combined_results = {}
        
        for i, doc_id in enumerate(semantic_results['ids'][0]):
            semantic_score = 1 - semantic_results['distances'][0][i]
            combined_results[doc_id] = {
                'semantic_score': semantic_score,
                'bm25_score': 0,
                'document': semantic_results['documents'][0][i],
                'metadata': semantic_results['metadatas'][0][i]
            }
        
        for idx in bm25_top_indices:
            doc_id = self.bm25_ids[idx]
            bm25_score = bm25_scores[idx]
            
            if doc_id in combined_results:
                combined_results[doc_id]['bm25_score'] = bm25_score
            else:
                doc_data = self.collection.get(ids=[doc_id])
                if doc_data['documents']:
                    combined_results[doc_id] = {
                        'semantic_score': 0,
                        'bm25_score': bm25_score,
                        'document': doc_data['documents'][0],
                        'metadata': doc_data['metadatas'][0]
                    }
        
        for doc_id in combined_results:
            semantic = combined_results[doc_id]['semantic_score']
            bm25 = combined_results[doc_id]['bm25_score']
            max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1
            bm25_norm = bm25 / max_bm25
            
            combined_results[doc_id]['combined_score'] = (
                HYBRID_ALPHA * semantic + (1 - HYBRID_ALPHA) * bm25_norm
            )
        
        sorted_results = sorted(
            combined_results.items(),
            key=lambda x: x[1]['combined_score'],
            reverse=True
        )[:retrieve_count]
        
        if USE_RERANKING and self.reranker:
            print("Reranking results...", end="\n")
            passages = [{"text": item[1]['document'], "id": item[0]} for item in sorted_results]
            
            rerank_request = RerankRequest(query=query_text, passages=passages)
            reranked = self.reranker.rerank(rerank_request)
            
            sorted_results = [(p['id'], combined_results[p['id']]) for p in reranked[:n_results]]
        else:
            sorted_results = sorted_results[:n_results]
        
        documents = [item[1]['document'] for item in sorted_results]
        metadatas = [item[1]['metadata'] for item in sorted_results]
        distances = [1 - item[1]['combined_score'] for item in sorted_results]
        
        print(f"Found {len(documents)} results (hybrid search)", end="\n")
        
        return {
            'documents': documents,
            'metadatas': metadatas,
            'distances': distances
        }
    
    def clear_collection(self):
        """Clear all documents from collection"""
        self.client.delete_collection(name="documents")
        self.collection = self.client.create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        self.bm25 = None
        self.bm25_corpus = []
        self.bm25_ids = []
        print("Collection cleared", end="\n")
    
    def get_stats(self):
        """Get collection statistics"""
        count = self.collection.count()
        return {
            'total_documents': count,
            'embedding_model': EMBEDDING_MODEL,
            'device': DEVICE,
            'hybrid_search': USE_HYBRID_SEARCH,
            'reranking': USE_RERANKING and self.reranker is not None
        }
