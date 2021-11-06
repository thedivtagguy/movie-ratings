# Scraping movie ratings and reviews from Common Sense Media

Script for scraping movie ratings and reviews from Common Sense Media written with Python using BeautifulSoup.

To run the script, you need to install the following packages:
1. BeautifulSoup
2. requests
3. pandas

Run the script with the following command:
```py
python scrape_movies_list.py
# Outputs a list of movies with their URLs
```

To scrape movie details, run the following command:
```py
python get_data.py
# Outputs a dataset of movie details
```

This will create a csv file with the following columns:
1. Movie Title
2. Movie URL
3. Movie Rating
4. Movie Year
5. Movie Genres
4. Movie Reviews by Available Categories. This includes: Positive Messages, Role Models, Consumerism, and Other. If unavailable, the cell will be empty.

This will scrape *all* the movie details and save them in a csv file, which is around 11,000 movies. There is currently no support for setting a limit for the number of movies to scrape.

For research and educational purposes only.

