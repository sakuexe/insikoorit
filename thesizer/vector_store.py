from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders import BSHTMLLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pypdf.errors import PyPdfError
# stdlib
from glob import glob
import pathlib


async def load_text(file_path: str) -> list[Document] | None:
    """Loads text documents (.txt) asynchronously from a passed file_path."""
    assert file_path != ""
    assert pathlib.Path(file_path).suffix == ".txt"

    try:
        loader = TextLoader(file_path)
        return await loader.aload()
    except UnicodeError or RuntimeError as err:
        print(f"could not load file: {file_path}")
        print(f"error: {err}")


# https://python.langchain.com/docs/how_to/document_loader_markdown/
async def load_markdown(file_path: str) -> list[Document] | None:
    """Loads markdown files asynchronously from a passed file_path."""
    assert file_path != ""
    assert pathlib.Path(file_path).suffix == ".md"

    try:
        # use the mode elements to keep metadata about if the information is
        # a paragraph, link or a heading for example
        loader = UnstructuredMarkdownLoader(file_path, mode="elements")
        return await loader.aload()
    except UnicodeError or RuntimeError as err:
        print(f"could not load file: {file_path}")
        print(f"error: {err}")


# https://python.langchain.com/docs/how_to/document_loader_pdf/
async def load_pdf(file_path: str) -> list[Document] | None:
    """Loads pdf documents (.pdf) asynchronously from a passed file_path."""
    assert file_path != ""
    assert pathlib.Path(file_path).suffix == ".pdf"

    loader = PyPDFLoader(file_path)
    try:
        return await loader.aload()
    except PyPdfError as err:
        print(f"could not read file: {file_path}")
        print(f"error: {err}")


async def load_html(file_path: str) -> list[Document]:
    """Loads html documents (.html) asynchronously from a passed file_path."""
    assert file_path != ""
    assert pathlib.Path(file_path).suffix == ".html" or ".htm"

    loader = BSHTMLLoader(file_path)
    return await loader.aload()


# hold all of the loader functions for easy 0(1) fetching
LOADER_MAP = {
    ".pdf": load_pdf,
    ".html": load_html,
    ".htm": load_html,
    ".txt": load_text,
    ".md": load_markdown,
}


# https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/vectorstore/
async def get_document_database(
    data_folder="learning_material/*/*",
    embedding_model="BAAI/bge-base-en-v1.5",
    chunk_size=1028, chunk_overlap=0,
) -> VectorStore:

    # get all the filepaths of the learning materials
    files = glob(data_folder)

    all_docs = []
    for file_path in files:
        extension = pathlib.Path(file_path).suffix
        if not extension:
            print(f"{file_path} is a folder, skipping")
            continue

        load_fn = LOADER_MAP.get(extension)
        if not load_fn:
            print(f"no document loader for file extension '{extension}'")
            print(f"file {file_path} will be skipped")
            continue

        # load the document with a filetype specific loader
        result_documents = await load_fn(file_path)

        if not result_documents:
            print(f"file {file_path} does not include any content, skipping")
            continue

        all_docs.extend(result_documents)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunked_docs = splitter.split_documents(all_docs)

    return await FAISS.afrom_documents(
        chunked_docs,
        HuggingFaceEmbeddings(model_name=embedding_model)
    )
