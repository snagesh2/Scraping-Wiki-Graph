"""
This is the Web Scraper
@author: snagesh2
"""

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import logging
import datetime
import json
import re


def Scraper( webpage_link, jsonMovies, jsonActors):
    """
    This is the definition of a fuction that recursively calls itself to scrape data from the web.
    :param webpage_link: The link that we are opening
    :param jsonMovies: The json data that corresponds to movies
    :param jsonActors: The json data that corresponds to actors
    :return: None, but modifies dta in jsonMovies and jsonActors
    """
    print("opening link", webpage_link)
    logging.info("opening link", webpage_link)
    logging.debug("Scraping webpage ----> ", webpage_link)


    def get_actor_age(check_alive, actor_born_year):
        """
        This function gets age of actor.
        :param check_alive: This checks if actor is alive
        :param actor_born_year: The year actor was born
        :return: The age of actor
        """
        if check_alive:
            return int(datetime.date.today().year) - int(actor_born_year.contents[0].split('-')[0])

    def movie_extract(soup_find):
        """
        Extracts movie and movie links from info table
        :param soup_find: The data to extract movies from
        :return: None
        """
        movie_tmp = []
        list_raw = soup_find.find_next("ul").findAll('a', href = True)
        for l in list_raw:
            movie_tmp.append(str(l.text))
            movie_link_list.append(str("https://en.wikipedia.org" + l['href']))
        movie.append(movie_tmp)

    def actors_extract(info_table):
        """
        Extracts actors and actor links from info table
        :param info_table: The data to extract movies from
        :return: None
        """
        list_raw = info_table.findAll('th')
        for l in list_raw:
            if str(l.text) == "Starring":
                cast_find = l.next_sibling.next_sibling
                cast_find = cast_find.findAll('a')
                for link in cast_find:
                    actor_link = str("https://en.wikipedia.org" + link['href'])
                    actor_link_list.append(actor_link)
                for cast_find_head in cast_find:
                    movie_cast = cast_find_head.text
                    movie_actors.append(movie_cast)
            elif str(l.find_next('div').text) == "Release date":
                year = l.find_next('div').find_next('li').text.split('(')
                year = year[0][-5:]
                year = year[:4]
                movie_year.append(year)

            elif str(l.text) == "Box office":
                gross_amount = l.find_next('td').text.split("[")
                gross.append(str(gross_amount[0]))

    # =================================== Begin Function Code =====================================

    try:
        r = requests.get(webpage_link, timeout=10)
        r.raise_for_status()
        soup = bs(urlopen(webpage_link), "html.parser")
        soup.prettify()
    except Exception:
        return

    actors = []
    actors_age = []
    movie = []
    movie_link_list = []
    actor_link_list = []
    movies = []
    movie_year = []
    movie_actors = []
    gross = []

    # ========================================= Actor Web page =====================================

    check_actor = soup.find("table", {"class": "infobox biography vcard"})
    if check_actor:
        check_alive = False
        logging.info("Getting actor's name")
        actor_name = soup.find("h1", {"id": "firstHeading"})
        actor_name = actor_name.text
        logging.debug("Actor's name is ----> " + actor_name)
        actors.append(actor_name)
        actor_info = check_actor.find_all('th')
        for actor_info_head in actor_info:
            if actor_info_head.text == "Born":
                check_alive = True
                actor_year = soup.find("span", {"class": "bday"})
        logging.info("Calling function to calculate actor's age.")
        current_age = get_actor_age(check_alive, actor_year)
        logging.debug("Actor's age is ----> ", str(current_age))
        actors_age.append(current_age)
        check_actor_movie = soup.find("span", {"id": re.compile('.*graphy.*')})
        if check_actor_movie:
            logging.info("Extracting movies")
            movie_extract(check_actor_movie)
        else:
            logging.warning("Couldn't find Filmography")

    # ========================================= Movie Web page =====================================
    else:
        movie_info_table = soup.find("table", {"class": "infobox vevent"})
        if(movie_info_table):
            logging.info("Extracting movies")
            actors_extract(movie_info_table)
            movie_title = movie_info_table.find_next('th')
            movie_title = str(movie_title.text)
            logging.debug("The movie title for the webpage_link is: " + movie_title)
            movies.append(movie_title)
            logging.info("Getting movie's title from the webpage_link...")
        else:
            logging.warning("Couldn't find Actor Data")

    # =============================================== Json File Writing ===============================================
    movies_json = {}
    actors_json = {}

    logging.info('Preparing Json file')
    logging.debug('Preparing Json file')

    for j in range(0, len(gross)):
        movies_json[movies[j]] = {'Release Year': movie_year[j], 'Box office': gross[j], 'Actors': movie_actors}
    for j in range(0, len(actors_age)):
        actors_json[actors[j]] = {'Age': actors_age[j], 'Movies': movie}

    if bool(movies_json):
        jsonMovies.append(movies_json)
    if bool(actors_json):
        jsonActors.append(actors_json)

    logging.info('Finished preparation. Begin Next Recursive Call')
    logging.debug('Finished preparation. Begin Next Recursive Call')

    for link in movie_link_list:
        Scraper(link, jsonMovies, jsonActors)
    # for link in actor_link_list:
        # Scraper(link,jsonMovies, jsonActors)


# =========================== Calling data and Scraper function ==========================
starting_url = 'https://en.wikipedia.org/wiki/Faye_Dunaway'
jsonMovies = []
jsonActors = []
movie_count = 0
actor_count = 0
Scraper(starting_url, jsonMovies, jsonActors)
jsonFile = {"Actor": jsonActors, "Movie": jsonMovies}
with open('data.json', 'w') as outfile:
    json.dump(jsonFile, outfile)
