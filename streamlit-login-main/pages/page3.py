from dotenv import load_dotenv
import os
from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser
from PyPDF2 import PdfReader
import streamlit as st 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain_community.callbacks.manager import get_openai_callback
import langchain
from navigation import make_sidebar

langchain.verbose = False
make_sidebar()
#load env variable
load_dotenv()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

#process text from pdf
def process_text(text):
    #split text into chunks using langchain
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,
        chunk_overlap=200,
        length_function =len
        )
    
    chunks = text_splitter.split_text(text)
    
    #convert chunks of text into embeddings to form a knowledge base
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    
    knowledge_base=FAISS.from_texts(chunks, embeddings)
    
    return knowledge_base

def app():
    st.title("Chat with PDF")
    
    pdf_docs = st.file_uploader("Upload your PDF File here", type="pdf")
    
    if pdf_docs is not None:
        pdf_reader = PdfReader(pdf_docs)
        
        #store the pdf text in a var
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text()
            
        #create a knowledge base object
        
        KnowledgeBase = process_text(text)
        
        query = st.text_input("Ask your question about your PDF ...")
        cancel_button = st.button('Cancel')
        if cancel_button:
            st.stop()
            
        if query :
            docs =KnowledgeBase.similarity_search(query)
            
            llm = OpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"))
            
            chain = load_qa_chain(llm, chain_type="stuff")
            
            with get_openai_callback() as cost:
                response = chain.invoke(input ={"question": query, "input_documents":docs})
                print(cost)  
                
                st.write(response["output_text"])
                    
                
if __name__ == "__main__":
    app()
    
    