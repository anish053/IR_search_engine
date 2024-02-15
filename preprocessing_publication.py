import pandas as pd
import re
#preprocessing the text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

df = pd.read_csv('publications.csv')
def extract_authors(authors_string):
    # Use regular expression to find names between single quotes
    authors_list = re.findall(r"'([^']*)'", authors_string)
    return authors_list

df['Authors'] = df['Authors'].apply(extract_authors)

df.to_csv('postprocessing_publications.csv',index=False)
