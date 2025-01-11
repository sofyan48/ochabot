from langchain_community.document_loaders import (
        CSVLoader, 
        WebBaseLoader, 
        PyPDFLoader,
        JSONLoader
    )

def csv_loader(csv_path: str):
    loader = CSVLoader(file_path=csv_path, encoding="utf-8")
    return loader.load()

def web_loader(url):
    loader = WebBaseLoader(url=url)
    return loader.load()

def pdf_loader(pdf_path: str):
    loader = PyPDFLoader(file_path=pdf_path)
    return loader.load()

def json_loader(json_path: str):
    loader = JSONLoader(
        file_path=json_path
    )
    return loader.load()