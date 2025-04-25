from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from typing import List
from langchain_core.documents import Document
from uuid import uuid4


# Initialize text splitter and embedding function
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)

embedding_function = MistralAIEmbeddings(model="mistral-embed", api_key="Urh4e6lzqJEDhmVwCCFQqrAYcKr7Hswz")

url="https://c27d45f7-d4dd-49c8-aa6c-0e5959d04613.europe-west3-0.gcp.cloud.qdrant.io:6333"
api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.KstcPirDYZ8chwHsc-oHoFpU8lIR73xk1Lf-2AasctA"

client = QdrantClient(url = url, api_key= api_key)
vectorstore = QdrantVectorStore(
    client=client,
    collection_name="democollection",
    embedding=embedding_function,
)


def load_and_split_document(file_path: str) -> List[Document]:
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    documents = loader.load()
    return text_splitter.split_documents(documents)

def generate_id_for_documents(documents: List[Document]) -> List[str]:
    uuids = [str(uuid4()) for _ in range(len(documents))]
    return uuids

def index_document_to_qdrant(file_path: str) -> bool:
    try:
        splits = load_and_split_document(file_path)
        file_ids = generate_id_for_documents(splits)

        print(splits)
        print(file_ids)

        # Add metadata to each split
        for split, file_id in zip(splits, file_ids):
            split.metadata['file_id'] = file_id
        vectorstore.add_documents(documents=splits, ids=file_ids)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

def delete_doc_from_qdrant(file_id: List):
    try:
        vectorstore.delete(ids=file_id)
        print(f"Deleted all documents with file_id {file_id}")
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from qdrant: {str(e)}")
        return False