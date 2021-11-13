import csv
import os
import re
import pandas as pd
import nltk


df = pd.read_csv('data/movie_data.csv')

# Trim whitespace from all rows
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df.keys()

# Count the number of rows with missing values
df.isnull().sum()
# Empty cells are replaced with NaN
df.fillna(value=pd.np.nan, inplace=True)
# Remove rows with more than 40% of columns with NaN
df.dropna(thresh=len(df.columns) * 0.1, inplace=True)

# Fill parents_say and kids_say missing values with 0
df['parents_say'] = df['parents_say'].fillna(0)
df['kids_say'] = df['kids_say'].fillna(0)

def age_difference(string):
    """
    Count the age difference between parents_say 
    and kids_say columns where genre column has string
    """
    mean = df[(df['genres'].str.contains(string, na=False))]['parents_say'].mean() - df[(df['genres'].str.contains(string, na=False))]['kids_say'].mean()
    # Which mean is greater?
    greater= 'kids' if mean < 0 else 'parents'
    median = df[(df['genres'].str.contains(string, na=False))]['parents_say'].median() - df[(df['genres'].str.contains(string, na=False))]['kids_say'].median()
    result = {'mean': mean, 
              'median': median,
              'greater': greater}
    return result

age_difference('Horror')

# Select movie, url, and genres columns
dput = df[['movie', 'url', 'genres']].head(5)

# Count number of horror movies
dput['genres'] = dput['genres'].str.split(',')
df['genres'] = df['genres'].str.split(',')
df = df.explode('genres')

# Count movies where  genre is horror
count_horror = df[df['genres'].str.contains('Horror', na=False)].movie.count()

# Daatframe to SQL database
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)
df.to_sql('movie_data', con=engine, if_exists='replace', index=False)

# Choose random language_text from movie_data
df2 = pd.read_sql_table('movie_data', con=engine)
df2['language_text']

# Select words from movie_data in language_text of the regex pattern [a-zA-Z]-*[a-zA-Z]
query = """
        SELECT * FROM language_text
        WHERE language_text REGEXP '[a-zA-Z]-*[a-zA-Z]'
        """
df3 = pd.read_sql_query(query, con=engine)
df3