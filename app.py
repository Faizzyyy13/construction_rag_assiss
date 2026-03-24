import streamlit as st
import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer


# ==========================================
# 1. Configuration & Setup
# ==========================================
# Replace with your OpenRouter API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Using a free open-source embedding model [cite: 5]
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

embedder = load_embedding_model()

# ==========================================
# 2. Document Processing (Chunking & Embedding)
# ==========================================
# You must chunk the documents into meaningful segments[cite: 11].
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

import gdown
import pdfplumber
import os

@st.cache_data
def load_real_documents():
    # The names of the files you just uploaded to Colab
    file_names = ['doc1.pdf', 'doc2.pdf', 'doc3.pdf']
    
    docs = []
    for file_name in file_names:
        # Check if file exists to prevent crashing
        if not os.path.exists(file_name):
            st.warning(f"Missing file: {file_name}. Please upload it to Colab!")
            continue
            
        # Extract text from the PDF
        text = ""
        try:
            with pdfplumber.open(file_name) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            if text.strip():
                docs.append(text)
        except Exception as e:
            st.error(f"Error reading {file_name}: {e}")
            
    return docs

# Load the documents
with st.spinner("Processing official documents..."):
    documents = load_real_documents()

# We need to ensure documents were actually loaded before proceeding to embed
if not documents:
    st.error("No documents loaded. Please check your PDF uploads.")
    st.stop() # Stops the app from running further and hitting the IndexError

# Proceed to chunking and embedding only if we have text
chunks = []
for doc in documents:
    chunks.extend(chunk_text(doc))

embeddings = embedder.encode(chunks)

# ==========================================
# 3. Vector Indexing and Retrieval
# ==========================================
# Build a local vector index over the document embeddings[cite: 13].
# A local vector store is sufficient; managed services are not required[cite: 6].
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension) # FAISS implementation [cite: 5]
index.add(np.array(embeddings).astype('float32'))

def retrieve_context(query, k=2):
    """Retrieve the top-k most relevant document chunks[cite: 14]."""
    query_embedding = embedder.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]

# ==========================================
# 4. Grounded Answer Generation
# ==========================================
def generate_answer(query, context_chunks):
    """Use an LLM to generate answers only from retrieved chunks[cite: 7, 15]."""
    context_text = "\n\n".join(context_chunks)
    
    # Prompt explicitly instructs LLM to avoid hallucinations and unsupported claims[cite: 16].
    prompt = f"""
    You are an AI assistant for a construction marketplace. 
    Answer the user's question using ONLY the provided context below. 
    If the answer is not contained in the context, say "I don't have enough information to answer that."
    
    Context:
    {context_text}
    
    Question: {query}
    """

    # Using a free OpenRouter LLM [cite: 8]
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openrouter/free", # Example free model
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error {response.status_code}: {response.text}"

# ==========================================
# 5. Chatbot Interface (Custom Frontend)
# ==========================================
st.title("🏗️ Construction Marketplace AI Assistant")
st.write("Ask questions about construction policies, FAQs, and specs!")

user_query = st.text_input("Enter your query:")

if st.button("Submit"):
    if user_query:
        with st.spinner("Retrieving information..."):
            # Retrieve
            retrieved_chunks = retrieve_context(user_query)
            
            # Generate
            answer = generate_answer(user_query, retrieved_chunks)
            
            # Transparency: Clearly display the final generated answer[cite: 8].
            st.subheader("Answer")
            st.write(answer)
            
            # Transparency: Clearly display the retrieved document chunks used as context.
            st.subheader("Retrieved Context Used")
            for i, chunk in enumerate(retrieved_chunks):
                st.info(f"**Chunk {i+1}:** {chunk}")
