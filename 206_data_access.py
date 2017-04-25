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
CACHE_FNAME = "twitter_cache.json"

# Set up caching process for twitter_cache
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# Define function get_twitter_search_data that takes in a movie tile and returns a dictionary of data about ten tweets that mention that movie and caches this data if not cached already
def get_twitter_search_data(movie_title):
	unique_identifier = "twitter_{}".format(movie_title) 

	if unique_identifier in CACHE_DICTION:
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		twitter_results = api.search(movie_title)

		CACHE_DICTION[unique_identifier] = twitter_results
		
		f = open(CACHE_FNAME,'w')
		f.write(json.dumps(CACHE_DICTION)) 
		f.close()

	return twitter_results

# Call twitter search function on three movies
twitter_data_Inception = get_twitter_search_data("Inception movie")

twitter_data_Trainwreck = get_twitter_search_data("Trainwreck movie")

twitter_data_Brooklyn = get_twitter_search_data("Brooklyn movie")

# Put resulting tweet dictionaries in a list of 3 dictionaries
twitter_data_search_list = []
twitter_data_search_list.append(twitter_data_Inception)
twitter_data_search_list.append(twitter_data_Trainwreck)
twitter_data_search_list.append(twitter_data_Brooklyn)


# Make cache file for Twitter user data
CACHE_FNAME3 = "user_twitter_cache.json"

# Set up caching process for user_twitter_cache
try:
	cache_file3 = open(CACHE_FNAME3,'r')
	cache_contents3 = cache_file3.read()
	CACHE_DICTION3 = json.loads(cache_contents3)
except:
	CACHE_DICTION3 = {}

# Define function get_twitter_user_data that takes in a username and returns a dictionary of data about a user and caches this data if not cached already
def get_twitter_user_data(username):
	unique_identifier = "twitter_{}".format(username) 

	if unique_identifier in CACHE_DICTION3:
		twitter_results = CACHE_DICTION3[unique_identifier]
	else:
		twitter_results = api.get_user(username)

		CACHE_DICTION3[unique_identifier] = twitter_results
		
		f = open(CACHE_FNAME3,'w')
		f.write(json.dumps(CACHE_DICTION3)) 
		f.close()

	return twitter_results


# Make cache file for OMDB data
CACHE_FNAME2 = "omdb_cache.json"

# Set up caching process for omdb_cache
try:
	cache_file2 = open(CACHE_FNAME2,'r')
	cache_contents2 = cache_file2.read()
	CACHE_DICTION2 = json.loads(cache_contents2)
except:
	CACHE_DICTION2 = {}

# Write function get_omdb data that takes in a list of movie titles and returns a dictionary of all of the data about the movie movies and caches the data if it hasn't been cached already
def get_omdb_data(movie_list):
	movie_info = []
	for movie in movie_list:
		unique_identifier = "omdb_{}".format(movie)

		if unique_identifier in CACHE_DICTION2:
			movie_info.append(CACHE_DICTION2[unique_identifier])
		else:
			r = requests.get("http://www.omdbapi.com/?t="+movie)
			omdb_results = r.text

			movie_info.append(omdb_results)

			CACHE_DICTION2[unique_identifier] = omdb_results
		
			f = open(CACHE_FNAME2,'w')
			f.write(json.dumps(CACHE_DICTION2)) 
			f.close()

	return movie_info

# List of three movie titles to get data for
movie_list = ["Inception", "Trainwreck", "Brooklyn"]

# Call get OMDB data function and return list of 3 dictionaries (one for each movie in list)
movie_data = get_omdb_data(movie_list)

# Connect to database
conn = sqlite3.connect('databases.db')
cur = conn.cursor()

# Make table to hold Twitter data
cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('CREATE TABLE Tweets (tweet_id TEXT PRIMARY KEY, user_id INTEGER, tweet_text TEXT, user TEXT, retweets INTEGER, favorites INTEGER, user_mentions TEXT, movie_search TEXT)')

statement = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

# Insert cached data from twitter search function into database for each of three movies
for x in twitter_data_Inception["statuses"]:
	tweet_id = x["id_str"]
	user_id = x["user"]["id"]
	tweet_text = x["text"]
	user = x["user"]["screen_name"]
	retweets = x["retweet_count"]
	favorites = x["favorite_count"]
	user_dictionary = x["entities"]["user_mentions"]
	user_mentions = ""
	for x in user_dictionary:
		user_mentions = x["screen_name"]
	movie_search = "Inception"

	cur.execute(statement, (tweet_id, user_id, tweet_text, user, retweets, favorites, user_mentions, movie_search))

