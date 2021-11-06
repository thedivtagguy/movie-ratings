import requests
import json
import os
import tinycss
import pandas as pd
import bs4 as bs4
import re


def string_to_int(string):
    """
    Find and return the number in the string of
    """
    return int(re.findall("\d+", string)[0])

def clean(string):
    """
    Clean up the string
    """
    string = string.replace("\n", " ")
    string = string.replace("\t", " ")
    string = string.replace("\xa0", " ")
    return string

def get_ratings(string, soup):
    """
    Find and return the ratings and the explanations
    """
    soup = soup 
    message = soup.find("div", {"id": string}).find("p").text
    # Clean up the message
    message = clean(message)
    rating = soup.find("div", {"id": string}).find("div", {"class": "content-grid-rating"})
    rating = str(rating.attrs['class'][1])
    rating = string_to_int(rating)
    return rating, message


def scrape_movie(url):
    """
    Get movie data from the url
    """
    movie_data = {}
    movie_id = url
    movie_url = "https://www.commonsensemedia.org" + str(movie_id)
    response = requests.get(movie_url)
    print(response, movie_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # get the movie data
    movie_name = soup.find("div", {"class": "panel-pane pane-node-title csm_movie"}).find("h1").find("div", {"class" : "stat-wrapper age"}).text
    print("Scrapping: {movie} ...".format(movie=movie_name))
    
    movie_data[movie_name] = {}
    movie_data[movie_name]["url"] = movie_id

    # Parents and Kids Say
    try:
        parents_say = soup.find("div", {"class": "user-review-statistics adult"}).find("div", {"class" : "stat-wrapper age"}).text
        # Pattern to keep [\d]+\+ as string
        parents_say = string_to_int(parents_say)
        movie_data[movie_name]["parents_say"] = parents_say
    except Exception as e:
        movie_data[movie_name]["parents_say"] = None
        print("Error in: {movie} for Parents Recommended Age \n{e}".format(movie=movie_name, e=e))
    
    try:
        kids_say = soup.find("div", {"class": "user-review-statistics child"}).text
        kids_say = string_to_int(kids_say)
        movie_data[movie_name]["kids_say"] = kids_say
    except Exception as e:
        movie_data[movie_name]["kids_say"] = None
        print("Error in: {movie} for Kids Recommended Age \n{e}".format(movie=movie_name, e = e))
    

    try:
        # From application/ld+json, get the sameAs
        imdb = soup.find("script", {"type": "application/ld+json"}).text
        imdb = json.loads(imdb)
        imdb = imdb["itemReviewed"]["sameAs"]
    except Exception as e:
        imdb = None
        print("Error in: {movie} for IMDb link \n {e}".format(movie=movie_name, e=e))
    movie_data[movie_name]["imdb"] = imdb


    try:
        # Positive Messages
        positive = get_ratings("content-grid-item-message", soup)
        movie_data[movie_name]["positive_rating"] = positive[0]
        movie_data[movie_name]["positive_text"] = positive[1]
    except Exception as e:
        movie_data[movie_name]["positive_rating"] = None
        movie_data[movie_name]["positive_text"] = None
        print("Error in: {movie} for positive messages \n {e}".format(movie=movie_name, e=e))
    
    try:
        # Role Models
        role_models = get_ratings("content-grid-item-role_model", soup)
        movie_data[movie_name]["role_models_rating"] = role_models[0]
        movie_data[movie_name]["role_models_text"] = role_models[1]
    except Exception as e:
        movie_data[movie_name]["role_models_rating"] = None
        movie_data[movie_name]["role_models_text"] = None
        print("Error in: {movie} for role models \n {e}".format(movie=movie_name, e=e))
    
    try:
        # Diversity
        diversity = get_ratings("content-grid-item-diversity", soup)
        movie_data[movie_name]["diversity_rating"] = diversity[0]
        movie_data[movie_name]["diversity_text"] = diversity[1]
    except Exception as e:
        movie_data[movie_name]["diversity_rating"] = None
        movie_data[movie_name]["diversity_text"] = None
        print("Error in: {movie} for diversity \n {e}".format(movie=movie_name, e=e))
    
    try:
        # Violence
        violence = get_ratings("content-grid-item-violence", soup)
        movie_data[movie_name]["violence_rating"] = violence[0]
        movie_data[movie_name]["violence_text"] = violence[1]
    except Exception as e:
        movie_data[movie_name]["violence_rating"] = None
        movie_data[movie_name]["violence_text"] = None
        print("Error in: {movie} for violence \n {e}".format(movie=movie_name, e=e))
    
    try:
        # Sexual Content
        sexual_content = get_ratings("content-grid-item-sex", soup)
        movie_data[movie_name]["sex_rating"] = sexual_content[0]
        movie_data[movie_name]["sex_text"] = sexual_content[1]
    except Exception as e:
        movie_data[movie_name]["sex_rating"] = None
        movie_data[movie_name]["sex_text"] = None
        print("Error in: {movie} for sex \n {e}".format(movie=movie_name, e=e))

    try:
        # Language 
        language = get_ratings("content-grid-item-language", soup)
        movie_data[movie_name]["language_rating"] = language[0]
        movie_data[movie_name]["language_text"] = language[1]
    except Exception as e:
        movie_data[movie_name]["language_rating"] = None
        movie_data[movie_name]["language_text"] = None
        print("Error in: {movie} for language \n {e}".format(movie=movie_name, e=e))

    try:
        # Consumerism
        consumerism = get_ratings("content-grid-item-consumerism", soup)
        movie_data[movie_name]["consumerism_rating"] = consumerism[0]
        movie_data[movie_name]["consumerism_text"] = consumerism[1]
    except Exception as e:
        movie_data[movie_name]["consumerism_rating"] = None 
        movie_data[movie_name]["consumerism_text"] = None
        print("Error in: {movie} for consumerism \n {e}".format(movie=movie_name, e=e))

    
    try:
        # Drug Use
        drug_use = get_ratings("content-grid-item-drugs", soup)
        movie_data[movie_name]["drugs_rating"] = drug_use[0]
        movie_data[movie_name]["drugs_text"] = drug_use[1]
    except Exception as e:
        movie_data[movie_name]["drugs_rating"] = None
        movie_data[movie_name]["drugs_text"] = None
        print("Error in: {movie} for drug use \n {e}".format(movie=movie_name, e=e))

    print("-"*20)
    return movie_data






# Read in movie csv without headers
movies = pd.read_csv("data/movie_list.csv",  encoding='latin-1', header=None)


# Choose two rows to scrape randomly
movies = movies.sample(n=2)
movie_data = {}

# For each movie, get the information
for index, row in movies.iterrows():
    movie_id = row[1]
    print("Scrapping: {movie} ...".format(movie=movie_id))
    # Scrape and add to dictionary
    movie_data.update(scrape_movie(movie_id))

# Dictionary to DataFrame
df = pd.DataFrame.from_dict(movie_data, orient='index')

# df to csv
df.to_csv("data/movie_data.csv")