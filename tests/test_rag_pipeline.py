"""
RAG Pipeline Integration Test

Tests the complete RAG pipeline end-to-end:
- QA chain creation
- Vector store loading
- Ollama LLM integration
- Query processing
- Source document retrieval

Usage:
    python -m tests.test_rag_pipeline
"""

from dotenv import load_dotenv
load_dotenv()

from app.components.retriever import create_qa_chain
import traceback
import time


def test_qa_chain_creation():
    """Test that QA chain can be created successfully"""
    print("=" * 60)
    print("TEST 1: QA Chain Creation")
    print("=" * 60)

    try:
        qa_chain = create_qa_chain()
        print("✅ QA chain created successfully!")
        return qa_chain
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print(traceback.format_exc())
        return None


def test_query_processing(qa_chain, question="What is diabetes?"):
    """Test query processing with sample medical question"""
    print("\n" + "=" * 60)
    print("TEST 2: Query Processing")
    print("=" * 60)

    if not qa_chain:
        print("❌ SKIPPED: QA chain not available")
        return

    try:
        print(f"\n📝 Question: {question}")

        # Measure response time
        start_time = time.time()
        response = qa_chain.invoke({"query": question})
        elapsed_time = time.time() - start_time

        print(f"⏱️  Response time: {elapsed_time:.2f} seconds")

        # Validate response structure
        if not isinstance(response, dict):
            print(f"❌ FAILED: Expected dict, got {type(response)}")
            return

        print(f"✅ Response type: dict")
        print(f"✅ Response keys: {list(response.keys())}")

        # Extract and display answer
        answer = response.get('result', 'NO RESULT KEY')
        print(f"\n💬 Answer:\n{answer}")

        # Extract and display sources
        source_docs = response.get('source_documents', [])
        print(f"\n📚 Sources found: {len(source_docs)}")

        if source_docs:
            print("\nSource details:")
            for i, doc in enumerate(source_docs[:3], 1):
                source = doc.metadata.get('source', 'Unknown')
                page = doc.metadata.get('page_label', doc.metadata.get('page', 'N/A'))
                print(f"  {i}. {source.split('/')[-1]} (Page {page})")

        print("\n✅ Query processing successful!")

    except Exception as e:
        print(f"\n❌ FAILED: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc())


def test_multiple_queries(qa_chain):
    """Test multiple different medical queries"""
    print("\n" + "=" * 60)
    print("TEST 3: Multiple Queries")
    print("=" * 60)

    if not qa_chain:
        print("❌ SKIPPED: QA chain not available")
        return

    test_questions = [
        "What causes hypertension?",
        "How is asthma treated?",
        "What are the symptoms of pneumonia?"
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Query {i}/3 ---")
        print(f"Question: {question}")

        try:
            start_time = time.time()
            response = qa_chain.invoke({"query": question})
            elapsed_time = time.time() - start_time

            answer = response.get('result', 'No answer')
            print(f"Answer: {answer[:100]}...")  # First 100 chars
            print(f"Time: {elapsed_time:.2f}s")
            print("✅ Success")

        except Exception as e:
            print(f"❌ Failed: {str(e)}")


def main():
    """Run all tests"""
    print("\n🧪 RAG Pipeline Integration Tests")
    print("=" * 60)

    # Test 1: Create QA chain
    qa_chain = test_qa_chain_creation()

    # Test 2: Single query
    test_query_processing(qa_chain)

    # Test 3: Multiple queries (optional - commented out to save time)
    # test_multiple_queries(qa_chain)

    print("\n" + "=" * 60)
    print("🏁 Test suite completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
