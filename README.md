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
