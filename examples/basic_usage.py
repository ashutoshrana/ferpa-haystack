"""
Basic usage of ferpa-haystack.

Shows how to add FERPA-compliant filtering to a Haystack RAG pipeline.

Install: pip install ferpa-haystack haystack-ai
"""

from haystack import Document, Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.components.retrievers import InMemoryEmbeddingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore

from haystack_integrations.components.filters.ferpa_filter import FERPAMetadataFilter

# Build a sample document store with identity-tagged records
doc_store = InMemoryDocumentStore()
doc_store.write_documents([
    # Student stu_001's records
    Document(
        content="Alice Johnson — GPA: 3.85, Major: Computer Science, Credits: 92/120",
        meta={"student_id": "stu_001", "institution_id": "univ_abc", "category": "academic_record"},
    ),
    Document(
        content="Alice Johnson — Financial Aid Award 2025: $15,000 Pell Grant + $8,500 Subsidized Loan",
        meta={"student_id": "stu_001", "institution_id": "univ_abc", "category": "financial_aid"},
    ),
    # Another student's record — should be blocked
    Document(
        content="Bob Smith — GPA: 2.9, Academic Probation Notice",
        meta={"student_id": "stu_002", "institution_id": "univ_abc", "category": "academic_record"},
    ),
    # Shared knowledge base — no identity metadata — always passes through
    Document(
        content="University Graduation Requirements: 120 credits, minimum 2.0 GPA",
        meta={},
    ),
])

# FERPA filter — only Alice's academic and financial aid records pass through
ferpa_filter = FERPAMetadataFilter(
    student_id="stu_001",
    institution_id="univ_abc",
    authorized_categories=["academic_record", "financial_aid"],
    requesting_user_id="advisor_007",
    pipeline_context="student_advising_chatbot",
)

# Build pipeline — retriever → FERPA filter → LLM
pipeline = Pipeline()
pipeline.add_component("retriever", InMemoryEmbeddingRetriever(doc_store))
pipeline.add_component("ferpa_filter", ferpa_filter)
pipeline.add_component(
    "prompt",
    PromptBuilder(template="Answer using only the provided student records:\n{% for doc in documents %}{{ doc.content }}\n{% endfor %}\n\nQuestion: {{ question }}")
)
pipeline.add_component("llm", OpenAIGenerator(model="gpt-4o-mini"))

pipeline.connect("retriever.documents", "ferpa_filter.documents")
pipeline.connect("ferpa_filter.documents", "prompt.documents")
pipeline.connect("prompt.prompt", "llm.prompt")

# The FERPA filter ensures Bob's record never reaches the LLM
# result = pipeline.run({
#     "retriever": {"query_embedding": embed("What is Alice's GPA?")},
#     "prompt": {"question": "What is the student's GPA?"},
# })

# Standalone usage (no embedding needed for this demo)
sample_docs = [
    Document(
        content="Alice — GPA 3.85",
        meta={"student_id": "stu_001", "institution_id": "univ_abc", "category": "academic_record"},
    ),
    Document(
        content="Bob — GPA 2.9",  # different student
        meta={"student_id": "stu_002", "institution_id": "univ_abc", "category": "academic_record"},
    ),
    Document(
        content="Graduation requires 120 credits",  # shared content
        meta={},
    ),
]

result = ferpa_filter.run(sample_docs)
print(f"Input: {len(sample_docs)} documents")
print(f"After FERPA filter: {len(result['documents'])} documents")
print(f"Audit log: {result['disclosure_record'].to_log_entry()}")

# Expected output:
# Input: 3 documents
# After FERPA filter: 2 documents  (Alice's record + shared graduation info)
# Audit log: [FERPA_DISCLOSURE] student_id='stu_001' ... total_retrieved=3 total_disclosed=2
