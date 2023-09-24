import os
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from pprint import pprint
import numpy as np

CHROMA_PERSIST_DIR = "./chroma"
CHROMA_COLLECTION_NAME = "kdh-bot"


def delete_all():
    db = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=OpenAIEmbeddings(),
        collection_name=CHROMA_COLLECTION_NAME,
    )
    db.delete_collection()


def split_markdown(documents):
    headers_to_split_on = [
        ('#', 'service'),
        ("##", "header"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    return np.array([markdown_splitter.split_text(doc.page_content) for doc in documents]).flatten()


def split_by_chunk(documents):
    text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=10)  # 문구에 대한 분포도를 기준으로 chunk_size를 잡자
    return text_splitter.split_documents(documents)


def load_documents_from_file(file_path):
    documents = TextLoader(file_path).load()
    markdown_docs = split_markdown(documents)
    docs = split_by_chunk(markdown_docs)
    print(docs, end='\n\n\n')
    return docs


def save(documents):
    Chroma.from_documents(
        documents,
        OpenAIEmbeddings(),
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    print('db success')


def save_embedding_from_file(file_path):
    docs = load_documents_from_file(file_path)
    save(docs)


def save_embeddings_from_dir(dir_path):
    failed_files = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)

                try:
                    save_embedding_from_file(file_path)
                    print("SUCCESS: ", file_path)
                except Exception as e:
                    print("FAILED: ", file_path + f"by({e})")
                    failed_files.append(file_path)


def search(query, size):
    db = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=OpenAIEmbeddings(),
        collection_name=CHROMA_COLLECTION_NAME,
    )
    docs = db.similarity_search(query=query, k=size)
    pprint(docs)
    return docs


def init_db():
    delete_all()
    save_embeddings_from_dir('./markdown_data')


# if __name__ == "__main__":
#     init_db()
    # search('카카오 싱크')
    # db = Chroma(
    #     persist_directory=CHROMA_PERSIST_DIR,
    #     embedding_function=OpenAIEmbeddings(),
    #     collection_name=CHROMA_COLLECTION_NAME,
    # )
    # _retriever = db.as_retriever()
    # print(_retriever.get_relevant_documents('카카오 싱크 과정 예시'))
