import pandas as pd
import streamlit as st
import ast
from difflib import get_close_matches

def preprocess(df):
    all_genres = []
    for i in range(len(df)):
        genres = df['genres'][i]
        if isinstance(genres, str):
            try:
                genres = ast.literal_eval(genres)
            except ValueError:
                genres = []
        if isinstance(genres, list):
            genre_names = [genre['name'] for genre in genres if isinstance(genre, dict)]
            all_genres.append(genre_names)
        else:
            all_genres.append([])

    df['all_genres'] = all_genres
    df = df.drop(columns=['genres'])
    return df

def suggest_movie(df, movie_title):
    close_matches = get_close_matches(movie_title, df['original_title'], n=1, cutoff=0.6)
    return close_matches[0] if close_matches else None

def generate_similar_movies(original_title, popularity_threshold=10):
    url = "https://raw.githubusercontent.com/Apekshaj04/RecommendationSystem/refs/heads/main/tmdb_5000_movies.csv"
    df = pd.read_csv(url)
    df = preprocess(df)
    movie = df[df['original_title'] == original_title]
    
    if not movie.empty:
        movie_genres = set(movie['all_genres'].values[0])
        movie_popularity = movie['popularity'].values[0]
        similar_movies = df[df['all_genres'].apply(lambda genres: bool(movie_genres & set(genres)))]

        similar_movies = similar_movies.sort_values(by='popularity', ascending=False)
        similar_movies = similar_movies[similar_movies['popularity'].between(movie_popularity - popularity_threshold, movie_popularity + popularity_threshold)]

        if not similar_movies.empty:
            st.write(f"**Similar Movies to {original_title}:**")
            for index, row in similar_movies.iterrows():
                st.markdown(
                    f"""
                    <div style="background-color:#f4f4f9; border:1px solid #ddd; padding:10px; margin-bottom:15px; border-radius:5px;">
                        <h4 style="color:#333;">Title: {row['original_title']}</h4>
                        <p  style="color:#333;"><strong>Genres:</strong> {row['all_genres']}</p>
                        <p style="color:#333;"><strong>Popularity:</strong> {row['popularity']}</p>
                        <p style="color:#333;"><strong>Release Date:</strong> {row['release_date']}</p>
                        <p style="color:#333;"><strong>Overview:</strong> {row['overview']}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
        else:
            suggestion = suggest_movie(df, original_title)
            if suggestion:
                st.write(f"No similar movies found. Are you trying to find a movie titled **'{suggestion}'**?")
            else:
                st.write("No similar movies found. Are you trying to find a particular movie whose words match with the one you provided?")
    else:
        suggestion = suggest_movie(df, original_title)
        if suggestion:
            st.write(f"Movie not found. Did you mean **'{suggestion}'**?")
        else:
            st.write("Movie not found. Are you trying to find a particular movie whose words match with the one you provided?")

def main():
    st.header("Movie Recommendation System")
    movie = st.text_input("Enter Movie Title:")
    if st.button("Submit") and movie:
        generate_similar_movies(movie)

if __name__ == "__main__":
    main()
