import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


# Function to preprocess text
def preprocess_text(text):
    text = text.lower()  # Convert text to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text


# Function to preprocess authors
def preprocess_authors(authors):
    # Remove surrounding brackets and single quotes
    authors = authors.strip()[1:-1]
    # Split by single quote and strip whitespace
    authors_list = [author.strip() for author in authors.split('\'')]
    # Remove empty strings
    authors_list = [author for author in authors_list if author]
    return authors_list


# Function to create a dictionary mapping authors' last names to profile links
def create_author_profile_mapping(authors_data):
    author_profile_mapping = {}
    for index, row in authors_data.iterrows():
        last_name = row['New Column'].split(',')[0].strip()  # Extract last name
        author_profile_mapping[last_name] = row['Person Link']
    return author_profile_mapping


# Function to perform ranked retrieval
def ranked_retrieval(query, documents, links, authors, author_profile_mapping):
    # Preprocess query
    query = preprocess_text(query)

    # TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Transform the query to TF-IDF vector
    query_vector = tfidf_vectorizer.transform([query])

    # Calculate cosine similarity between query and documents
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Sort the indices by similarity score
    sorted_indices = cosine_similarities.argsort()[::-1]

    # Retrieve ranked documents, links, and authors with positive similarity scores
    ranked_results = []
    for i in sorted_indices:
        if cosine_similarities[i] > 0:
            document = documents[i]
            link = links[i]
            score = cosine_similarities[i]
            document_authors = preprocess_authors(authors[i])  # Preprocess authors

            # Match authors' last names with profile links
            author_profile_links = []
            for author in document_authors:
                last_name = author.split(',')[0].strip()  # Extract last name
                profile_link = author_profile_mapping.get(last_name)
                if profile_link:
                    author_profile_links.append((author, profile_link))
                else:
                    author_profile_links.append((author, None))

            ranked_results.append((document, link, score, author_profile_links))

    return ranked_results


# Load preprocessed DataFrame from the first CSV file
file_path = 'postprocessing_publications.csv'  # Adjust the file path accordingly
df = pd.read_csv(file_path)

# Load authors data from the second CSV file
authors_file_path = 'persons.csv'  # Adjust the file path accordingly
authors_data = pd.read_csv(authors_file_path)

# Create a dictionary mapping authors' last names to profile links
author_profile_mapping = create_author_profile_mapping(authors_data)

# Streamlit app
st.title('Ranked Retrieval with TF-IDF')

# Input text box for query
query = st.text_input('Enter your query:', '')

# Button to perform retrieval
if st.button('Retrieve'):
    # Perform ranked retrieval
    ranked_results = ranked_retrieval(query, df['Title'], df['Publication Link'], df['Authors'], author_profile_mapping)

    # Display results
    st.subheader('Ranked Results:')
    if ranked_results:
        for i, (document, link, score, authors) in enumerate(ranked_results):
            st.write(f'{i + 1}. Document: {document}, Score: {score:.4f}')
            st.markdown(f'[Link to publication]({link})')
            st.write('Authors:')
            for author, profile_link in authors:
                if profile_link:
                    st.markdown(f'[Profile Link]({profile_link}) {author}')
                else:
                    st.write(author)
            st.write('---')  # Add a separator between results
    else:
        st.write('No results found.')
