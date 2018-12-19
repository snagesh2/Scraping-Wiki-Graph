import json
import ast


class Edges:
    def __init__(self, actor, movie, weight):
        self.actor = actor
        self.movie = movie
        self.weight = weight

    def info(self):
        """
        Class Edges creates edges for the graph
        :return: An edge datatype structure
        """
        ret = {'Actor': self.actor, 'Movie': self.movie, 'Weight': self.weight}
        return ast.literal_eval(json.dumps(ret))