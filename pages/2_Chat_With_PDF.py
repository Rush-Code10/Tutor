import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from _htmlTemplates import css, bot_template, user_template
from langchain_community.chat_models import ChatOllama

st.set_page_config(
    page_title="Chat With PDF",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    
    llm = ChatOllama(model = "qwen2:0.5b", temperature = "0.5")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    st.header("Chat With PDF", divider="grey", anchor=False)
    
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    user_question = st.text_input("Ask away: ")
    if user_question:
        handle_userinput(user_question)
    
    # st.write(user_template, unsafe_allow_html=True)
    # st.write(bot_template, unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your documents: ")
        pdf_docs = st.file_uploader("Upload your PDFs", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                # Get raw text
                raw_text = get_pdf_text(pdf_docs)

                # Get text chunks
                text_chunks = get_text_chunks(raw_text)

                # Create vector store
                vectorstore = get_vectorstore(text_chunks)

                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

                


if __name__ == '__main__':
    main()
