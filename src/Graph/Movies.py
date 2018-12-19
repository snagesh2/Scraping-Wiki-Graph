import json
import ast


class Movies:

    def __init__(self, name, release_yr, gross, actors):
        self.name = name
        self.release_yr = release_yr
        self.gross = gross
        self.actors = actors

    def info(self):
        """
        Class Movies creates movies for the graph
        :return: A movie datatype structure
        """
        ret = {'Name': self.name, 'Release Year': self.release_yr, 'Box office': self.gross, 'Actors': self.actors}
        return ast.literal_eval(json.dumps(ret))