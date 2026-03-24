#  Construction Marketplace AI Assistant (Mini RAG)

**Live Demo:** [Click here to view the deployed application](https://2gppc3u39hmwrptappppfeol.streamlit.app)

This repository contains a Retrieval-Augmented Generation (RAG) pipeline built for a construction marketplace. The AI assistant answers user questions regarding internal policies, FAQs, and specifications by retrieving relevant information from official documents and strictly grounding its responses in that context

##  How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Faizzyyy13/construction_rag_assiss.git
   cd construction_rag_assiss
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Add ur documents**
   Ensure the required PDF documents (doc1.pdf, doc2.pdf, doc3.pdf) are placed in the root directory of the project.
4. **Set up API KEY**
   Create a .streamlit/secrets.toml file in the root directory and add your OpenRouter API key:
   ```Ini,TOML
   OPENROUTER_API_KEY = "your_api_key_here"
5. ** Run streamlit app**
      ```bash
   streamlit run app.py

Architecture & Technical Choices
1. Embedding Model
Model Used: all-MiniLM-L6-v2 (via sentence-transformers)

Why: This is a highly efficient, lightweight open-source embedding model. It is exceptionally fast for local execution while maintaining high accuracy for semantic search tasks, making it ideal for a small-scale document retrieval system.

2. Large Language Model (LLM)
Model Used: OpenRouter Dynamic Free Router (openrouter/free)

Why: OpenRouter provides a seamless API to access powerful, open-weights models for free. Using the dynamic free router ensures the application always has access to an online, highly capable instruct-tuned model to generate coherent text that strictly adheres to system prompts.

3. Document Chunking & Retrieval
Chunking Strategy: Documents are parsed using pdfplumber to extract raw text. The text is then divided into fixed-size chunks of 500 words with a 50-word overlap. The overlap ensures that context isn't lost if a relevant concept spans across the boundary of two chunks.

Retrieval Implementation: The chunks are converted into vector embeddings and indexed locally using FAISS (Facebook AI Similarity Search) utilizing IndexFlatL2. When a user submits a query, it is embedded using the same model, and FAISS performs a cosine-similarity (L2 distance) search to retrieve the top-K most relevant chunks.

4. Enforcing Grounding & Preventing Hallucinations
Grounding is strictly enforced through prompt engineering. The retrieved document chunks are injected directly into the LLM's system prompt along with explicit constraints:

The model is instructed to act as an AI assistant for a construction marketplace.

It is explicitly commanded to answer using ONLY the provided context.

It is instructed to reply with "I don't have enough information to answer that" if the answer cannot be found in the retrieved chunks, effectively neutralizing the risk of hallucination.

🔎 Transparency
The user interface is designed for explainability. Every time an answer is generated, the frontend explicitly displays both the final generated answer and the exact retrieved context (document chunks) that the LLM used to formulate its response.

🏆 Quality Analysis (Bonus Evaluation)
To evaluate the system's performance, a test suite of 12 questions was created based on the internal documents. These questions test factual retrieval, synthesis, and the system's ability to refuse unanswerable questions.

Test Questions
Direct Retrieval (Factual)

1. How many critical checkpoints are included in Indecimal's quality assurance system?
2. What are the four stages involved in the partner onboarding process?
3. What types of maintenance are covered under the Zero Cost Maintenance Program?
4. How does the escrow-based payment model work?
5. What is the estimated timeline for home financing confirmation and disbursal?

Synthesis & Process
6. What factors affect construction project delays?
7. What operational mechanisms does Indecimal use to enforce its Zero-Tolerance Policy on Construction Delays?
8. What are the 10 stages of the customer journey?
9. How does the company attempt to reduce hidden surprises in pricing?

Boundary Testing (Anti-Hallucination)
10. Does Indecimal build commercial office spaces? (Expected: I don't have enough information)
11. Which specific brands of cement and steel does Indecimal use? (Expected: I don't have enough information)
12. What is the exact interest rate for the home financing support? (Expected: I don't have enough information)

Evaluation Findings
Relevance of Retrieved Chunks: The all-MiniLM-L6-v2 embedding model combined with FAISS performs exceptionally well. For highly specific queries, the system consistently ranks the exact relevant document chunk as the top result.

Presence of Hallucinations: The prompt engineering successfully constrains the LLM. When asked the boundary test questions (Questions 10-12), the model correctly outputs that it does not have enough information, rather than fabricating plausible-sounding general construction facts.

Completeness and Clarity: The LLM effectively translates the raw, bulleted markdown from the retrieved chunks into natural, easy-to-read conversational answers without losing critical details.
