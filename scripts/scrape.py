import bs4 as bs4
import requests
import pandas as pd
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

def get_ratings(string):
    """
    Find and return the ratings and the explanations
    """
    message = soup.find("div", {"id": string}).find("p").text
    # Clean up the message
    message = clean(message)
    rating = soup.find("div", {"id": string}).find("div", {"class": "content-grid-rating"})
    rating = str(rating.attrs['class'][1])
    rating = string_to_int(rating)
    return rating, message


def scrape_movie(url):
    movie_data = {}
    movie_id = url
    movie_url = "https://www.commonsensemedia.org/movie-reviews" + "/" + str(movie_id)
    response = requests.get(movie_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # get the movie data
    movie_name = soup.find("div", {"class": "panel-pane pane-node-title csm_movie"}).find("h1").text
    print("Scrapping: {movie} ...".format(movie=movie_name))
    movie_data[movie_name] = {}
    movie_data[movie_name]["url"] = movie_id

    # Parents and Kids Say
    parents_say = soup.find("div", {"class": "user-review-statistics adult"}).text
    # Pattern to keep [\d]+\+ as string
    parents_say = string_to_int(parents_say)
    movie_data[movie_name]["parents_say"] = parents_say

    kids_say = soup.find("div", {"class": "user-review-statistics child"}).text
    kids_say = string_to_int(kids_say)
    movie_data[movie_name]["kids_say"] = kids_say

    # Get ul inside div with class "product-subtitle csm_movie"
    info = soup.find("div", {"class": "product-subtitle csm_movie"}).find("ul")
    # First list item is rating
    rating = info.find("li").text
    movie_data[movie_name]["mppa_rating"] = rating
    movie_data[movie_name]["year"] = info.find_all("li")[1].text

    runtime = string_to_int(info.find_all("li")[2].text)
    movie_data[movie_name]["runtime"] = runtime


    details = soup.find("ul", {"id": "review-product-details-list"})

    # Get the genres
    movie_data[movie_name]["genres"] = details.find_all("li")[4].find("a").text
    movie_data[movie_name]["topics"] = details.find_all("li")[5].find("a").text
    movie_data[movie_name]["rating_explanation"] = details.find_all("li")[9].find("a").text

    # Get the rating categories 

    # Positive Messages
    positive = get_ratings("content-grid-item-message")

    movie_data[movie_name]["positive_rating"] = positive[0]
    movie_data[movie_name]["positive_text"] = positive[1]

    # Role Models
    role_models = get_ratings("content-grid-item-role_model")

    movie_data[movie_name]["role_models_rating"] = role_models[0]
    movie_data[movie_name]["role_models_text"] = role_models[1]

    # Diversity
    diversity = get_ratings("content-grid-item-diversity")
    movie_data[movie_name]["diversity_rating"] = diversity[0]
    movie_data[movie_name]["diversity_text"] = diversity[1]

    # Violence
    violence = get_ratings("content-grid-item-violence")
    movie_data[movie_name]["violence_rating"] = violence[0]
    movie_data[movie_name]["violence_text"] = violence[1]

    # Sexual Content
    sexual_content = get_ratings("content-grid-item-sex")
    movie_data[movie_name]["sex_rating"] = sexual_content[0]
    movie_data[movie_name]["sex_text"] = sexual_content[1]

    # Language 
    language = get_ratings("content-grid-item-language")
    movie_data[movie_name]["language_rating"] = language[0]
    movie_data[movie_name]["language_text"] = language[1]

    # Consumerism
    consumerism = get_ratings("content-grid-item-consumerism")
    movie_data[movie_name]["consumerism_rating"] = consumerism[0]
    movie_data[movie_name]["consumerism_text"] = consumerism[1]

    # Drug Use
    drug_use = get_ratings("content-grid-item-drugs")
    movie_data[movie_name]["drugs_rating"] = drug_use[0]
    movie_data[movie_name]["drugs_text"] = drug_use[1]

    print("-"*20)
    return movie_data
