"""
This is the Graph library
@author: snagesh2
"""
import heapq
import json

import numpy

from src.Graph.Actors import Actors
from src.Graph.Edges import Edges
from src.Graph.Movies import Movies
import matplotlib.pyplot as plt


class Graph2:
    """
    The class contains graph library, with vertices and edges
    This also contains functions for the queries
    """

    FILE = "../Scraping/data_given.json"

    def __init__(self):
        self.movies = {}
        self.actors = {}
        self.edges = {}

    def parseFile(self, filename):
        """
        Parses through the .json file to create the graph
        :param filename: the name of the JSON format file
        :return: A graph structure with with vertices and edges
        """
        with open(filename, 'r') as json_data:
            data = json.load(json_data)
        for d in data:
            for either in d:
                if d[either]['json_class']=='Movie':
                    # print("==================================Movies=======================================")
                    i = d[either]['name']
                    release_yr = d[either]['year']
                    gross = d[either]['box_office']
                    actors = d[either]['actors']
                    self.add_movie(Movies(i, release_yr, gross, actors))

                else:
                    # print("==================================Actors=======================================")
                    i = d[either]['name']
                    age = d[either]['age']
                    movies = d[either]['movies']
                    self.add_actor(Actors(i, age, movies))
        # print("==================================Edges=======================================")
        for each_actor in self.actors:
            movies = self.actors[each_actor].info()['Movies']
            for m in movies:
                for each_movie in self.movies:
                    if each_movie == m:
                        self.movies[each_movie].info()['Release Year']
                        gross_m = self.movies[each_movie].info()['Box office']
                        if(gross_m < 9999):
                            gross_m *= 1000000
                        number_actors_m = len(self.movies[each_movie].info()['Actors'])
                        rank = 0;
                        for a in range(number_actors_m):
                            if self.movies[each_movie].info()['Actors'][a] == i:
                                rank = a;
                        if number_actors_m != 0:
                            weight = gross_m * (number_actors_m - rank) / number_actors_m
                        else:
                            weight = gross_m
                        self.add_edge(Edges(each_actor, each_movie, weight))

    def add_movie(self, movie_data):
        """
        Adds a movie type vertex to Graph
        :param movie_data: the data to add. It is of type Movies.
        :return: the updated graph
        """
        if movie_data not in self.movies:
            self.movies[movie_data.name] = movie_data
            # print(movie_data.info())

    def add_actor(self, actor_data):
        """
        Adds an actor type vertex to Graph
        :param actor_data: the data to add. It is of type Actors.
        :return: the updated graph
        """
        if actor_data not in self.actors:
            self.actors[actor_data.name] = actor_data
            # print(actor_data.info())

    def add_edge(self, edge_data):
        """
         Adds an Edges type edge to Graph
         :param edge_data: the data to add. It is of type Edges.
         :return: the updated graph
         """
        if edge_data.actor not in self.edges:
            self.edges[edge_data.movie] = edge_data
        # print(edge_data.info())

    def get_movies_for_actor(self, actor_name):
        """
        Gets movies an actor has acted in
        :param actor_name: Name of actor
        :return: Prints the names of movies
        """
        print(" ")
        print(actor_name, "has played in -----> ", end="")
        for each_actor in self.actors:
            if self.actors[each_actor].info()['Name'] == actor_name:
                print( ', '.join(self.actors[each_actor].info()['Movies']))

    def get_movies_for_year(self,year):
        """
        Gets movies for a given year
        :param year: Year of release
        :return: Prints movies of that year
        """
        print(" ")
        print("In the year",year,"-----> ", end="")
        movies_list = []
        for each_movie in self.movies:
            if self.movies[each_movie].info()['Release Year'] == year:
                movies_list.append( self.movies[each_movie].info()['Name'])
        print(', '.join(movies_list), " were released")

    def get_movie_gross(self,movie_name):
        """
        Gets Box Office gross
        :param movie_name: Name of movie
        :return: Prints the amount the movie grossed at Box Office
        """
        print(" ")
        print("The movie",movie_name," grossed -----> ", end="")
        for each_movie in self.movies:
            if self.movies[each_movie].info()['Name'] == movie_name:
                print( self.movies[each_movie].info()['Box office'], "$ at the Box Office")

    def get_actors_for_movie(self,movie_name):
        """
        List which actors worked in a movie
        :param movie_name: Name of movie
        :return: Prints actors who worked in a movie
        """
        print(" ")
        print("The movie",movie_name," had actors -----> ", end="")
        for each_movie in self.movies:
            if self.movies[each_movie].info()['Name'] == movie_name:
                print( self.movies[each_movie].info()['Actors'])

    def get_movie_actors_for_year(self,year):
        """
        List all the movie actors for a given year
        :param year: Year of release
        :return: Prints actors active during that year
        """
        print(" ")
        print("In the year",year,"-----> ", end="")
        movies_list = []
        for each_movie in self.movies:
            if self.movies[each_movie].info()['Release Year'] == year:
                if isinstance(self.movies[each_movie].info()['Actors'], list):
                        movies_list.append( self.movies[each_movie].info()['Actors'])
                else:
                    tmp = []
                    tmp.append(self.movies[each_movie].info()['Actors'])
                    movies_list.append(tmp)
        flat_list = [item for sublist in movies_list for item in sublist]
        print(', '.join(list(set(flat_list))), " acted in movies")

    def find_highest_grossing_actors(self, x):
        """
        List the top X actors with the most total grossing value
        :param x: Number of actors to return
        :return: the top X actors with the most total grossing value
        """
        print(" ")
        weight_list = []
        actor_list = []
        movie_list = []
        for each_edge in self.edges:
            weight_list.append(self.edges[each_edge].info()['Weight'])
            actor_list.append(self.edges[each_edge].info()['Actor'])
            movie_list.append(self.edges[each_edge].info()['Movie'])
        a = numpy.array(weight_list)
        index_list = heapq.nlargest(x, range(len(a)), a.take)
        for i in index_list:
            print(actor_list[i],"for role in",movie_list[i], "earned", weight_list[i],"$")

    def find_oldest_actors(self,x):
        """
        List the oldest X actors
        :param x: Number of actors to return
        :return: the oldest X actors
        """
        print(" ")
        print("The oldest actors in this database are:")
        age_list = []
        actor_list = []
        for each_actor in self.actors:
            age_list.append(self.actors[each_actor].info()['Age'])
            actor_list.append(self.actors[each_actor].info()['Name'])
        a = numpy.array(age_list)
        index_list = heapq.nlargest(x, range(len(a)), a.take)
        for i in index_list:
            print(actor_list[i]," is ",age_list[i], "years old")

    def find_actor_hub(self,x):
        print(" ")
        score_list = []
        movie_list = []
        actor_list = []
        for each_actor in self.actors:
            #print(each_actor)
            movie_list = self.actors[each_actor].info()['Movies']
            actor_list.append(self.actors[each_actor].info()['Name'])

            #print(movie_list)
            score = 0
            for m in movie_list:
                for each_movie in self.movies:
                    if each_movie == m:
                        score += len(self.movies[m].info()['Actors'])
            score_list.append(score)
        a = numpy.array(score_list)
        index_list = heapq.nlargest(x, range(len(a)), a.take)
        for i in index_list:
            print(actor_list[i]," has connections with",score_list[i],"other actors")

    def plot_actor_hub(self):
        score_list = []
        movie_list = []
        actor_list = []
        for each_actor in self.actors:
            #print(each_actor)
            movie_list = self.actors[each_actor].info()['Movies']
            actor_list.append(self.actors[each_actor].info()['Name'])

            #print(movie_list)
            score = 0
            for m in movie_list:
                for each_movie in self.movies:
                    if each_movie == m:
                        score += len(self.movies[m].info()['Actors'])
            score_list.append(score)
        a = numpy.array(score_list)
        index_list = heapq.nlargest(50, range(len(a)), a.take)
        objects = []
        performance = []
        for i in index_list:
            objects.append(actor_list[i])
            performance.append(score_list[i])
        y_pos = numpy.arange(len(objects))
        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects, fontsize= 6)
        plt.ylabel('Actors')
        plt.title('The hub of the actors- Top 50')
        plt.show()

    def send_movies_to_json(self):
        jsonMovies = []
        for each_movie in self.movies:
            jsonMovies.append(self.movies[each_movie].info())
        jsonFile = {"Movies": jsonMovies}
        with open('movies.json', 'w') as outfile:
            json.dump(jsonFile, outfile)

    def send_actors_to_json(self):
        jsonActors = []
        for each_actor in self.actors:
            jsonActors.append(self.actors[each_actor].info())

        jsonFile = {"Actors": jsonActors}
        with open('actors.json', 'w') as outfile:
            json.dump(jsonFile, outfile)

    def send_edges_to_json(self):
        jsonEdges = []
        for each_edge in self.edges:
            jsonEdges.append(self.edges[each_edge].info())
        jsonFile = {"Edges": jsonEdges}
        with open('edges.json', 'w') as outfile:
            json.dump(jsonFile, outfile)

    def age_group_analysis(self):
        print(" ")
        age_group_list = {'0\'s to 20\'s':0, '20\'s to 40\'s':0, '40\'s to 60\'s':0, '60\'s to 80\'s':0, '80\'s to 100\'s':0}
        gross_age_group_list = {'0\'s to 20\'s':0, '20\'s to 40\'s':0, '40\'s to 60\'s':0, '60\'s to 80\'s':0, '80\'s to 100\'s':0}
        for each_actor in self.actors:
            #print(self.actors[each_actor].info()['Age'])
            if(self.actors[each_actor].info()['Age'] > 0 and self.actors[each_actor].info()['Age'] < 20):
                movie_list = self.actors[each_actor].info()['Movies']
                score = 0
                for m in movie_list:
                    for each_movie in self.movies:
                        if each_movie == m:
                            if(self.movies[m].info()['Box office'] > 9999):
                                score += self.movies[m].info()['Box office']
                            else:
                                score += self.movies[m].info()['Box office']*1000000
                if(score == 0):
                    continue
                gross_age_group_list['0\'s to 20\'s'] += score
                age_group_list['0\'s to 20\'s'] +=1


            elif(self.actors[each_actor].info()['Age'] >= 20 and self.actors[each_actor].info()['Age'] < 40):
                movie_list = self.actors[each_actor].info()['Movies']
                score = 0
                for m in movie_list:
                    for each_movie in self.movies:
                        if each_movie == m:
                            if(self.movies[m].info()['Box office'] > 9999):
                                score += self.movies[m].info()['Box office']
                            else:
                                score += self.movies[m].info()['Box office']*1000000
                if(score == 0):
                    continue
                gross_age_group_list['20\'s to 40\'s'] += score
                age_group_list['20\'s to 40\'s'] +=1


            elif(self.actors[each_actor].info()['Age'] >= 40 and self.actors[each_actor].info()['Age'] < 60):
                movie_list = self.actors[each_actor].info()['Movies']
                score = 0
                for m in movie_list:
                    for each_movie in self.movies:
                        if each_movie == m:
                            if(self.movies[m].info()['Box office'] > 9999):
                                score += self.movies[m].info()['Box office']
                            else:
                                score += self.movies[m].info()['Box office']*1000000

                if(score == 0):
                    continue
                gross_age_group_list['40\'s to 60\'s'] += score
                age_group_list['40\'s to 60\'s'] +=1


            elif (self.actors[each_actor].info()['Age'] >= 60 and self.actors[each_actor].info()['Age'] < 80):
                movie_list = self.actors[each_actor].info()['Movies']
                score = 0
                for m in movie_list:
                    for each_movie in self.movies:
                        if each_movie == m:
                            if(self.movies[m].info()['Box office'] > 9999):
                                score += self.movies[m].info()['Box office']
                            else:
                                score += self.movies[m].info()['Box office']*1000000
                if(score == 0):
                    continue
                gross_age_group_list['60\'s to 80\'s'] += score
                age_group_list['60\'s to 80\'s'] += 1


            elif(self.actors[each_actor].info()['Age'] >= 80 and self.actors[each_actor].info()['Age'] < 100):
                movie_list = self.actors[each_actor].info()['Movies']
                score = 0
                for m in movie_list:
                    for each_movie in self.movies:
                        if each_movie == m:
                            if(self.movies[m].info()['Box office'] > 9999):
                                score += self.movies[m].info()['Box office']
                            else:
                                score += self.movies[m].info()['Box office']*1000000
                if(score == 0):
                    continue
                gross_age_group_list['80\'s to 100\'s'] += score
                age_group_list['80\'s to 100\'s'] += 1

        for i in age_group_list:
            if(age_group_list[i] == 0):
                age_group_list[i] = 1
        average_gross = dict((k, float(gross_age_group_list[k]) / age_group_list[k]) for k in gross_age_group_list)
        average_gross =dict((k,float(average_gross[k]/4000000)) for k in average_gross)
        objects = age_group_list.keys()
        performance = average_gross.values()
        y_pos = numpy.arange(len(objects))
        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects, fontsize= 9)
        plt.ylabel('Age Groups')
        plt.title('Averrage Box Office Gross (in millions)')
        plt.show()

