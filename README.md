# 🎬 Movie Recommender System

A Machine Learning-based Movie Recommender System built with **Python, Scikit-learn, and Streamlit** that helps users discover movies based on their preferences and similarity between movies.

🔴 **Live Demo:** [Try the Movie Recommender System](https://movie-recommender-system-8yvtu6tsg7hhggbbyamtj5.streamlit.app/)

## 📌 Project Overview

Finding a movie to watch can be difficult with thousands of options available. This project provides a simple and interactive way to discover movies using a recommendation algorithm based on movie similarity.

The system processes movie data, uses precomputed similarity scores, and recommends movies related to a selected movie through an interactive Streamlit web application.

## ✨ Features

- 🎥 **Movie Recommendations:** Discover similar movies based on a selected movie.
- 🧠 **Machine Learning:** Uses similarity-based recommendation logic.
- 🖼️ **Movie Posters:** Displays movie posters where available.
- ⚡ **Fast Recommendations:** Uses precomputed similarity data to generate recommendations.
- 🌐 **Interactive Web App:** Simple interface built with Streamlit.
- ☁️ **Live Deployment:** Accessible online without requiring local installation.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and preprocessing |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning and similarity-based processing |
| Streamlit | Interactive web application |
| Pickle | Saving and loading processed data and similarity information |
| TMDB API | Movie poster retrieval, if configured in the application |

## 🧠 How It Works

The recommendation workflow consists of the following steps:

1. **Data Preparation:** Movie information is processed into a suitable format.
2. **Feature Representation:** Relevant movie features are used to represent movies for similarity comparison.
3. **Similarity Calculation:** Similarity scores are calculated between movies during model preparation.
4. **Model Serialization:** Processed movie data and similarity information are stored in pickle files.
5. **Recommendation Generation:** When a user selects a movie, the system identifies movies with high similarity scores.
6. **Display Results:** Recommended movies are displayed through the Streamlit interface.

### Recommendation Approach

The project follows a similarity-based recommendation approach. The saved similarity matrix allows the application to retrieve related movies without recalculating all similarity scores for every request.

## 📂 Project Structure

```text
Movie-Recommender-System/
│
├── app.py                 # Streamlit application
├── movies_dic.pkl         # Processed movie data
├── similarity.pkl         # Precomputed similarity matrix
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

*Note: Update the filenames above if your repository uses a different structure.*

## 🚀 Run Locally

Follow these steps to run the project on your computer.

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd Movie-Recommender-System
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

**Important:** Ensure that the required pickle files and any necessary API configuration are available before running the app.

## 🌐 Live Application

Try the deployed application here:

**[Open Movie Recommender System](https://movie-recommender-system-8yvtu6tsg7hhggbbyamtj5.streamlit.app/)**

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Building a machine learning-based recommendation application.
- Working with movie datasets and data preprocessing.
- Understanding similarity-based recommendation techniques.
- Saving and loading processed data using pickle.
- Integrating a machine learning workflow with Streamlit.
- Deploying a Python application for public access.
- Handling API integration and application deployment challenges.

## ✨ Advanced Features

- 🎬 **Intelligent Movie Recommendations:** Recommends similar movies using a similarity-based recommendation algorithm.
- 🎭 **Detailed Movie Information:** Displays movie details, including cast, genres, and release dates.
- ⭐ **Reviews and Ratings:** Provides movie reviews and rating information.
- 🖼️ **Interactive Movie Details Page:** Explore additional information about selected movies.
- 🎨 **Enhanced User Interface:** Offers an intuitive and engaging movie discovery experience.
- 🔍 **Hybrid Recommendation Approach:** Combines content-based recommendations with collaborative filtering to improve recommendation relevance.
- 🌐 **Live Deployment:** Deployed on Streamlit for easy access.

## 🚀 Future Improvements

- Personalised recommendations based on individual user preferences and viewing history.
- Advanced recommendation evaluation using metrics such as Precision@K and Recall@K.
- User accounts and watchlist management.
- Improved recommendation performance for large movie datasets.

## 👨‍💻 Author

**Gitansh Soni**

B.Tech Computer Science Engineering Student | Aspiring AI/ML Engineer

---

⭐ If you find this project interesting, consider starring the repository!

