"""
Testing Graph and Queries
@author: snagesh2
"""
import unittest

from src.Graph.Graph2 import Graph2
from src.Graph.Actors import Actors
from src.Graph.Edges import Edges
from src.Graph.Movies import Movies

TESTFILE = Graph2.FILE


class GraphTest(unittest.TestCase):
    def testGraphExtract(self):
        """
        Tests extraction from Json file and structure of Graph
        """
        graph = Graph2()
        graph.parseFile(TESTFILE)

if __name__ == "__main__":
    #unittest.main()
    graph = Graph2()
    graph.parseFile(TESTFILE)
    tmp_movie = Movies("BlahBlah", 2010, 121890708, ["Robert Redford","Freeman Blah"])
    tmp_actor = Actors("Freeman Blah", 7 , ["BlahBlah"])
    graph.add_movie(tmp_movie)
    graph.add_actor(tmp_actor)
    graph.add_edge(Edges(tmp_actor.name, tmp_movie.name, 222759050.0))
    graph.get_movies_for_actor("Faye Dunaway")
    graph.get_movies_for_year(2002)
    graph.get_movie_actors_for_year(2002)
    graph.get_actors_for_movie("Message in a Bottle")
    graph.get_movie_gross("The Thomas Crown Affair")
    graph.find_highest_grossing_actors(5)
    graph.find_oldest_actors(2)
    graph.find_actor_hub(5)
    graph.send_actors_to_json()
    graph.send_edges_to_json()
    graph.send_movies_to_json()
    graph.age_group_analysis()
    graph.plot_actor_hub()
