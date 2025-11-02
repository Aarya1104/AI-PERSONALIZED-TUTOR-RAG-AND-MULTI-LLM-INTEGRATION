import ollama
import re
from typing import Dict, List, Tuple
from datetime import datetime
import json
from pathlib import Path
from config import CONVERSATIONS_DIR, MAX_HISTORY_LENGTH

class LLMManager:
    def __init__(self):
        print("Initializing LLM Manager...", end="\n")
        self.small_model = "phi3:mini"
        self.large_model = "mistral:7b"
        
        # Verify models are available
        self._verify_models()
        print("LLM Manager initialized successfully", end="\n")
    
    def _verify_models(self):
        """Check if models are installed"""
        try:
            models = ollama.list()
            available = [m['name'] for m in models['models']]
            
            if self.small_model not in available:
                print(f"Warning: {self.small_model} not found. Run: ollama pull {self.small_model}", end="\n")
            
            if self.large_model not in available:
                print(f"Warning: {self.large_model} not found. Run: ollama pull {self.large_model}", end="\n")
                
        except Exception as e:
            print(f"Error checking models: {str(e)}", end="\n")
    
    def classify_query_complexity(self, query: str) -> str:
        """Determine if query is simple or complex"""
        query_lower = query.lower()
        
        # Complex query indicators
        complex_indicators = [
            'explain', 'why', 'how does', 'compare', 'difference between',
            'analyze', 'evaluate', 'discuss', 'elaborate', 'in detail',
            'step by step', 'pros and cons', 'advantages', 'disadvantages'
        ]
        
        # Check for multiple questions
        question_marks = query.count('?')
        
        # Check query length
        word_count = len(query.split())
        
        # Determine complexity
        is_complex = False
        
        if any(indicator in query_lower for indicator in complex_indicators):
            is_complex = True
        
        if question_marks > 1:
            is_complex = True
        
        if word_count > 15:
            is_complex = True
        
        complexity = "complex" if is_complex else "simple"
        print(f"Query classified as: {complexity}", end="\n")
        return complexity
    
    def generate_response(self, query: str, context: str, complexity: str = None) -> str:
        """Generate response using appropriate model"""
        
        if complexity is None:
            complexity = self.classify_query_complexity(query)
        
        # Select model based on complexity
        model = self.large_model if complexity == "complex" else self.small_model
        print(f"Using model: {model}", end="\n")
        
        # Create prompt with context
        prompt = self._create_prompt(query, context)
        
        try:
            # Generate response
            print("Generating response...", end="\n")
            response = ollama.generate(
                model=model,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'num_predict': 500
                }
            )
            
            answer = response['response'].strip()
            print(f"Response generated ({len(answer)} characters)", end="\n")
            return answer
            
        except Exception as e:
            print(f"Error generating response: {str(e)}", end="\n")
            return f"Error: Could not generate response. {str(e)}"
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create prompt with RAG context"""
        prompt = f"""You are an intelligent AI tutor. Use the following context from the student's learning materials to answer their question accurately and clearly.

Context from materials:
{context}

Student Question: {query}

Instructions:
- Answer based primarily on the provided context
- If the context doesn't fully answer the question, use your knowledge but indicate this
- Provide clear, educational explanations
- Use examples when helpful
- Be concise but thorough

Answer:"""
        return prompt


class EnhancedLLMManager(LLMManager):
    def __init__(self):
        super().__init__()
        self.conversation_history = []
        self.student_level = "intermediate"
        print("Enhanced LLM Manager with tutor features initialized", end="\n")
    
    def set_student_level(self, level: str):
        """Set student proficiency level"""
        self.student_level = level
        print(f"Student level set to: {level}", end="\n")
    
    def add_to_history(self, query: str, answer: str, sources: List[str]):
        """Add interaction to conversation history"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'answer': answer,
            'sources': sources,
            'student_level': self.student_level
        })
        
        # Limit history length
        if len(self.conversation_history) > MAX_HISTORY_LENGTH:
            self.conversation_history = self.conversation_history[-MAX_HISTORY_LENGTH:]
    
    def get_conversation_context(self, num_previous: int = 3) -> str:
        """Get recent conversation for context"""
        if not self.conversation_history:
            return ""
        
        recent = self.conversation_history[-num_previous:]
        context_parts = []
        
        for i, item in enumerate(recent, 1):
            context_parts.append(f"Previous Q{i}: {item['query']}")
            context_parts.append(f"Previous A{i}: {item['answer'][:200]}...")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Enhanced educational prompt with level adaptation and conversation history"""
        
        # Get conversation context
        conv_context = self.get_conversation_context(2)
        
        # Adjust teaching style based on student level
        teaching_styles = {
            "beginner": "Use very simple language, avoid jargon, use lots of analogies and everyday examples. Break everything into tiny steps.",
            "intermediate": "Use clear explanations with some technical terms (define them). Balance theory and practice.",
            "advanced": "Use precise technical language, focus on nuances, compare approaches, discuss implications and applications."
        }
        
        style_instruction = teaching_styles.get(self.student_level, teaching_styles["intermediate"])
        
        conv_section = f"""
🔄 RECENT CONVERSATION:
{conv_context}
""" if conv_context else ""
        
        prompt = f"""You are an experienced AI tutor helping a {self.student_level}-level student learn. 

🎓 TEACHING STYLE FOR {self.student_level.upper()} STUDENT:
{style_instruction}
{conv_section}
📚 RELEVANT CONTEXT FROM MATERIALS:
{context}

❓ STUDENT QUESTION: {query}

