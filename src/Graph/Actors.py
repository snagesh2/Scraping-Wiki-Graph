import json
import ast


class Actors:
    def __init__(self, name, age, movies):
        self.age = age
        self.movies = movies
        self.name = name

    def info(self):
        """
        Class Actors creates movies for the graph
        :return: An actor datatype structure
        """
        ret = {'Name': self.name, 'Age': self.age, 'Movies': self.movies}
        return ast.literal_eval(json.dumps(ret))