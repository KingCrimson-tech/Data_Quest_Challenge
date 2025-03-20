import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie Dashboard", layout="wide")

movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')
users_df = pd.read_csv('users.csv')

st.title("Movie Dashboard")

selected_genre = st.sidebar.multiselect(
    "Pick Genres",
    movies_df['genre'].unique(),
    movies_df['genre'].unique()
)

filtered_movies = movies_df[movies_df['genre'].isin(selected_genre)]
filtered_ratings = ratings_df[ratings_df['movie_id'].isin(filtered_movies['movie_id'])]

col1, col2 = st.columns(2)

with col1:
    fig_rating = px.histogram(filtered_ratings, x='rating',
                            title='Rating Distribution',
                            nbins=20)
    st.plotly_chart(fig_rating, use_container_width=True)

with col2:
    top_movies = filtered_ratings.merge(filtered_movies, on='movie_id')
    top_movies = top_movies.groupby(['movie_id', 'title'])['rating'].mean().reset_index()
    top_movies = top_movies.sort_values('rating', ascending=False).head(5)
    fig_top = px.bar(top_movies, x='title', y='rating',
                    title='Top 5 Movies')
    fig_top.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_top, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig_age = px.histogram(users_df, x='age',
                          title='User Age',
                          nbins=30)
    st.plotly_chart(fig_age, use_container_width=True)

with col4:
    fig_runtime = px.histogram(filtered_movies, x='runtime',
                             title='Movie Length',
                             nbins=30)
    st.plotly_chart(fig_runtime, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    country_counts = users_df['country'].value_counts().head(10)
    fig_country = px.pie(values=country_counts.values, 
                        names=country_counts.index,
                        title='User Countries')
    st.plotly_chart(fig_country, use_container_width=True)

with col6:
    genre_counts = filtered_movies['genre'].value_counts()
    fig_genre = px.pie(values=genre_counts.values,
                      names=genre_counts.index,
                      title='Movie Genres')
    st.plotly_chart(fig_genre, use_container_width=True)

st.header("Numbers")
col7, col8, col9, col10 = st.columns(4)

with col7:
    st.metric("Movies", len(filtered_movies))
with col8:
    st.metric("Users", len(users_df))
with col9:
    st.metric("Avg Rating", round(filtered_ratings['rating'].mean(), 2))
with col10:
    st.metric("Ratings", len(filtered_ratings))