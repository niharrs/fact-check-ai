from dotenv import find_dotenv, load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
from numpy import dot
from numpy.linalg import norm

load_dotenv(find_dotenv())
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def get_embeddings():
    embeddings = embeddings_model.embed_documents(
        [
            "Hi there! My name is Niharika. I am from Gurgaon",
            "What's your name?",
            "Niharika is not from Gurgaon.",
            "Niharika is from India."
        ]
    )
    return embeddings

def embedding_query():
    embedded_query = embeddings_model.embed_query("Niharika is from Gurgaon.")
    return embedded_query

def calculate_similarity(X, Y):
    cos_sim = dot(X, Y)/(norm(X)*norm(Y))
    return cos_sim


embeddings = get_embeddings()
embeddingquery = embedding_query()

rows = len(embeddings)
columns = len(embeddings[0])

print("Cosine Similarity: ", calculate_similarity(embeddings, embeddingquery))

