from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate 
from vec_db_helper import doc
import os

os.environ['HUGGINGFACEHUB_API_TOKEN']="YOUR HUGGINGFACEHUB API"
llm = HuggingFaceHub(repo_id='gpt2', model_kwargs={'temperature': 0.1, 'max_length': 200})
docsearch = doc()

def build_prompt():
    template = """You are a helpful AI assistant with expertise in restaurants. You can answer questions related to restaurants and dining from the information i provided.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Question: {context}

    Answer: <bot>: """

    prompt = PromptTemplate(template=template, input_variables=["context"])
    return prompt

def chain(inp: str):
    global llm, docsearch
    prompt_template=build_prompt()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(search_kwargs={"k": 1}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template},
    )

    result = qa_chain(inp)
    result_string=result["result"]
    if "ส" or "า" in result_string:     
        return str(result['source_documents'][0])
    else:
        return result_string


