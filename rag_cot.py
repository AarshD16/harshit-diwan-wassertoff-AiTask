# RAG Configuration
from data_retrieval import vector_database
from transformers import RagRetriever, RagTokenizer, RagSequenceForGeneration


# Custom retriever class using FAISS
class CustomRagRetriever(RagRetriever):
    def __init__(self, vector_database, tokenizer, **kwargs):
        super().__init__(tokenizer=tokenizer, **kwargs)
        self.vector_database = vector_database

    def retrieve(self, query_embeddings, n_docs=5):
        # Retrieve the closest embeddings from the vector database
        distances, indices = self.vector_database.search(query_embeddings, n_docs)

        # Create documents to return based on the retrieved indices
        documents = []
        for idx in indices[0]:
            document = {
                "title": f"Document {idx}",
                "content": f"Content for document {idx}",
                "score": distances[0][idx],
            }
            documents.append(document)

        return documents


def configure_rag(tokenizer):
    custom_retriever = CustomRagRetriever(
        vector_database,
        tokenizer=tokenizer,  # Pass the tokenizer as expected by the custom retriever
        index_name="custom",
    )
    model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq", retriever=custom_retriever)

    return tokenizer, custom_retriever, model


# Chain of Thought module for processing queries
def process_query_with_chain_of_thought(model, tokenizer, user_query, context):
    # Initial response using RAG
    inputs = tokenizer([user_query], return_tensors="pt")
    outputs = model.generate(inputs["input_ids"])
    initial_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Develop reasoning steps
    thought_steps = develop_reasoning_steps(initial_response, context)

    # Refine response based on CoT logic
    final_response = refine_response_based_on_thought_steps(thought_steps)

    return final_response


# Helper functions for Chain of Thought
def develop_reasoning_steps(initial_response, context):
    steps = []
    steps.append(f"Given the context '{context}', here's the response: {initial_response}")
    steps.append("Let's consider additional information...")

    # Add more steps based on desired reasoning or context
    return steps


def refine_response_based_on_thought_steps(thought_steps):
    # Create a coherent final response
    response = "\n".join(thought_steps)
    return response
