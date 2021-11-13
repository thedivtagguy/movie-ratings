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



## License 

This data belongs to [Common Sense Media](commonsensemedia.org) and should not be used for any commercial and/or non-academic purposes. If you make use of this dataset either as a whole or create a visualization based on this data, it is necessary to upload it with the following attribution: 

Copyright (c) 2021 Common Sense Media

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/thedivtagguy/movie-ratings">Common Sense Media Dataset</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/thedivtagguy/">Aman Bhargava</a> is licensed under <a href="http://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"></a></p>

