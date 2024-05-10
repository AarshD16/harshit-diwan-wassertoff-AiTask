import requests
import torch
import faiss
from transformers import AutoTokenizer, AutoModel

# Function to fetch WordPress data using the REST API
def get_wordpress_content(api_url):
    res = requests.get(api_url)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("Failed to fetch data from WordPress.")

# Function to extract content from a WordPress post
def get_post_content(post):
    return post['content']['rendered']

# Function to create embeddings from text using a pre-trained model
def text_to_embeddings(text):
    # Use a suitable model to generate embeddings
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # Generate embeddings from tokenized text
    tokens = tokenizer([text], return_tensors="pt", padding=True, truncation=True)
    outputs = model(**tokens)

    # Get the mean of the last hidden state for a single embedding
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()

    return embeddings

# Initialize a FAISS-based vector database that supports IDs
embedding_dimension = 384
flat_index = faiss.IndexFlatL2(embedding_dimension)  # Base index with L2 (Euclidean) distance
vector_db = faiss.IndexIDMap(flat_index)  # Index that allows adding vectors with specific IDs

# Function to add embeddings to the vector database
def add_embeddings_to_db(index, post_id, embeddings):
    # FAISS requires embeddings to be float32
    embeddings = embeddings.astype("float32")
    post_ids = torch.tensor([post_id], dtype=torch.int64)  # Convert post ID to int64 for FAISS

    # Add embeddings to the index with associated post IDs
    index.add_with_ids(embeddings, post_ids.numpy())

# Fetch data from WordPress
api_url = 'https://techcrunch.com/wp-json/wp/v2/posts?_fields=id,title,content'  # The URL for WordPress API
posts = get_wordpress_content(api_url)

# Process each post to generate embeddings and update the vector database
for post in posts:
    content_text = get_post_content(post)  # Extract content
    embeddings = text_to_embeddings(content_text)  # Generate embeddings from text
    add_embeddings_to_db(vector_db, post['id'], embeddings)  # Add to the vector database
