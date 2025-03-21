import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Movie Dashboard", layout="wide")

movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')
users_df = pd.read_csv('users.csv')

st.title("Movie Dashboard")

# Add movie search feature after the title
st.subheader("Search a Movie")
movie_search = st.text_input("Type a movie name")

if movie_search:
    # Find movies that match the search
    found_movies = movies_df[movies_df['title'].str.contains(movie_search, case=False)]
    
    if len(found_movies) > 0:
        st.write(f"Found {len(found_movies)} movies!")
        
        for _, movie in found_movies.iterrows():
            # Get ratings for this movie
            movie_ratings = ratings_df[ratings_df['movie_id'] == movie['movie_id']]
            avg_rating = movie_ratings['rating'].mean()
            num_ratings = len(movie_ratings)
            
            # Show movie info in an expander
            with st.expander(f"🎬 {movie['title']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("Release Year:", movie['release_year'])
                    st.write("Runtime:", movie['runtime'], "minutes")
                
                with col2:
                    st.write("Genre:", movie['genre'])
                    st.write("Number of Ratings:", num_ratings)
                
                with col3:
                    if num_ratings > 0:
                        st.write("Average Rating:", round(avg_rating, 2))
                        # Make a simple rating chart
                        rating_dist = px.histogram(movie_ratings, x='rating', 
                                                 title='Rating Distribution',
                                                 nbins=10)
                        st.plotly_chart(rating_dist, use_container_width=True)
                    else:
                        st.write("No ratings yet!")
    else:
        st.write("No movies found! Try another name.")

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

# Churn Analysis
st.header("User Activity Analysis")
ratings_df['review_date'] = pd.to_datetime(ratings_df['review_date'])
last_review = ratings_df.groupby('user_id')['review_date'].max().reset_index()
last_review['days_since_last_review'] = (datetime.now() - last_review['review_date']).dt.days

col7, col8 = st.columns(2)

with col7:
    fig_churn = px.histogram(last_review, x='days_since_last_review',
                           title='Days Since Last Review',
                           nbins=30)
    st.plotly_chart(fig_churn, use_container_width=True)

with col8:
    churn_status = last_review['days_since_last_review'].apply(lambda x: 'Active' if x < 30 else 'At Risk' if x < 90 else 'Churned')
    churn_counts = churn_status.value_counts()
    fig_churn_status = px.pie(values=churn_counts.values,
                            names=churn_counts.index,
                            title='User Churn Status')
    st.plotly_chart(fig_churn_status, use_container_width=True)

st.header("Numbers")
col9, col10, col11, col12 = st.columns(4)

with col9:
    st.metric("Movies", len(filtered_movies))
with col10:
    st.metric("Users", len(users_df))
with col11:
    st.metric("Avg Rating", round(filtered_ratings['rating'].mean(), 2))
with col12:
    st.metric("Ratings", len(filtered_ratings))

st.markdown("---")
st.markdown("Made with Streamlit") 