for x in twitter_data_Trainwreck["statuses"]:
	tweet_id = x["id_str"]
	user_id = x["user"]["id"]
	tweet_text = x["text"]
	user = x["user"]["screen_name"]
	retweets = x["retweet_count"]
	favorites = x["favorite_count"]
	user_dictionary = x["entities"]["user_mentions"]
	user_mentions = ""
	for x in user_dictionary:
		user_mentions = x["screen_name"]
	movie_search = "Trainwreck"

	cur.execute(statement, (tweet_id, user_id, tweet_text, user, retweets, favorites, user_mentions, movie_search))

for x in twitter_data_Brooklyn["statuses"]:
	tweet_id = x["id_str"]
	user_id = x["user"]["id"]
	tweet_text = x["text"]
	user = x["user"]["screen_name"]
	retweets = x["retweet_count"]
	user_dictionary = x["entities"]["user_mentions"]
	user_mentions = ""
	for x in user_dictionary:
		user_mentions = x["screen_name"]
	movie_search = "Brooklyn"

	cur.execute(statement, (tweet_id, user_id, tweet_text, user, retweets, favorites, user_mentions, movie_search))

conn.commit()

# Query to access users mentioned in tweets from Tweets database, store in user_neighborhood
user_neighborhood = []
query = "SELECT user_mentions FROM Tweets WHERE user_mentions > 0"
cur.execute(query)
temp_tup = cur.fetchall()
user_neighborhood = [x[0] for x in temp_tup]

# Query to access users who posted tweets in Tweets database, add to user_neighborhood
query1 = "SELECT user FROM Tweets"
cur.execute(query1)
temp_tup1 = cur.fetchall()
user_neighborhood += [x[0] for x in temp_tup1]

# Make dictionary user_neighborhood_dict with keys of users that map to a dictionary of data about the user
user_neighborhood_dict = {}
for user in user_neighborhood:
	user_neighborhood_dict[user] = get_twitter_user_data(user)

# Make tabel to hold User data with columns
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('CREATE TABLE Users (user_id INTEGER PRIMARY KEY, screen_name TEXT, favorites INTEGER)')

# Insert cached data from twitter user function into database for each of the users in user_neighborhood_dict
statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?)'

for key in user_neighborhood_dict:
	temp_user_dict = {}
	temp_user_dict = user_neighborhood_dict[key]
	user_id = temp_user_dict["id"]
	screen_name = temp_user_dict["name"]
	favorites = temp_user_dict["favourites_count"]

	cur.execute(statement, (user_id, screen_name, favorites))

conn.commit()

# Make table to hold OMDB data with columns: title, director (will probably add to this later)
cur.execute('DROP TABLE IF EXISTS OMDB')
cur.execute('CREATE TABLE OMDB (movie_id TEXT PRIMARY KEY, title TEXT, director TEXT, language INTEGER, imdb_rating TEXT, actor TEXT)')

# Insert cached data from omdb function into database for each of three movies
statement = 'INSERT OR IGNORE INTO OMDB VALUES (?, ?, ?, ?, ?, ?)'

for x in movie_data:
	x = json.loads(x)
	movie_id = x["imdbID"]
	title = x["Title"]
	director = x["Director"]

	lang_string = x["Language"]
	split_lang = lang_string.split(",")
	language = len(split_lang)

	imdb_rating = x["imdbRating"]

	actor_string = x["Actors"]
	split_actor = actor_string.split(",")
	actor = split_actor[0]

	cur.execute(statement, (movie_id, title, director, language, imdb_rating, actor))

conn.commit()


# Define Movie class
class Movie(object):
	# Constructor: accepts a movie dictionary
	def __init__(self, movie_dict):
		self.movie_dict = json.loads(movie_dict)
		self.title = self.movie_dict["Title"]
		self.director = self.movie_dict["Director"]
		self.imdb_rating = self.movie_dict["imdbRating"]
		self.actor_list = self.movie_dict["Actors"]
		self.num_lang = self.movie_dict["Language"]

	# Define __str__ method
	def __str__(self):
		return "{} was directed by {} and has an IMDB rating of {}. The actors include {}. The following languages are spoken in the movie: {}.".format(self.title, self.director, self.imdb_rating, self.actor_list, self.num_lang)
	
	# Define function that uses the imdb_rating to return true is a movie is "good," meaning it has a rating of 5 or higher
	def is_movie_good(self):
		if float(self.imdb_rating) > 5:
			return True
		else:
			return False

# Query to see if users who get more favorites
query_faves = "SELECT Users.favorites, Tweets.favorites FROM Tweets INNER JOIN Users on Tweets.user_id = Users.user_id"
cur.execute(query_faves)
faves_relationship = cur.fetchall()

# Query to see which movies got the most favorites in tweets about them
query_popularity = "SELECT OMDB.title, Tweets.favorites FROM Tweets INNER JOIN OMDB on Tweets.movie_search = OMDB.title"
cur.execute(query_popularity)
popularity_relationship = cur.fetchall()

