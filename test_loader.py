from document_loader import DocumentLoader

# Test with a sample text
loader = DocumentLoader()

# Create a sample text file for testing
sample_text = """
Machine Learning is a subset of artificial intelligence that focuses on algorithms and statistical models.
Deep Learning is a specialized form of machine learning using neural networks with multiple layers.
Natural Language Processing enables computers to understand and process human language.
""" * 100  # Repeat to create enough text for chunking

# Save sample file
with open("uploads/sample.txt", "w", encoding="utf-8") as f:
    f.write(sample_text)

# Test document processing
documents = loader.process_document("uploads/sample.txt")
print(f"\nFirst chunk preview:", end="\n")
print(documents[0]['text'][:200], end="\n")
print(f"\nMetadata:", end="\n")
print(documents[0]['metadata'], end="\n")
