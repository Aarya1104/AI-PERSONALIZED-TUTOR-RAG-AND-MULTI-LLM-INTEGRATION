import os
from typing import List, Dict
from pathlib import Path
import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

class DocumentLoader:
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        print("DocumentLoader initialized", end="\n")
    
    def load_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        print(f"Loading PDF: {file_path}", end="\n")
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                print(f"Total pages: {total_pages}", end="\n")
                
                for page_num, page in enumerate(pdf_reader.pages):
                    text += page.extract_text()
                    if (page_num + 1) % 10 == 0:
                        print(f"Processed {page_num + 1}/{total_pages} pages", end="\n")
                
            print(f"PDF loaded successfully. Total characters: {len(text)}", end="\n")
            return text
        except Exception as e:
            print(f"Error loading PDF: {str(e)}", end="\n")
            return ""
    
    def load_txt(self, file_path: str) -> str:
        """Load text from TXT file"""
        print(f"Loading TXT: {file_path}", end="\n")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            print(f"TXT loaded successfully. Total characters: {len(text)}", end="\n")
            return text
        except Exception as e:
            print(f"Error loading TXT: {str(e)}", end="\n")
            return ""
    
    def load_document(self, file_path: str) -> str:
        """Load document based on file extension"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self.load_pdf(file_path)
        elif file_ext == '.txt':
            return self.load_txt(file_path)
        else:
            print(f"Unsupported file type: {file_ext}", end="\n")
            return ""
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        print("Chunking text...", end="\n")
        chunks = self.text_splitter.split_text(text)
        print(f"Created {len(chunks)} chunks", end="\n")
        return chunks
    
    def process_document(self, file_path: str) -> List[Dict[str, str]]:
        """Process document and return chunks with metadata"""
        text = self.load_document(file_path)
        if not text:
            return []
        
        chunks = self.chunk_text(text)
        
        # Create documents with metadata
        documents = []
        filename = Path(file_path).name
        
        for idx, chunk in enumerate(chunks):
            documents.append({
                'text': chunk,
                'metadata': {
                    'source': filename,
                    'chunk_id': idx,
                    'total_chunks': len(chunks),
                    'type': 'text'
                }
            })
        
        print(f"Document processing complete: {len(documents)} document chunks created", end="\n")
        return documents
