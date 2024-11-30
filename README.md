# RecommendationSystem
A basic recommendation system based on the dataset by TMDB 

#  Things I Learned While Making a Basic Recommendation System
1. Use of ast Library
The ast (Abstract Syntax Trees) library is used for safely evaluating Python literals from strings. This is particularly helpful when dealing with data stored as string representations of Python objects, such as lists or dictionaries. The ast.literal_eval() function allows you to safely convert these string representations into actual Python objects.

For example, when handling movie genres stored as a string like "[{'name': 'Action'}, {'name': 'Drama'}]", you can use ast.literal_eval() to convert it into a Python list of dictionaries.

Example:
import ast
genres_string = "[{'name': 'Action'}, {'name': 'Drama'}]"
genres_list = ast.literal_eval(genres_string)
 **Output: [{'name': 'Action'}, {'name': 'Drama'}]**
This conversion is necessary for further processing, such as extracting genre names from the list of dictionaries.

2. Using get_close_matches() from difflib
The get_close_matches() function from the difflib library helps you find the closest matches to a given string from a list of possibilities. It’s useful for fuzzy matching, especially when the user input might not exactly match the records in your dataset. This function compares strings based on their similarity and returns the closest matches.

Arguments:
word: The string you want to find close matches for.
possibilities: A list of strings to compare against.
n: The maximum number of close matches to return (default is 3).
cutoff: A float between 0 and 1 representing the minimum similarity ratio required for a match (default is 0.6).

Example :
from difflib import get_close_matches
movie_title = "Avengers Endgame"
movie_list = ["Avengers: Infinity War", "Avengers Endgame", "Batman v Superman"]
   
close_matches = get_close_matches(movie_title, movie_list, n=1, cutoff=0.6)
**** Output: ['Avengers Endgame']
