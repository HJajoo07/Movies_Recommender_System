from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load movie data
try:
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    backend_ok = True
except Exception as e:
    print("Error loading backend data:", e)
    backend_ok = False

# Home route for testing API
@app.route("/")
def home():
    if backend_ok:
        return "<h2 style='color:green;text-align:center;margin-top:50px;'>🎬 Movie Recommendation API is working!</h2>"
    else:
        return "<h2 style='color:red;text-align:center;margin-top:50px;'>❌ API Error: Data not loaded properly</h2>"

# API to get all movies
@app.route("/movies", methods=["GET"])
def get_movies():
    if backend_ok:
        return jsonify({"movies": list(movies['title'].values)})
    else:
        return jsonify({"error": "Backend not loaded"}), 500

# API to get recommendations
@app.route("/recommend", methods=["POST"])
def recommend_movies():
    if not backend_ok:
        return jsonify({"error": "Backend not loaded"}), 500

    data = request.get_json()
    movie_name = data.get("movie")
    if movie_name not in movies['title'].values:
        return jsonify({"recommendations": []})

    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended = [movies.iloc[i[0]].title for i in movie_list]
    return jsonify({"recommendations": recommended})

if __name__ == "__main__":
    app.run(debug=True)
