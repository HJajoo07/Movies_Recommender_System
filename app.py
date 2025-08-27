import streamlit as st
import pickle
import pandas as pd

# Load saved data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Recommendation function
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies=[]
    for i in movie_list:
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies
# Streamlit UI
st.title("🎬 Movie Recommendation System")

movie_name = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    recommendations = recommend(movie_name)
    st.write("### Recommended Movies")
    for m in recommendations:
        st.write("- ", m)
