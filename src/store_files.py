import numpy
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import CohereEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.memory import ConversationBufferMemory
import os
import dotenv
dotenv.load_dotenv()
import warnings
warnings.filterwarnings("ignore")


SUPPORT_DOC_FOLDER_PATH = 'E:\RWTH\Master thesis_Liz\chatbot\llm_to_revenue-main\customer_support_bot\support_docs' #add folder path

def process_doc_files(SUPPORT_DOC_FOLDER_PATH):
    doc_dict = {}
    # to check if folder exists
    if not os.path.exists(SUPPORT_DOC_FOLDER_PATH):
        return doc_dict #only return when folder does not exits
    #list of files in the folder
    file_list = os.listdir(SUPPORT_DOC_FOLDER_PATH)

    for filename in file_list:
        if filename.endswith(".txt"):
            #create a full path to the filename
            file_path = os.path.join(SUPPORT_DOC_FOLDER_PATH, filename)  

            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
            # Store the content in the dictionary with the filename as the key
            doc_dict[filename] = file_content 
    
    return doc_dict


cohere_api_key = os.getenv("COHERE_API_KEY")
embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=cohere_api_key)
all_docs = list(process_doc_files(SUPPORT_DOC_FOLDER_PATH).values())
docs_search  = Chroma.from_texts(all_docs, embeddings)
#save the vector store in a directory
docs_search._persist_directory = "E:\RWTH\Master thesis_Liz\chatbot\llm_to_revenue-main\customer_support_bot\vector_store"
#save the vector store in a directory
docs_search.persist()
