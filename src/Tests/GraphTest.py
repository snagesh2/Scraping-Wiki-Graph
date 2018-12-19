"""
Testing Graph and Queries
@author: snagesh2
"""
import unittest

from src.Graph.Graph import Graph
from src.Graph.Actors import Actors
from src.Graph.Edges import Edges
from src.Graph.Movies import Movies

TESTFILE = Graph.FILE


class GraphTest(unittest.TestCase):
    def testGraphExtract(self):
        """
        Tests extraction from Json file and structure of Graph
        """
        graph = Graph()
        graph.parseFile(TESTFILE)

    def testGraphAddActor(self):
        """
        Tests adding actor vertex
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        graph.add_actor(Actors("Freeman Blah", 80, "BlahBlah"))

    def testGraphAddMovie(self):
        """
        Tests adding movie vertex
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        graph.add_movie(Movies("BlahBlah", "1980", "$121,890,708", "Robert Redford"))


    def testGraphAddEdge(self):
        """
        Tests adding an edge
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        tmp_movie = Movies("BlahBlah", "1980", "$121,890,708", "Robert Redford")
        tmp_actor = Actors("Freeman Blah", 80, "BlahBlah")
        graph.add_movie(tmp_movie)
        graph.add_actor(tmp_actor)
        graph.add_edge(Edges( tmp_actor.name,tmp_movie.name, 222759050.0))

    def testGetMoviesForActor(self):
        """
        Tests getting films an actor has acted in
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        graph.get_movies_for_actor("Faye Dunaway")

    def testGetMoviesForYear(self):
        """
        Tests getting movies for given year
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        tmp_movie = Movies("BlahBlah", "1980", "$121,890,708", "Robert Redford")
        tmp_actor = Actors("Freeman Blah", 80, "BlahBlah")
        graph.add_movie(tmp_movie)
        graph.add_actor(tmp_actor)
        graph.add_edge(Edges( tmp_actor.name,tmp_movie.name, 222759050.0))
        graph.get_movies_for_year("1980")

    def testMovieGross(self):
        """
        Tests how much a movie grossed at Box Office
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        tmp_movie = Movies("BlahBlah", "1980", "$121,890,708", "Robert Redford")
        tmp_actor = Actors("Freeman Blah", 80, "BlahBlah")
        graph.add_movie(tmp_movie)
        graph.add_actor(tmp_actor)
        graph.add_edge(Edges( tmp_actor.name,tmp_movie.name, 222759050.0))
        graph.get_movie_gross("The Thomas Crown Affair")

    def testMovieActors(self):
        """
        Tests finding actors who acted in a given movie
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        tmp_movie = Movies("BlahBlah", "1980", "$121,890,708", "Robert Redford")
        tmp_actor = Actors("Freeman Blah", 80, "BlahBlah")
        graph.add_movie(tmp_movie)
        graph.add_actor(tmp_actor)
        graph.add_edge(Edges( tmp_actor.name,tmp_movie.name, 222759050.0))
        graph.get_actors_for_movie("The Arrangement")

    def testGetMovieActorsForYear(self):
        """
        Tests finding actors for a given year
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        tmp_movie = Movies("BlahBlah", "1980", "$121,890,708", "Robert Redford")
        tmp_actor = Actors("Freeman Blah", 80, "BlahBlah")
        graph.add_movie(tmp_movie)
        graph.add_actor(tmp_actor)
        graph.add_edge(Edges( tmp_actor.name,tmp_movie.name, 222759050.0))
        graph.get_movie_actors_for_year("1980")

    def testHighestGrossing(self):
        """
        Tests finding highest grossing X actors
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        tmp_movie = Movies("BlahBlah", "1980", "$121,890,708", "Robert Redford")
        tmp_actor = Actors("Freeman Blah", 80, "BlahBlah")
        graph.add_movie(tmp_movie)
        graph.add_actor(tmp_actor)
        graph.add_edge(Edges( tmp_actor.name,tmp_movie.name, 222759050.0))
        graph.find_highest_grossing_actors(5)

    def testOldestActors(self):
        """
        Tests finding oldest X actors
        """
        graph = Graph()
        graph.parseFile(TESTFILE)
        tmp_movie = Movies("BlahBlah", "1980", "$121,890,708", "Robert Redford")
        tmp_actor = Actors("Freeman Blah", 78, "BlahBlah")
        graph.add_movie(tmp_movie)
        graph.add_actor(tmp_actor)
        graph.add_edge(Edges( tmp_actor.name,tmp_movie.name, 222759050.0))
        graph.find_oldest_actors(2)


if __name__ == "__main__":
    #unittest.main()
    graph = Graph()
    graph.parseFile(TESTFILE)
    tmp_movie = Movies("BlahBlah", "1980", "$121,890,708", "Robert Redford")
    tmp_actor = Actors("Freeman Blah", 78 , "BlahBlah")
    graph.add_movie(tmp_movie)
    graph.add_actor(tmp_actor)
    graph.add_edge(Edges(tmp_actor.name, tmp_movie.name, 222759050.0))
    graph.get_movies_for_actor("Faye Dunaway")
    graph.get_movies_for_year("1980")
    graph.get_movie_actors_for_year("1980")
    graph.get_actors_for_movie("The Thomas Crown Affair")
    graph.get_movie_gross("The Thomas Crown Affair")
    graph.find_highest_grossing_actors(5)
    graph.find_oldest_actors(2)


