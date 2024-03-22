from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
import streamlit as st
import json as json
from sentence_transformers import SentenceTransformer
import couchbase.search as search
from couchbase.options import SearchOptions
from couchbase.vector_search import VectorQuery, VectorSearch

model = SentenceTransformer('all-MiniLM-L6-v2')


def connect_to_capella():
    cluster = Cluster('couchbases://cb.tyueipwlkadlrkli.cloud.couchbase.com',
                      ClusterOptions(PasswordAuthenticator('vijay', 'Pa55w0rd$')))
    bucket = cluster.bucket('movie')
    return bucket


def insert_into_capella(movie_arr, bucket):
    for item in movie_arr:
        key = item['title']
        item['vector'] = vectorize_text(item['description'])
        bucket.default_collection().upsert(key, item)
    st.success(f"Loaded {len(movie_arr)} sample movies into the database.")


def load_sample_data():
    with open('/Users/vijaymuthukrishna/PycharmProjects/pythonProject/src/MovieSample.json', 'r') as sample_data:
        movie_arr = json.load(sample_data)
    return movie_arr


def vectorize_text(text):
    return model.encode(text).tolist()


def search_movie(bucket):
    st.title("Movie Search App Powered by Vector Search")
    query = st.text_input("Enter search terms related to the movie:")
    if query:
        query_vector = vectorize_text(query)
        results = perform_vector_search(bucket, query_vector)
        if results:
            for result in results:
                print(result)
                title = result.fields['title']
                description = result.fields['description']
                st.subheader(title, divider='rainbow')
                st.write(f"Description: {description}")


def perform_vector_search(bucket, query_vector):
    search_index = 'movie-search-vector'
    search_req = search.SearchRequest.create(search.MatchNoneQuery()).with_vector_search(
        VectorSearch.from_vector_query(
            VectorQuery('vector', query_vector, num_candidates=5)
        )
    )
    result = bucket.default_scope().search(search_index, search_req, SearchOptions(fields=['title', 'description']))
    return result
