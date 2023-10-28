from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
import pinecone

def initialize_pinecone():
    pinecone.init(api_key='YOUR PINECONE API', environment='gcp-starter')
    return pinecone.Index('restaurant-sugg')

def load_embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')

def create_question_list(data, embeddings):
    question_list = []
    for _, row in data.iterrows():
        question_list.append(
            (
                str(row['id']),
                embeddings.embed_query(row['name']),
                {
                    'id': int(row['id']),
                    'text': row['name']
                }
            )
        )
    return question_list

def main():
    pinecone_index = initialize_pinecone()
    embeddings_model = load_embeddings()

    data_path = "DataSet\DataSet.csv"
    data = pd.read_csv(data_path)

    questions = create_question_list(data, embeddings_model)
    pinecone_index.upsert(vectors=questions)

if __name__ == "__main__":
    main()
