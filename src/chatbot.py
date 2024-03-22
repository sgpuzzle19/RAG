import numpy
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import CohereEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os
import dotenv
dotenv.load_dotenv()
import warnings
warnings.filterwarnings("ignore")
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatCohere
from langchain.chains.question_answering import load_qa_chain


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


script = None
def generate_output(question: str) -> str:
    template_text = """I am a chatbot
    {context}
    {chat_history}
    Human:{question}
    Chatbot:"""

    global script

    cohere_api_key = os.getenv("COHERE_API_KEY")
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=cohere_api_key)

    all_docs = list(process_doc_files(SUPPORT_DOC_FOLDER_PATH).values())
    docs_search  = Chroma.from_texts(all_docs, embeddings)
    similar_docs = docs_search.similarity_search(question, k = 1)


    if script is None:
        llm = ChatCohere(cohere_api_key=cohere_api_key)
        prompt = PromptTemplate(input_variables=["context", "chat_history", "question"], template=template_text)
        Memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")
        script = load_qa_chain(llm=llm, chain_type="stuff", memory= Memory, prompt=prompt)
        
    input = {"input_documents": similar_docs, "question": question}
    output = script(input, return_only_outputs=True)
    print(script.memory.buffer)

    return output['output_text']
    