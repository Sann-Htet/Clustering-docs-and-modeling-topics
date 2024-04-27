from fastapi import FastAPI
from haystack.nodes import EmbeddingRetriever
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

TOPIC_MODEL = "deep-learning-analytics/automatic-title-generation"
EMBEDDINGS_MODEL = "sentence-transformers/all-MiniLM-L12-v2"

class Data(BaseModel):
    ids: list
    docs: list
    threshold: float = 0.5

class Description(BaseModel):
    description: list

app = FastAPI()


def generate_topic(document: list) -> list:
    pipe = pipeline("text2text-generation", model=TOPIC_MODEL)
    return pipe(document)


def cluster_docs(documents: list, threshold: float) -> list:

    retriever = EmbeddingRetriever(
      embedding_model=EMBEDDINGS_MODEL, use_gpu=True,
      )

    document_embeddings = retriever.embed_queries(documents)

    similarity_matrix = cosine_similarity(document_embeddings)

    clusters = []
    visited_documents = set()

    for doc_index, _ in enumerate(documents):
        if doc_index in visited_documents:
            continue

        cluster = [doc_index]
        visited_documents.add(doc_index)

        similar_documents = similarity_matrix[doc_index]
        for target_index, similarity_score in enumerate(similar_documents):
            if target_index not in visited_documents and similarity_score >= threshold:
                cluster.append(target_index)
                visited_documents.add(target_index)

        if cluster:
            clusters.append(cluster)

    return clusters


@app.post("/cluster_and_generate_topics")
def cluster_and_generate_topics(data: Data) -> dict:

    requests = data.docs
    request_ids = data.ids

    clusters = cluster_docs(requests, data.threshold)

    cluster_topics = {}
    joined_cluster_docs = []
    for cluster_id, cluster in enumerate(clusters):
        cluster_documents = [requests[i] for i in cluster]
        joined_text = " ".join(cluster_documents)
        joined_cluster_docs.append(joined_text)
        cluster_topics[cluster_id] = {
            "cluster_documents": cluster_documents,
            "request_ids": [request_ids[i] for i in cluster],
        }

    generated_topics = generate_topic(joined_cluster_docs)
    for i, cluster_id in enumerate(cluster_topics):
        cluster_topics[cluster_id]["generated_topic"] = generated_topics[i]["generated_text"]

    return cluster_topics


@app.post("/cluster_documents")
def cluster_documents(data: Data) -> dict:

    documents = data.docs
    document_ids = data.ids

    clusters = cluster_docs(documents, data.threshold)

    cluster_documents = {}
    for cluster_id, cluster in enumerate(clusters):
        docs = [documents[i] for i in cluster]
        cluster_documents[cluster_id] = {
            "cluster_documents": docs,
            "document_ids": [document_ids[i] for i in cluster],
        }

    return cluster_documents

@app.post("/generate_topics")
def generate_topics(data: Description) -> dict:
    description = data.description
    topics = generate_topic(description)

    return {
        "generated_topics": [topic["generated_text"] for topic in topics],
    }
