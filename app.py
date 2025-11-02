import gradio as gr
from pathlib import Path
from document_loader import DocumentLoader
from vector_store import VectorStore
from llm_manager import EnhancedLLMManager, QueryRouter
import os
from datetime import datetime

class AITutorApp:
    def __init__(self):
        print("Initializing AI Tutor Application...", end="\n")
        self.loader = DocumentLoader()
        self.vector_store = VectorStore()
        self.llm_manager = EnhancedLLMManager()
        self.llm_manager.set_student_level("intermediate")
        self.router = QueryRouter(self.vector_store, self.llm_manager)
        print("Application initialized successfully", end="\n")
    
    def upload_document(self, file):
        """Handle document upload and processing"""
        if file is None:
            return "No file uploaded", ""
        
        try:
            file_path = file.name
            filename = Path(file_path).name
            
            print(f"\nProcessing uploaded file: {filename}", end="\n")
            
            documents = self.loader.process_document(file_path)
            
            if not documents:
                return f"Error: Could not process {filename}", ""
            
            self.vector_store.add_documents(documents)
            
            stats = self.vector_store.get_stats()
            
            success_msg = f"""✅ Successfully processed: {filename}
            
📊 Statistics:
- Text chunks created: {len(documents)}
- Total documents in database: {stats['total_documents']}
- Embedding model: {stats['embedding_model']}
- Device: {stats['device']}
- Hybrid Search: {'✅' if stats['hybrid_search'] else '❌'}
- Reranking: {'✅' if stats['reranking'] else '❌'}

You can now ask questions about this material!"""
            
            return success_msg, ""
            
        except Exception as e:
            return f"❌ Error processing file: {str(e)}", ""
    
    def answer_question(self, question, history):
        """Handle question answering with model indication"""
        if not question.strip():
            return history + [("", "Please enter a question.")]
        
        stats = self.vector_store.get_stats()
        if stats['total_documents'] == 0:
            return history + [(question, "⚠️ No documents uploaded yet. Please upload study materials first.")]
        
        try:
            result = self.router.answer_query(question, n_results=5)
            
            # Determine which model was used
            complexity = result['complexity']
            model_used = 'mistral:7b (Detailed)' if complexity == 'complex' else 'phi3:mini (Fast)'
            
            answer = f"""**🤖 Model: {model_used}**
**Query Type: {complexity}**

**📚 Answer:**

{result['answer']}

---
**📖 Sources:**
"""
            for i, source in enumerate(result['sources'][:3], 1):
                similarity_pct = source['similarity'] * 100
                answer += f"\n{i}. {source['metadata']['source']} (Chunk {source['metadata']['chunk_id']}) - {similarity_pct:.1f}% relevant"
            
            return history + [(question, answer)]
            
        except Exception as e:
            return history + [(question, f"❌ Error: {str(e)}")]
    
    def generate_quiz_handler(self, topic, num_questions):
        """Handle quiz generation"""
        try:
            quiz = self.router.generate_quiz(topic if topic.strip() else None, int(num_questions))
            return f"📝 **Generated Quiz:**\n\n{quiz}"
        except Exception as e:
            return f"❌ Error generating quiz: {str(e)}"
    
    def get_hint_handler(self, question):
        """Handle hint request"""
        if not question.strip():
            return "Please enter a question to get hints for."
        
        try:
            hints = self.router.get_hint(question)
            return f"💡 **Hints:**\n\n{hints}"
        except Exception as e:
            return f"❌ Error generating hints: {str(e)}"
    
    def change_level(self, level):
        """Change student proficiency level"""
        self.llm_manager.set_student_level(level)
        return f"✅ Student level changed to: {level}"
    
    def clear_database(self):
        """Clear all documents"""
        self.vector_store.clear_collection()
        return "🗑️ All documents cleared from database.", []
    
    def export_conversation_handler(self):
        """Export conversation"""
        try:
            filepath = self.llm_manager.export_conversation()
            return f"✅ Conversation exported to: {filepath}"
        except Exception as e:
            return f"❌ Error exporting: {str(e)}"
    
    def get_stats_display(self):
        """Get formatted statistics"""
        stats = self.vector_store.get_stats()
        history_count = len(self.llm_manager.conversation_history) if hasattr(self.llm_manager, 'conversation_history') else 0
        
        return f"""**System Statistics:**
- Total Documents: {stats['total_documents']}
- Questions Asked: {history_count}
- Student Level: {self.llm_manager.student_level}
- Hybrid Search: {'✅' if stats['hybrid_search'] else '❌'}
- Reranking: {'✅' if stats['reranking'] else '❌'}
- Device: {stats['device']}

**Model Information:**
- Small Model: phi3:mini (simple queries)
- Large Model: mistral:7b (complex queries)"""
    
    def launch(self):
        """Launch Gradio interface"""
        
        with gr.Blocks(title="AI Personalized Tutor", theme=gr.themes.Soft()) as demo:
            
            gr.Markdown("""
            # 🎓 AI Personalized Tutor
            ### RAG-Powered Learning Assistant with Multi-LLM Integration
            
            **Features:** Hybrid Search • Intelligent Reranking • Adaptive Teaching • Quiz Generation • Model Tracking
            
            **Perfect for:** NCERT Textbooks, 9th-10th Grade Students in India
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📤 Upload Study Materials")
                    
                    file_input = gr.File(
                        label="Upload PDF or TXT files",
                        file_types=[".pdf", ".txt"],
                        type="filepath"
                    )
                    
                    upload_btn = gr.Button("Process Document", variant="primary")
                    upload_output = gr.Textbox(
                        label="Upload Status",
                        lines=10,
                        interactive=False
                    )
                    
                    with gr.Row():
                        clear_btn = gr.Button("Clear Database", variant="stop", scale=1)
                        export_btn = gr.Button("Export Chat", variant="secondary", scale=1)
                    
                    export_output = gr.Textbox(label="Export Status", lines=2)
                    
                    gr.Markdown("### 🎯 Student Level")
                    level_dropdown = gr.Radio(
                        choices=["beginner", "intermediate", "advanced"],
                        value="intermediate",
                        label="Set Learning Level"
                    )
                    level_output = gr.Textbox(label="Level Status", lines=1)
                    
                    gr.Markdown("### 📊 Statistics")
                    stats_btn = gr.Button("Refresh Stats")
                    stats_display = gr.Markdown()
                
                with gr.Column(scale=2):
                    gr.Markdown("### 💬 Ask Questions")
                    
                    chatbot = gr.Chatbot(
                        label="Conversation",
                        height=450
                    )
                    
                    with gr.Row():
                        question_input = gr.Textbox(
                            label="Your Question",
                            placeholder="Ask anything about your uploaded materials...",
                            lines=2,
                            scale=4
                        )
                        submit_btn = gr.Button("Ask", variant="primary", scale=1)
                    
                    gr.Examples(
                        examples=[
                            "What is photosynthesis?",
                            "Explain photosynthesis and cellular respiration in detail",
                            "Compare aerobic and anaerobic respiration",
                            "Why is photosynthesis important?"
                        ],
                        inputs=question_input
                    )
                    
                    gr.Markdown("### 🎯 Learning Tools")
                    
                    with gr.Tab("📝 Generate Quiz"):
                        quiz_topic = gr.Textbox(
                            label="Topic (leave blank for general quiz)",
                            placeholder="e.g., photosynthesis"
                        )
                        quiz_num = gr.Slider(
                            minimum=3,
                            maximum=10,
                            value=5,
                            step=1,
                            label="Number of Questions"
                        )
                        quiz_btn = gr.Button("Generate Quiz", variant="secondary")
                        quiz_output = gr.Markdown()
                    
                    with gr.Tab("💡 Get Hints"):
                        hint_question = gr.Textbox(
                            label="Question you're stuck on",
                            placeholder="Enter a question to get hints..."
                        )
                        hint_btn = gr.Button("Get Hints", variant="secondary")
                        hint_output = gr.Markdown()
            
            # Event handlers
            upload_btn.click(
                fn=self.upload_document,
                inputs=[file_input],
                outputs=[upload_output, question_input]
            )
            
            submit_btn.click(
                fn=self.answer_question,
                inputs=[question_input, chatbot],
                outputs=[chatbot]
            ).then(
                lambda: "",
                outputs=[question_input]
            )
            
            question_input.submit(
                fn=self.answer_question,
                inputs=[question_input, chatbot],
                outputs=[chatbot]
            ).then(
                lambda: "",
                outputs=[question_input]
            )
            
            clear_btn.click(
                fn=self.clear_database,
                outputs=[upload_output, chatbot]
            )
            
            export_btn.click(
                fn=self.export_conversation_handler,
                outputs=[export_output]
            )
            
            level_dropdown.change(
                fn=self.change_level,
                inputs=[level_dropdown],
                outputs=[level_output]
            )
            
            quiz_btn.click(
                fn=self.generate_quiz_handler,
                inputs=[quiz_topic, quiz_num],
                outputs=[quiz_output]
            )
            
            hint_btn.click(
                fn=self.get_hint_handler,
                inputs=[hint_question],
                outputs=[hint_output]
            )
            
            stats_btn.click(
                fn=self.get_stats_display,
                outputs=[stats_display]
            )
            
            demo.load(
                fn=self.get_stats_display,
                outputs=[stats_display]
            )
            
            gr.Markdown("""
            ---
            ### 🚀 Features
            
            **Intelligent Retrieval:**
            - Hybrid Search (Semantic + Keyword)
            - Intelligent Reranking
            - Conversation Context
            
            **Adaptive Teaching:**
            - 3 Learning Levels
            - Adaptive Explanations
            - Real-World Examples
            
            **Smart Model Routing:**
            - Simple queries → phi3:mini (fast)
            - Complex queries → mistral:7b (detailed)
            
            **Learning Tools:**
            - Auto-generated quizzes
            - Socratic hints
            - Source citations
            - Conversation export
            """)
        
        demo.launch(share=False, server_name="127.0.0.1", server_port=7860)

if __name__ == "__main__":
    app = AITutorApp()
    app.launch()
