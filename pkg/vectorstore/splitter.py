from langchain.text_splitter import RecursiveCharacterTextSplitter  


class TextSplitter:  
    _instance = None  
    
    def __new__(cls, *args, **kwargs):    
        if cls._instance is None:    
            cls._instance = super(TextSplitter, cls).__new__(cls)    
        return cls._instance 

    @classmethod
    def text_splitter(cls, data, chunk=2000, overlap=500):
       text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk, chunk_overlap=overlap)
       return text_splitter.split_documents(data)
    