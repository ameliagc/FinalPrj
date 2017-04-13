## Your name: Amelia Cacchione
## The option you've chosen: project 2

# Put import statements you expect to need here!

import unittest
import tweepy
import requests
import json
import twitter_info
import random
import re
import sqlite3


# Write your test cases here.

class TestCases(unittest.TestCase):
	# tests the type of the title instance variable from the Movie class
	def test_class_type_title(self):
		movie = Movie({title: "test", director: "me", rating: 8, actors: ["actor1", "actor2"], num_lang: 10})
		self.assertEqual(movie.title, type(str))
	# tests the type of the director instance variable from the Movie class
	def test_class_type_director(self):
		movie = Movie({title: "test", director: "me", rating: 8, actors: ["actor1", "actor2"], num_lang: 10})
		self.assertEqual(movie.director, type(str))
	# tests the type of the rating instance variable from the Movie class
	def test_class_type_rating(self):
		movie = Movie({title: "test", director: "me", rating: 8, actors: ["actor1", "actor2"], num_lang: 10})
		self.assertEqual(movie.rating, type(int))
	# tests the type of the actors instance variable from the Movie class
	def test_class_type_actors(self):
		movie = Movie({title: "test", director: "me", rating: 8, actors: ["actor1", "actor2"], num_lang: 10})
		self.assertEqual(movie.actors, type(list))
	# tests the type of the rating instance variable from the Movie class
	def test_class_type_num_lang(self):
		movie = Movie({title: "test", director: "me", rating: 8, actors: ["actor1", "actor2"], num_lang: 10})
		self.assertEqual(movie.num_lang, type(int))
	# tests if the variable ratings_for_multiple_langs that holds the return from query 1 holds an integer
	def test_query_1_return(self):
		self.assertEqual(ratings_for_multiple_langs, type(int))
	# tests if the variable rating_vs_favs that holds the return from query 2 holds a dictionary
	def test_query_2_return(self):
		self.assertEqual(rating_vs_favs, type(dict))
	# tests if the title instance variable is correct for the created Movie class
	def test_movie_title_return(self):
		movie = Movie({title: "test", director: "me", rating: 8, actors: ["actor1", "actor2"], num_lang: 10})
		self.assertEqual(movie.title, "test")



## Remember to invoke all your tests...

if __name__ == "__main__":
    unittest.main(verbosity=2)