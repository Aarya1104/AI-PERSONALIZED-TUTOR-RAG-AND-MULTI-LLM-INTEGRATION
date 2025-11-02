# AI Personalized Tutor

## RAG-Powered Learning Assistant with Multi-LLM Integration

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Aarya1104/AI-PERSONALIZED-TUTOR-RAG-AND-MULTI-LLM-INTEGRATION/releases/tag/v1.0.0)
[![Python](https://img.shields.io/badge/python-3.10.11-green.svg)](https://www.python.org/downloads/release/python-31011/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active%20Development-brightgreen.svg)](https://github.com/Aarya1104/AI-PERSONALIZED-TUTOR-RAG-AND-MULTI-LLM-INTEGRATION)

---

## Overview

An intelligent tutoring platform that creates a vectorized knowledge base from uploaded learning materials and dynamically answers queries using a hybrid retrieval system with multi-LLM pipeline. Specifically designed for secondary education students (grades 9-10) in India utilizing NCERT curriculum materials.

---

## Core Features

### Intelligent Retrieval System

- **Hybrid Search Architecture**: Integrates semantic understanding through sentence-transformers with BM25 keyword matching for optimal information retrieval
- **Intelligent Reranking**: FlashRank optimization ensures highest relevance results are prioritized
- **Contextual Understanding**: Conversation history tracking enables coherent multi-turn interactions and contextual awareness

### Smart Multi-LLM Routing

- **Phi3:mini**: Optimized for rapid responses to straightforward queries (response time under 2 seconds)
- **Mistral:7b**: Advanced model for detailed analysis of complex, multi-component questions
- **Automatic Classification**: System automatically routes queries to appropriate model based on complexity analysis, eliminating manual model selection

### Adaptive Teaching System

- **Three Proficiency Levels**: Beginner, Intermediate, Advanced
- **Dynamic Response Adaptation**: Explanation complexity automatically adjusts based on student proficiency level
- **Contextual Examples**: Real-world analogies and practical applications tailored to student comprehension level
- **Structured Learning**: Complex concepts decomposed into sequential, digestible components

### Interactive Learning Tools

- **Automated Quiz Generation**: Creates review questions dynamically from uploaded materials on any specified topic
- **Socratic Method Implementation**: Provides guided hints without revealing direct answers to encourage critical thinking
- **Source Attribution**: Transparent retrieval mechanism displays exact content sources for all responses
- **Session Export**: Complete conversation histories exportable as JSON format for review and progress tracking

### Knowledge Management

- **ChromaDB Vector Storage**: Efficient semantic indexing with persistent storage capabilities
- **Multi-Format Document Processing**: Supports PDF and TXT formats with intelligent text chunking
- **Scalable Knowledge Base**: Supports multiple document uploads to build comprehensive subject knowledge bases

---

## System Requirements

### Minimum Requirements

- **Python Version**: 3.10.11 or higher
- **RAM**: 16GB minimum (32GB recommended for optimal performance)
- **Disk Space**: Approximately 20GB for models and data storage
- **Ollama**: Local LLM runtime environment

### Supported Platforms

- Windows 10/11
- macOS 10.15 or higher
- Linux (Ubuntu 20.04+, Debian 11+)

---

## Installation Guide

### Step 1: Install Ollama

Download and install Ollama from the official website: [ollama.com](https://ollama.com)

Verify installation:

```bash
ollama --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/Aarya1104/AI-PERSONALIZED-TUTOR-RAG-AND-MULTI-LLM-INTEGRATION.git
cd AI-PERSONALIZED-TUTOR-RAG-AND-MULTI-LLM-INTEGRATION
```

### Step 3: Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Download LLM Models

Models are downloaded once and cached locally (approximately 7GB total storage required):

**Small model for simple queries (2.3GB):**

```bash
ollama pull phi3:mini
```

**Large model for complex queries (4.1GB):**

```bash
ollama pull mistral:7b
```

**Verify installation:**

```bash
ollama list
```

### Step 6: Launch Application

```bash
python app.py
```

The application will be accessible at: `http://127.0.0.1:7860`

---

## User Guide

### 1. Upload Study Materials

1. Click the "Upload PDF or TXT files" button
2. Select NCERT textbook or study materials
3. Wait for processing completion
4. Review processing statistics including chunks created and database size

### 2. Configure Student Level

Select appropriate proficiency level for response adaptation:

- **Beginner**: Simplified language with extensive analogies and examples
- **Intermediate**: Clear explanations with defined technical terminology
- **Advanced**: Precise technical language with nuanced discussions

### 3. Submit Queries

Submit questions regarding uploaded materials:

- **Simple queries**: "What is photosynthesis?"
- **Complex queries**: "Compare and contrast photosynthesis and cellular respiration in detail"
- System automatically routes queries to appropriate model based on complexity

### 4. Generate Quizzes

1. Navigate to "Generate Quiz" tab
2. Optionally specify topic area
3. Select number of questions (3-10)
4. Receive automatically generated review questions

### 5. Request Learning Hints

1. Navigate to "Get Hints" tab
2. Enter question requiring assistance
3. Receive Socratic hints promoting guided learning
4. Develop understanding through structured thinking

### 6. Export Conversation History

1. Click "Export Chat" button
2. Complete conversation history saved as JSON format
3. Utilize for review or study note compilation

---

## Technical Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | Text vectorization and semantic encoding |
| **Vector Database** | ChromaDB | Persistent semantic storage and retrieval |
| **Retrieval System** | BM25 + Semantic Hybrid | Flexible dual-mode search mechanism |
| **Reranking** | FlashRank | Result relevance optimization |
| **Language Models** | Phi3:mini, Mistral:7b via Ollama | Local inference engine |
| **User Interface** | Gradio | Web-based interface framework |
| **Core Language** | Python 3.10.11 | Primary implementation language |

### System Architecture Flow

```
┌─────────────────────────┐
│   Upload Materials      │
│   (PDF/TXT Format)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Document Processing    │
│  • Text extraction      │
│  • Semantic chunking    │
│  • Metadata tagging     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Embedding Generation   │
│  • Vector conversion    │
│  • ChromaDB storage     │
│  • BM25 index build     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐         User Query
│   Hybrid Retrieval      │◄────────────────────
│   • Semantic search     │
│   • Keyword search      │
│   • Smart reranking     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    Query Routing        │
│    • Complexity check   │
│    • Model selection    │
└───────────┬─────────────┘
            │
      ┌─────┴─────┐
      ▼           ▼
┌──────────┐  ┌──────────┐
│ Phi3:mini│  │Mistral:7b│
│  (Fast)  │  │(Detailed)│
└─────┬────┘  └────┬─────┘
      │            │
      └─────┬──────┘
            ▼
    ┌───────────────┐
    │ LLM Response  │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │   Display     │
    │   with        │
    │   Citations   │
    └───────────────┘
```

---

## Dependency Specifications

### Python Package Requirements

```
torch==2.1.0
transformers==4.35.0
sentence-transformers==2.2.2
chromadb==0.4.18
gradio==4.7.1
pypdf==3.17.0
langchain-text-splitters==0.0.1
ollama==0.1.6
rank-bm25==0.2.2
flashrank==0.2.4
numpy==1.24.3
```

### Model Specifications

- **phi3:mini**: 2.3GB (optimized for speed and simple query processing)
- **mistral:7b**: 4.1GB (enhanced reasoning capabilities for complex analysis)
- **Total Storage**: Approximately 6.5GB (one-time download, persistent cache)

### Data Storage Structure

```
data/
├── chroma_db/              # Vector database (scales with document uploads)
└── conversations/          # Exported chat histories (JSON format)

uploads/
├── sample.txt              # Upload location for study materials
└── textbooks/              # NCERT books and supplementary materials
```

---

## Project Structure

```
ai-tutor-rag/
├── app.py                  # Main Gradio interface
├── config.py               # Configuration and system settings
├── document_loader.py      # PDF/TXT processing module
├── vector_store.py         # ChromaDB and retrieval logic
├── llm_manager.py          # Multi-LLM orchestration
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore
├── data/
│   ├── chroma_db/         # Vector database (auto-generated)
│   └── conversations/      # Exported chat sessions
├── uploads/
│   └── .gitkeep
└── models/
    └── .gitkeep
```

---

## Configuration Parameters

Edit `config.py` to customize system behavior:

```python
# Learning parameters
CHUNK_SIZE = 1000           # Document chunk size in characters
CHUNK_OVERLAP = 200         # Overlap for context preservation

# Search settings
USE_HYBRID_SEARCH = True    # Enable hybrid search mode
HYBRID_ALPHA = 0.5          # Balance: 0.5 = 50% semantic, 50% keyword
USE_RERANKING = True        # Enable result reranking

# Device configuration
DEVICE = "cpu"              # Use "cuda" for GPU acceleration

# Conversation settings
MAX_HISTORY_LENGTH = 10     # Retain last 10 interactions
```

---

## Development Roadmap

### Version 1.0.0 (Current Release)

- Hybrid search with intelligent reranking
- Multi-LLM routing (phi3:mini + mistral:7b)
- Adaptive teaching with three proficiency levels
- Automated quiz generation functionality
- Socratic hints system
- Conversation export capability

### Version 1.1.0 (Planned)

- **Docker Containerization**: Pre-configured containers for simplified deployment
  - Single-command setup via `docker-compose up`
  - Cloud platform support (AWS, Azure, Google Cloud, DigitalOcean)
  - Optional GPU acceleration support

### Version 2.0.0 (Future Development)

- Vision support via LLaVA for diagram and image analysis
- Progress tracking dashboard with analytics
- Spaced repetition system implementation
- Multi-language support for regional languages
- Enhanced API integration options
- Fine-tuned models optimized for Indian curriculum
- Mobile application (React Native implementation)
- Multi-user support with individual progress tracking and authentication

---

## Usage Examples

### Example 1: Biology Study Session

**Upload**: NCERT Biology Textbook (Chapter 13: Photosynthesis)

**Set Level**: Beginner

**Query 1**: "What is photosynthesis?"
- **Result**: Simple, beginner-friendly explanation with analogies

**Query 2**: "Explain the light reactions in detail"
- **Result**: System routes to mistral:7b for comprehensive analysis

**Generate Quiz**: 5 questions on photosynthesis mechanisms

**Request Hints**: Socratic guidance for challenging questions

**Export**: Complete session saved for future review

### Example 2: Board Exam Preparation Workflow

**Upload**: Complete NCERT Science textbook series (Physics, Chemistry, Biology)

**Set Level**: Intermediate

**Daily Study Routine**:

1. Submit concept clarification questions
2. Generate practice quizzes for each chapter
3. Export session notes for offline review
4. Track progress over study period

---

## Contributing Guidelines

Contributions are welcome. To contribute:

1. Fork the repository
2. Create feature branch:
   ```bash
   git checkout develop
   git checkout -b feature/your-feature-name
   ```
3. Implement changes with appropriate tests
4. Commit with descriptive messages
5. Push to origin:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Submit pull request via GitHub with detailed description

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for complete terms and conditions.

---

## Support and Issue Reporting

- **Bug Reports**: Submit via [GitHub Issues](https://github.com/Aarya1104/AI-PERSONALIZED-TUTOR-RAG-AND-MULTI-LLM-INTEGRATION/issues)
- **Feature Requests**: Propose via [GitHub Discussions](https://github.com/Aarya1104/AI-PERSONALIZED-TUTOR-RAG-AND-MULTI-LLM-INTEGRATION/discussions)
- **Documentation**: Refer to project wiki for detailed technical documentation

---

## Target Audience

This platform serves:

- Secondary school students (grades 9-10) following NCERT curriculum in India
- Self-paced learners requiring personalized educational assistance
- Students preparing for Board examinations and competitive assessments
- Educators creating customized learning materials
- Researchers exploring RAG and adaptive learning systems
- Developers building educational AI applications

---

## Technical Details

**Architecture Approach**: Intelligent tutoring system combining modern artificial intelligence techniques including Retrieval-Augmented Generation (RAG), multi-model orchestration, adaptive learning systems, and open-source language models for local deployment.

**Primary Technologies**: Python, ChromaDB, Ollama, Gradio, Sentence Transformers, FlashRank

**Development Focus**: Educational AI platform optimized for secondary education in Indian curriculum context.

---

## Project Metadata

**Author**: Aarya Joshi  
**GitHub Profile**: [@Aarya1104](https://github.com/Aarya1104)  
**Repository**: [AI-PERSONALIZED-TUTOR-RAG-AND-MULTI-LLM-INTEGRATION](https://github.com/Aarya1104/AI-PERSONALIZED-TUTOR-RAG-AND-MULTI-LLM-INTEGRATION)  
**Current Version**: 1.0.0  
**Release Date**: November 2025  
**Status**: Active Development

---

## Quick Navigation

- [Installation Guide](#installation-guide)
- [User Guide](#user-guide)
- [Technical Architecture](#technical-architecture)
- [Development Roadmap](#development-roadmap)
- [Contributing Guidelines](#contributing-guidelines)
- [License](#license)

---

**Built as an educational AI platform for enhanced student learning outcomes.**