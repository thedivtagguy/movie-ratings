import requests
import bs4 as bs

# Listing page for movies
url = 'https://www.commonsensemedia.org/movie-reviews?page={page_no}'
total_page = 3

movies = {}
# Do not exceed the request limit
# Go to each page and scrape the data
for page_no in range(1, total_page + 1):
    print('Scraping page {}'.format(page_no))
    page_url = url.format(page_no=page_no)
    page_response = requests.get(page_url)
    page_content = page_response.content
    page_soup = bs.BeautifulSoup(page_content, 'lxml')

    # Scrape the movie title and link
    movie_list = page_soup.find_all('div', class_='views-row')
    for movie in movie_list:
        title = movie.find('div', class_='result-title').text
        link = movie.find('a')['href']
        print('Title: {}'.format(title))
        print('Link: {}'.format(link))
        print('-' * 20)
        # Add to the dictionary
        movies[title] = link

# Save movie_list to csv
import csv
with open('data/movie_list.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in movies.items():
        writer.writerow([key, value])