# Variables hold number of favorites from each tweet about each movie
inception_faves = []
trainwreck_faves = []
brooklyn_faves= []
for tup in popularity_relationship:
	if tup[0] == "Inception":
		inception_faves.append(tup[1])
	elif tup[0] == "Trainwreck":
		trainwreck_faves.append(tup[1])
	else:
		brooklyn_faves.append(tup[1])

# Variables hold the addition of the number of favorites for tweets about each movie
inception_total	= 0
trainwreck_total = 0
brooklyn_total = 0
for num in inception_faves:
	inception_total += num
for num in trainwreck_faves:
	trainwreck_total += num
for num in brooklyn_faves:
	brooklyn_total += num

# Create text file to write data to
f = open("summary_stats.txt", "w+")

# Write summary statistics to text file
f.write("Here are the summary stats for Tweets about the following movies:\n")
for movie in movie_list:
	if movie == "Brooklyn":
		f.write("and "+movie+"\n")
	else:
		f.write(movie+", ")
f.write("\n")

f.write("Do users who favorite more tweets get more favorites on their tweets?\n")

f.write("Number of tweets a user has favorited vs. Number of favorites a user got on a tweet:\n")
for pair in faves_relationship:
	f.write(str(pair[0])+" vs. "+str(pair[1])+"\n")
f.write("There appears to be no relationship between how many tweets a user favorites and how many favorites a user gets on their tweet.")
f.write("\n")
f.write("\n")

f.write("Which movie got the most total favorites on tweets that mentioned the movie?\n")
f.write("Inception: "+str(inception_total)+"\n")
f.write("Trainwreck: "+str(trainwreck_total)+"\n")
f.write("Brooklyn: "+str(brooklyn_total)+"\n")

f.write("\n")
f.write("\n")

f.write("Whether or not a movie is good or bad is determined by if it has more or less than 5 points on IMDB. Here are the results: ")
f.write("\n")
inception_instance = Movie(movie_data[0])
if(inception_instance.is_movie_good()):
	f.write("Inception is a good movie.\n")
trainwreck_instance = Movie(movie_data[1])
if(trainwreck_instance.is_movie_good()):
	f.write("Trainwreck is a good movie.\n")
brooklyn_instance = Movie(movie_data[2])
if(brooklyn_instance.is_movie_good()):
	f.write("Brooklyn is a good movie.\n")

f.close()


# Put your tests here, with any edits you now need from when you turned them in with your project plan.
class TestCases(unittest.TestCase):
	# tests the type of the title instance variable from the Movie class
	def test_class_type_title(self):
		test_movie = Movie(movie_data[0])
		self.assertEqual(type(test_movie.title), str)
	# tests the type of the director instance variable from the Movie class
	def test_class_type_director(self):
		test_movie = Movie(movie_data[0])
		self.assertEqual(type(test_movie.director), str)
	# tests the type of the rating instance variable from the Movie class
	def test_class_type_rating(self):
		test_movie = Movie(movie_data[0])
		self.assertEqual(type(test_movie.imdb_rating), str)
	# tests the type of the actors instance variable from the Movie class
	def test_class_type_actors(self):
		test_movie = Movie(movie_data[0])
		self.assertEqual(type(test_movie.actor_list), str)
	# tests the type of the rating instance variable from the Movie class
	def test_class_type_num_lang(self):
		test_movie = Movie(movie_data[0])
		self.assertEqual(type(test_movie.num_lang), str)
	# tests if the query for movie favorites returns a list
	def test_query_faves_return(self):
		self.assertEqual(type(faves_relationship), list)
	# tests if the query for movie popularity returns a list
	def test_query_2_return(self):
		self.assertEqual(type(popularity_relationship), list)
	# tests if the title instance variable is correct for the created Movie class
	def test_movie_title_return(self):
		test_movie = Movie(movie_data[0])
		self.assertEqual(test_movie.title, "Inception")
	# tests if the method is_good_movie returns True for a movie with a rating above 5
	def test_is_good_movie(self):
		test_movie = Movie(movie_data[0])
		self.assertEqual(test_movie.is_movie_good(), True)
	# tests return value from get_twitter_search_data() to make sure it's a dictionary
	def test_search_data(self):
		test_dict = get_twitter_search_data("search data")
		self.assertEqual(type(test_dict), dict)
	# tests return value from get_twitter_user_data()
	def test_user_data(self):
		test_dict = get_twitter_user_data("ameliacacchione")
		self.assertEqual(type(test_dict), dict)
	def test_omdb_data(self):
		test_list = get_omdb_data(["Mean Girls", "Cars"])
		self.assertEqual(type(test_list), list)

if __name__ == "__main__":
    unittest.main(verbosity=2)