🎯 PROVIDE AN EDUCATIONAL RESPONSE THAT:

1. **Direct Answer** (2-3 sentences):
   - Answer the question clearly and directly first

2. **Core Explanation** (Step-by-step):
   - Break down the concept into understandable parts
   - Explain WHY things work this way, not just WHAT they are
   
3. **Concrete Example**:
   - Provide a real-world analogy or example
   - Make it relatable to everyday experience

4. **Connection to Bigger Picture**:
   - How does this relate to other concepts in the materials?
   - Why is this important to understand?

5. **Learning Extension** (Optional):
   - Suggest a thought-provoking question for deeper thinking
   - Or mention a related concept worth exploring

💡 REMEMBER:
- Be encouraging and supportive
- Build on previous conversation when relevant
- If the student seems confused, simplify further
- Celebrate understanding with positive reinforcement
- If context is insufficient, acknowledge it honestly

TUTOR'S RESPONSE:"""
        
        return prompt
    
    def generate_review_questions(self, topic: str, context: str, num_questions: int = 3) -> str:
        """Generate review questions for a topic"""
        print(f"Generating {num_questions} review questions for: {topic}", end="\n")
        
        prompt = f"""Based on this learning material about {topic}:

{context}

Generate {num_questions} review questions that help students test their understanding. 

Questions should:
- Progress from basic recall to deeper understanding
- Cover key concepts from the material
- Be clear and answerable based on the context
- Vary in difficulty

Format: Just list the questions numbered 1, 2, 3, etc.

REVIEW QUESTIONS:"""

        try:
            response = ollama.generate(
                model=self.small_model,
                prompt=prompt,
                options={'temperature': 0.8, 'num_predict': 300}
            )
            return response['response'].strip()
        except Exception as e:
            return f"Error generating questions: {str(e)}"
    
    def provide_hints(self, question: str, context: str) -> str:
        """Provide hints without giving away the answer"""
        prompt = f"""A student is stuck on this question: "{question}"

Context: {context}

Provide 2-3 helpful hints that guide them toward the answer WITHOUT directly giving it away.
Use the Socratic method - ask guiding questions, point to key concepts, suggest what to think about.

HINTS:"""

        try:
            response = ollama.generate(
                model=self.small_model,
                prompt=prompt,
                options={'temperature': 0.7, 'num_predict': 200}
            )
            return response['response'].strip()
        except Exception as e:
            return f"Error generating hints: {str(e)}"
    
    def export_conversation(self, filename: str = None) -> str:
        """Export conversation history to JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        filepath = CONVERSATIONS_DIR / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'student_level': self.student_level,
                    'export_time': datetime.now().isoformat(),
                    'conversation': self.conversation_history
                }, f, indent=2, ensure_ascii=False)
            
            return str(filepath)
        except Exception as e:
            return f"Error exporting: {str(e)}"


class QueryRouter:
    def __init__(self, vector_store, llm_manager):
        self.vector_store = vector_store
        self.llm_manager = llm_manager
        print("QueryRouter initialized", end="\n")
    
    def answer_query(self, query: str, n_results: int = 5) -> Dict:
        """Main pipeline: retrieve context and generate answer"""
        print(f"\n=== Processing Query ===", end="\n")
        print(f"Query: {query}", end="\n")
        
        # Step 1: Retrieve relevant context
        print("\nStep 1: Retrieving relevant context...", end="\n")
        search_results = self.vector_store.query(query, n_results=n_results)
        
        # Combine context
        context_chunks = search_results['documents']
        context = "\n\n".join(context_chunks)
        
        print(f"Retrieved {len(context_chunks)} relevant chunks", end="\n")
        
        # Step 2: Classify complexity
        print("\nStep 2: Classifying query complexity...", end="\n")
        complexity = self.llm_manager.classify_query_complexity(query)
        
        # Step 3: Generate answer
        print("\nStep 3: Generating answer...", end="\n")
        answer = self.llm_manager.generate_response(query, context, complexity)
        
        # Step 4: Add to history
        sources = [meta['source'] for meta in search_results['metadatas']]
        if hasattr(self.llm_manager, 'add_to_history'):
            self.llm_manager.add_to_history(query, answer, sources)
        
        return {
            'query': query,
            'answer': answer,
            'complexity': complexity,
            'sources': [
                {
                    'text': doc[:200] + "...",
                    'metadata': meta,
                    'similarity': 1 - dist
                }
                for doc, meta, dist in zip(
                    search_results['documents'],
                    search_results['metadatas'],
                    search_results['distances']
                )
            ]
        }
    
    def generate_quiz(self, topic: str = None, n_questions: int = 3) -> str:
        """Generate a quiz from uploaded materials"""
        if topic:
            results = self.vector_store.query(topic, n_results=5)
        else:
            stats = self.vector_store.get_stats()
            if stats['total_documents'] == 0:
                return "No documents available for quiz generation."
            results = self.vector_store.query("key concepts main topics", n_results=5)
        
        context = "\n\n".join(results['documents'])
        
        if hasattr(self.llm_manager, 'generate_review_questions'):
            return self.llm_manager.generate_review_questions(
                topic or "the uploaded materials", 
                context, 
                n_questions
            )
        return "Quiz generation not available with current LLM manager."
    
    def get_hint(self, question: str) -> str:
        """Get hints for a question"""
        results = self.vector_store.query(question, n_results=3)
        context = "\n\n".join(results['documents'])
        
        if hasattr(self.llm_manager, 'provide_hints'):
            return self.llm_manager.provide_hints(question, context)
        return "Hint generation not available."
