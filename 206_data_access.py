###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import unittest
import tweepy
import requests
import json
import twitter_info
import random
import re
import sqlite3

# Begin filling in instructions....

# Grab authentification info from twitter_info.py file
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Get twitter data in JSON format and store in variable api
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Make cache file for Twitter data
CACHE_FNAME = "twitter_and_movie_cache.json"

# Set up caching process
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# Define function get_twitter_search_data that takes in a movie tile and returns data about ten tweets that mention that movie and caches this data if not cached already
def get_twitter_user_data(movie_title):
	unique_identifier = "twitter_{}".format(movie_title) 

	if unique_identifier in CACHE_DICTION:
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		twitter_results = api.statuses_lookup(movie_title)

		CACHE_DICTION[unique_identifier] = twitter_results
		
		f = open(CACHE_FNAME,'w')
		f.write(json.dumps(CACHE_DICTION)) 
		f.close()

	tweets = [] 
	for tweet in twitter_results:
		tweets.append(tweet)
	return tweets[:10]

twitter_data = get_twitter_user_data("Trainwreck movie")

# Write function get_omdb data that takes in a movie title and returns all of the data about the movie and caches the data if it hasn't been cached already
# List of three movie titles to get data for
movie_list = ["Inception", "Trainwreck", "Brooklyn"]

def get_omdb_data(movie_list):
	for movie in movie_list:
		unique_identifier = "omdb_{}".format(movie)

		if unique_identifier in CACHE_DICTION:
			omdb_results = CACHE_DICTION[unique_identifier]
		else:
			for title in movie_list:
				omdb_results = requests.get("http://www.omdbapi.com/?t="+title)

			CACHE_DICTION[unique_identifier] = omdb_results
		
			f = open(CACHE_FNAME,'w')
			f.write(json.dumps(CACHE_DICTION)) 
			f.close()

		movie_info = []
		for movie in omdb_results:
			movie_info.append(movie)
		return movie_info

movie_data = get_omdb_data(movie_list)

# Define Movie class
	# Constructor: accepts a movie dictionary

	# Instance variables: title, director, IMDB rating, list of actors, number of languages

	# Define __str__ method that doesn't take any parameters

	# Define num_languages method that doesn't take any parameters

# Define function movie_title_list that returns a list of 3 movie titles from OMDB


# Make a query request to OMDB with each of the three terms from the list that returns all of the dictionaries in a variable called movie_dictionaries


# Define a function movie_list that takes in movie_dictionaries and returns a list of instances of the movie class


# Define a function three_movie_list that returns a list of three movies in the variable three_movies


# Define a function movie_director that takes in the list three_movies and returns the variable movie_director that holds a list of the directors of those three movies


# Define a function related_user that returns the username of any Twitter user mentioned in the previous Tweets accessed


# Create a database that is a table of Tweets from the Twitter database
	# Rows: tweet text, tweet ID, user who posted the tweet, movie search tweet came from, number favorites, number retweets

# Create a database that is a table of Users from the Twitter database
	# Rows: User ID, user screen name, number of favorites


# Create a database that is a table of Movies from the OMDB database
	# Rows: ID, title, director, number of languages, IMDB, top billed

# Load the data into the database

# Make a query called lang_num that accesses the IMDB rating of movies that have more than 1 language


# Make a query called rating_favorites that accesses the IMDB rating and number of times a tweet about a movie has been favorited so I'll be joining the Tweets table and Movies table. 


# Write the data to a text file

'''
# Put your tests here, with any edits you now need from when you turned them in with your project plan.
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


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)

if __name__ == "__main__":
    unittest.main(verbosity=2)
'''