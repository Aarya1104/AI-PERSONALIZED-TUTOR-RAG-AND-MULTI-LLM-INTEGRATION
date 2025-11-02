from document_loader import DocumentLoader
from vector_store import VectorStore
from llm_manager import EnhancedLLMManager, QueryRouter

print("\n" + "="*80, end="\n")
print("🧪 AI TUTOR MODEL TEST CASES", end="\n")
print("="*80 + "\n", end="\n")

# Initialize
loader = DocumentLoader()
vector_store = VectorStore()
llm_manager = EnhancedLLMManager()
router = QueryRouter(vector_store, llm_manager)

# Process sample document
print("Step 1: Processing sample document...", end="\n")
documents = loader.process_document("uploads/sample_textbook.txt")
vector_store.add_documents(documents)
print(f"✅ Loaded {len(documents)} chunks\n", end="\n")

# Test cases
test_cases = [
    {
        'name': 'Simple Question (phi3:mini expected)',
        'query': 'What is photosynthesis?',
        'expected_model': 'phi3:mini',
        'reason': 'Simple definition question'
    },
    {
        'name': 'Complex Question (mistral:7b expected)',
        'query': 'Compare photosynthesis and cellular respiration. Explain the differences and how they relate to each other.',
        'expected_model': 'mistral:7b',
        'reason': 'Complex - uses "compare", multiple concepts'
    },
    {
        'name': 'Definition Query (phi3:mini expected)',
        'query': 'What is chlorophyll?',
        'expected_model': 'phi3:mini',
        'reason': 'Simple definition'
    },
    {
        'name': 'Detailed Explanation (mistral:7b expected)',
        'query': 'Explain in detail how the light reactions and Calvin cycle work together.',
        'expected_model': 'mistral:7b',
        'reason': 'Complex - "explain in detail"'
    },
]

# Run tests
for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}", end="\n")
    print(f"TEST {i}: {test['name']}", end="\n")
    print(f"{'='*80}", end="\n")
    print(f"Query: {test['query']}", end="\n")
    print(f"Expected Model: {test['expected_model']}", end="\n")
    print(f"Reason: {test['reason']}", end="\n")
    print("-" * 80, end="\n")
    
    result = router.answer_query(test['query'], n_results=3)
    
    complexity = result['complexity']
    model_used = 'mistral:7b' if complexity == 'complex' else 'phi3:mini'
    
    print(f"Query Complexity: {complexity}", end="\n")
    print(f"Model Used: {model_used}", end="\n")
    
    if model_used == test['expected_model']:
        print("✅ PASS - Correct model used!", end="\n")
    else:
        print(f"⚠️  MISMATCH - Expected {test['expected_model']} but got {model_used}", end="\n")
    
    print(f"\nAnswer Preview: {result['answer'][:200]}...", end="\n")

print("\n" + "="*80, end="\n")
print("✅ ALL TESTS COMPLETED", end="\n")
print("="*80 + "\n", end="\n")
