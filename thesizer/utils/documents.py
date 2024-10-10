from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, VectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from glob import glob


def get_document_database(
    data_folder="learning_material/**",
    embedding_model="BAAI/bge-base-en-v1.5",
) -> VectorStore:

    md_files = glob(data_folder)

    all_docs = []
    for file_path in md_files:
        loader = TextLoader(file_path)
        docs = loader.load()
        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=30)
    chunked_docs = splitter.split_documents(all_docs)

    return FAISS.from_documents(
        chunked_docs,
        HuggingFaceEmbeddings(model_name=embedding_model)
    )
