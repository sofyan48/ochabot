# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores.faiss import FAISS
# from langchain_core.vectorstores import VectorStoreRetriever


# class Retriever():
#     def __init__(self, embedding_model="sentence-transformers/all-mpnet-base-v2") -> None:
#         self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    
#     def build(self, data, name="model", chunk=200):
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk)
#         all_splits = text_splitter.split_documents(data)
#         faiss_retriever = FAISS.from_documents(documents=all_splits, embedding=self.embeddings)
#         faiss_retriever.save_local(name)

#     def retriever(self, topK: int, folder_path: str) -> VectorStoreRetriever:
#         local = FAISS.load_local(folder_path, self.embeddings, allow_dangerous_deserialization=True)
#         return local.as_retriever(
#             search_kwargs={
#                 "k": topK
#             }
#         )