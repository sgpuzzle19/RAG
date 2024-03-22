import numpy
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import CohereEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.memory import ConversationBufferMemory
import os
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatCohere
import dotenv
dotenv.load_dotenv()
import warnings
warnings.filterwarnings("ignore")


openai_api_key = os.getenv("OPENAI_API_KEY")
# embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
cohere_api_key = os.getenv("COHERE_API_KEY")
def chatbot(question:str = "how to troubleshoot slow internet issue according to documents provided?"):
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=cohere_api_key)
    #load the vector store chroma from a directory
    docs_search = Chroma(persist_directory="E:\RWTH\Master thesis_Liz\chatbot\llm_to_revenue-main\customer_support_bot\vector_store", embedding_function=embeddings)


    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    retriever = docs_search.as_retriever(search_kwargs={"k": 4})
    llm = ChatCohere(cohere_api_key=cohere_api_key)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    

    answer = qa.run(question)
    return answer