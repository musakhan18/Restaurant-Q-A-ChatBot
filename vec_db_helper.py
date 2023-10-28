import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = None
docsearch = None

def doc():
    global embeddings, docsearch

    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')

    if docsearch is None:
        pinecone.init(      
            api_key='YOUR PINECONE API',      
            environment='gcp-starter'      
        )      
        index = pinecone.Index('restaurant-sugg')
        docsearch = Pinecone.from_existing_index(index_name="restaurant-sugg", embedding=embeddings)

    return docsearch
