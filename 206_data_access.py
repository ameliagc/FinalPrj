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

# Set up caching process
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# Define function get_twitter_search_data that takes in a movie tile and returns data about ten tweets that mention that movie and caches this data if not cached already
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

# List of resulting tweet dictionaries with all three movies
twitter_data_search_list = []
twitter_data_search_list.append(twitter_data_Inception)
twitter_data_search_list.append(twitter_data_Trainwreck)
twitter_data_search_list.append(twitter_data_Brooklyn)


# Make cache file for Twitter data
CACHE_FNAME3 = "user_twitter_cache.json"

# Set up caching process
try:
	cache_file3 = open(CACHE_FNAME3,'r')
	cache_contents3 = cache_file3.read()
	CACHE_DICTION3 = json.loads(cache_contents3)
except:
	CACHE_DICTION3 = {}

# Define function get_twitter_search_data that takes in a movie tile and returns data about ten tweets that mention that movie and caches this data if not cached already
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

#user_twitter_data = get_twitter_user_data("IMDb")

# Make cache file for OMDB data
CACHE_FNAME2 = "omdb_cache.json"

# Set up caching process
try:
	cache_file2 = open(CACHE_FNAME2,'r')
	cache_contents2 = cache_file2.read()
	CACHE_DICTION2 = json.loads(cache_contents2)
except:
	CACHE_DICTION2 = {}

# Write function get_omdb data that takes in a movie title and returns all of the data about the movie and caches the data if it hasn't been cached already

# Function that gets data from OMDB and puts it in cache file
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

# Make table to hold Twitter data with columns: tweet ID, text, retweets (will probably add to this later)
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

# Query to access users mentioned in tweets from Tweets database
user_neighborhood = []
query = "SELECT user_mentions FROM Tweets WHERE user_mentions > 0"
cur.execute(query)
temp_tup = cur.fetchall()
user_neighborhood = [x[0] for x in temp_tup]

# Query to access users who posted tweets in Tweets database
query1 = "SELECT user FROM Tweets"
cur.execute(query1)
temp_tup1 = cur.fetchall()
user_neighborhood += [x[0] for x in temp_tup1]

user_neighborhood_dict = {}
for user in user_neighborhood:
	user_neighborhood_dict[user] = get_twitter_user_data(user)

# Make tabel to hold User data with columns: user ID, user screen name, number of favorites
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('CREATE TABLE Users (user_id INTEGER PRIMARY KEY, screen_name TEXT, favorites INTEGER)')

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
	# Instance variables: title, director, IMDB rating, list of actors, number of languages

	# Constructor: accepts a movie dictionary

	def __init__(self, movie_dict):
		self.movie_dict = movie_dict
		self.title = movie_dict["Title"]
		self.director = movie_dict["Director"]
		self.imdb_rating = movie_dict["imdbRating"]
		self.actor_list = movie_dict["Actors"]
		self.num_lang = movie_dict["Language"]

	# Define __str__ method that doesn't take any parameters
	def __str__(self):
		return "{} was directed by {} and has an IMDB rating of {}. The actors include {}. The following languages are spoken in the movie: {}.".format(self.title, self.director, self.imdb_rating, self.actor_list, self.num_lang)
	
	# Define num_languages method that doesn't take any parameters


# Query to see if users who get more favorites
query_faves = "SELECT Users.favorites, Tweets.favorites FROM Tweets INNER JOIN Users on Tweets.user_id = Users.user_id"
cur.execute(query_faves)
faves_relationship = cur.fetchall()

# Query to see which movies got the most favorites in tweets about them
query_popularity = "SELECT OMDB.title, Tweets.favorites FROM Tweets INNER JOIN OMDB on Tweets.movie_search = OMDB.title"
cur.execute(query_popularity)
popularity_relationship = cur.fetchall()

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

inception_total	= 0
trainwreck_total = 0
brooklyn_total = 0
for num in inception_faves:
	inception_total += num
for num in trainwreck_faves:
	trainwreck_total += num
for num in brooklyn_faves:
	brooklyn_total += num

#user_favorites = []
#user_favorites = [x[0] for x in faves_relationship]

#tweet_favorites = []
#tweet_favorites = [x[1] for x in faves_relationship]

# Create text file to write data to
f = open("summary_stats.txt", "w+")

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

f.close()
'''
# Will have to pass in 1st item from movie list so it's a dictionary
movie_dict_1 = json.loads(movie_data[0])
movie_dict_2 = json.loads(movie_data[1])
movie_dict_3 = json.loads(movie_data[2])

movie_dict_list = []
movie_dict_list.append(movie_dict_1)
movie_dict_list.append(movie_dict_2)
movie_dict_list.append(movie_dict_3)

# Create list of instances of Movie class and store in movie_instance_list
movie_instance_list = []
for movie in movie_dict_list:
	movie_instance_list.append(Movie(movie))

# Define a function movie_director that takes in the list three_movies and returns the variable movie_director that holds a list of the directors of those three movies
director_search_1 = get_twitter_search_data("Christopher Nolan")
director_search_2 = get_twitter_search_data("Judd Apatow")
director_search_3 = get_twitter_search_data("John Crowly")

list_of_director_searches = []
list_of_director_searches.append(director_search_1)
list_of_director_searches.append(director_search_2)
list_of_director_searches.append(director_search_3)
'''

#for director in list_of_director_searches:
	#print(director["statuses"])

#for director in list_of_director_searches:
	#print(director)

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