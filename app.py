import streamlit as st
import pandas as pd
import pickle
import requests
import joblib
import time

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

session = requests.Session()

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"
BACKDROP_URL = "https://image.tmdb.org/t/p/original"

movie_dic = pickle.load(open("movies_dic.pkl", "rb"))
movies = pd.DataFrame(movie_dic)
similarity = joblib.load("similarity.joblib")

if "selected_movie" not in st.session_state:
    st.session_state["selected_movie"] = None

if "recommendations" not in st.session_state:
    st.session_state["recommendations"] = []

if "page" not in st.session_state:
    st.session_state["page"] = "home"

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(229, 9, 20, 0.13), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(111, 66, 193, 0.12), transparent 25%),
        #08090d;
    color: #ffffff;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.hero {
    position: relative;
    min-height: 360px;
    border-radius: 28px;
    padding: 55px 55px;
    margin-bottom: 35px;
    overflow: hidden;
    background:
        linear-gradient(90deg, rgba(5,5,8,0.98) 0%, rgba(5,5,8,0.88) 38%, rgba(5,5,8,0.30) 100%),
        linear-gradient(135deg, #171820, #090a0f);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 25px 80px rgba(0,0,0,0.45);
}

.hero-small {
    color: #e50914;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.hero-title {
    font-size: 52px;
    line-height: 1.05;
    font-weight: 900;
    margin: 0;
    max-width: 700px;
}

.hero-text {
    color: #a8abb5;
    font-size: 17px;
    max-width: 650px;
    line-height: 1.7;
    margin-top: 18px;
}

.brand {
    font-size: 29px;
    font-weight: 900;
    letter-spacing: -1px;
    margin-bottom: 25px;
}

.brand span {
    color: #e50914;
}

.section-title {
    font-size: 26px;
    font-weight: 800;
    margin-top: 35px;
    margin-bottom: 18px;
}

.movie-card {
    background: linear-gradient(145deg, #15161d, #0d0e13);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 10px;
    transition: all 0.25s ease;
    box-shadow: 0 12px 30px rgba(0,0,0,0.22);
}

.movie-card:hover {
    transform: translateY(-7px);
    border-color: rgba(229,9,20,0.45);
    box-shadow: 0 20px 45px rgba(0,0,0,0.45);
}

.movie-title {
    font-size: 15px;
    font-weight: 700;
    line-height: 1.35;
    margin: 10px 3px 3px 3px;
    min-height: 42px;
}

.rating-pill {
    display: inline-block;
    background: rgba(255,193,7,0.12);
    color: #ffc107;
    border: 1px solid rgba(255,193,7,0.18);
    border-radius: 50px;
    padding: 4px 9px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 4px;
}

.info-box {
    background: linear-gradient(145deg, #15161d, #0c0d11);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
}

.movie-detail-title {
    font-size: 45px;
    line-height: 1.08;
    font-weight: 900;
    margin-bottom: 12px;
}

.movie-meta {
    color: #a7a9b1;
    font-size: 14px;
    margin-bottom: 18px;
}

.rating-large {
    font-size: 22px;
    font-weight: 800;
    color: #ffc107;
}

.genre-pill {
    display: inline-block;
    background: rgba(229,9,20,0.10);
    border: 1px solid rgba(229,9,20,0.28);
    color: #ff6b72;
    border-radius: 50px;
    padding: 6px 12px;
    margin: 4px 5px 4px 0;
    font-size: 12px;
    font-weight: 600;
}

.cast-name {
    font-size: 14px;
    font-weight: 700;
    margin-top: 7px;
}

.cast-character {
    color: #8e919c;
    font-size: 12px;
}

.review-box {
    background: #111218;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
}

.review-author {
    color: #ffffff;
    font-weight: 800;
    margin-bottom: 10px;
}

.review-text {
    color: #b0b2bb;
    line-height: 1.7;
    font-size: 14px;
}

.footer {
    text-align: center;
    color: #666a75;
    padding: 45px 0 15px 0;
    font-size: 13px;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.10);
    background: #15161d;
    color: white;
    font-weight: 700;
    min-height: 42px;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background: #e50914;
    border-color: #e50914;
    color: white;
}

div[data-baseweb="select"] > div {
    background: #12131a;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 13px;
}

.stTextInput > div > div > input {
    background: #12131a;
    color: white;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 13px;
}

[data-testid="stImage"] img {
    border-radius: 15px;
}

hr {
    border-color: rgba(255,255,255,0.07);
}

</style>
""", unsafe_allow_html=True)


def tmdb_request(endpoint, params=None):
    if params is None:
        params = {}

    params["api_key"] = TMDB_API_KEY
    url = BASE_URL + endpoint

    for attempt in range(3):
        try:
            response = session.get(
                url,
                params=params,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=20
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                return None
            time.sleep(1)

    return None


@st.cache_data(ttl=3600, show_spinner=False)
def get_movie_details(movie_id):
    return tmdb_request(
        f"/movie/{movie_id}",
        {"language": "en-US"}
    )


@st.cache_data(ttl=3600, show_spinner=False)
def get_credits(movie_id):
    return tmdb_request(
        f"/movie/{movie_id}/credits",
        {"language": "en-US"}
    )


@st.cache_data(ttl=3600, show_spinner=False)
def get_trailer(movie_id):
    data = tmdb_request(
        f"/movie/{movie_id}/videos",
        {"language": "en-US"}
    )

    if not data:
        return None

    videos = data.get("results", [])

    for video in videos:
        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
            and video.get("official") is True
        ):
            return f"https://www.youtube.com/watch?v={video['key']}"

    for video in videos:
        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
        ):
            return f"https://www.youtube.com/watch?v={video['key']}"

    return None


@st.cache_data(ttl=3600, show_spinner=False)
def get_reviews(movie_id):
    data = tmdb_request(
        f"/movie/{movie_id}/reviews",
        {
            "language": "en-US",
            "page": 1
        }
    )

    if not data:
        return []

    return data.get("results", [])


@st.cache_data(ttl=3600, show_spinner=False)
def get_similar_movies(movie_id):
    data = tmdb_request(
        f"/movie/{movie_id}/similar",
        {
            "language": "en-US",
            "page": 1
        }
    )

    if not data:
        return []

    return data.get("results", [])[:6]


@st.cache_data(ttl=3600, show_spinner=False)
def get_poster(movie_id):
    details = get_movie_details(movie_id)

    if details:
        return details.get("poster_path")

    return None


def recommend(movie):
    movie_idx = movies[movies["title"] == movie].index[0]
    distance = similarity[movie_idx]

    movie_list = sorted(
        enumerate(distance),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append({
            "title": movies.iloc[i[0]].title,
            "movie_id": movie_id,
            "score": float(i[1])
        })

    return recommended_movies


def movie_card(movie, key_prefix="movie"):
    movie_id = movie["movie_id"]
    title = movie["title"]

    poster_path = get_poster(movie_id)

    st.markdown('<div class="movie-card">', unsafe_allow_html=True)

    if poster_path:
        st.image(
            IMAGE_URL + poster_path,
            use_container_width=True
        )
    else:
        st.markdown(
            '<div style="height:260px;display:flex;align-items:center;justify-content:center;background:#181920;border-radius:15px;color:#777;">No Poster</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        f'<div class="movie-title">{title}</div>',
        unsafe_allow_html=True
    )

    if "score" in movie:
        score = movie["score"]
        st.markdown(
            f'<div class="rating-pill">✨ {score:.0%} Match</div>',
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "View Details",
        key=f"{key_prefix}_{movie_id}"
    ):
        st.session_state["selected_movie"] = movie_id
        st.rerun()


def show_movie_details(movie_id):
    details = get_movie_details(movie_id)

    if not details:
        st.error("Movie details could not be loaded.")
        return

    credits = get_credits(movie_id)
    trailer = get_trailer(movie_id)
    reviews = get_reviews(movie_id)
    similar_movies = get_similar_movies(movie_id)

    if st.button("← Back to Movies", key="back_details"):
        st.session_state["selected_movie"] = None
        st.rerun()

    title = details.get("title", "Unknown")
    overview = details.get("overview", "No overview available.")
    poster_path = details.get("poster_path")
    backdrop_path = details.get("backdrop_path")
    rating = details.get("vote_average", 0)
    release_date = details.get("release_date", "N/A")
    runtime = details.get("runtime")
    genres = details.get("genres", [])

    if backdrop_path:
        st.markdown(
            f"""
            <div style="
                height:360px;
                border-radius:25px;
                margin-top:20px;
                margin-bottom:30px;
                background:
                linear-gradient(90deg, rgba(5,5,8,0.98) 0%, rgba(5,5,8,0.70) 45%, rgba(5,5,8,0.20) 100%),
                url('{BACKDROP_URL + backdrop_path}');
                background-size:cover;
                background-position:center;
                box-shadow:0 25px 70px rgba(0,0,0,0.45);
            ">
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2 = st.columns([1, 2.3], gap="large")

    with col1:
        if poster_path:
            st.image(
                IMAGE_URL + poster_path,
                use_container_width=True
            )

    with col2:
        st.markdown(
            f'<div class="movie-detail-title">{title}</div>',
            unsafe_allow_html=True
        )

        meta_parts = []

        if release_date != "N/A":
            meta_parts.append(f"📅 {release_date}")

        if runtime:
            meta_parts.append(f"⏱️ {runtime} min")

        meta_parts.append(f"🎬 TMDB {movie_id}")

        st.markdown(
            f'<div class="movie-meta">{" &nbsp; • &nbsp; ".join(meta_parts)}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="rating-large">⭐ {rating:.1f} / 10</div>',
            unsafe_allow_html=True
        )

        if genres:
            genre_html = ""

            for genre in genres:
                genre_html += (
                    f'<span class="genre-pill">{genre["name"]}</span>'
                )

            st.markdown(
                f'<div style="margin-top:18px;">{genre_html}</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            '<div style="height:18px;"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div style="font-size:22px;font-weight:800;margin-bottom:10px;">Story</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="color:#b4b6bf;line-height:1.8;font-size:15px;">{overview}</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    director_name = "Information unavailable"

    if credits:
        crew = credits.get("crew", [])

        directors = [
            person.get("name")
            for person in crew
            if person.get("job") == "Director"
        ]

        if directors:
            director_name = ", ".join(directors)

    st.markdown(
        '<div class="section-title">🎬 Director</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="info-box"><b>{director_name}</b></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">🌟 Star Cast</div>',
        unsafe_allow_html=True
    )

    if credits:
        cast = credits.get("cast", [])[:10]

        if cast:
            cast_cols = st.columns(5)

            for index, person in enumerate(cast):
                with cast_cols[index % 5]:
                    profile_path = person.get("profile_path")

                    if profile_path:
                        st.image(
                            IMAGE_URL + profile_path,
                            use_container_width=True
                        )
                    else:
                        st.markdown(
                            '<div style="height:220px;background:#171820;border-radius:15px;display:flex;align-items:center;justify-content:center;color:#777;">No Image</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        f'<div class="cast-name">{person.get("name", "Unknown")}</div>',
                        unsafe_allow_html=True
                    )

                    character = person.get("character", "")

                    if character:
                        st.markdown(
                            f'<div class="cast-character">as {character}</div>',
                            unsafe_allow_html=True
                        )

    st.markdown(
        '<div class="section-title">🎞️ Official Trailer</div>',
        unsafe_allow_html=True
    )

    if trailer:
        st.video(trailer)
    else:
        st.info("Trailer not available.")

    st.markdown(
        '<div class="section-title">💬 Reviews</div>',
        unsafe_allow_html=True
    )

    if reviews:
        for review in reviews[:5]:
            author = review.get("author", "Anonymous")
            content = review.get("content", "")

            if len(content) > 1500:
                content = content[:1500] + "..."

            st.markdown(
                f"""
                <div class="review-box">
                    <div class="review-author">👤 {author}</div>
                    <div class="review-text">{content}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No reviews available.")

    st.markdown(
        '<div class="section-title">🎥 You May Also Like</div>',
        unsafe_allow_html=True
    )

    if similar_movies:
        similar_cols = st.columns(6)

        for index, movie in enumerate(similar_movies):
            with similar_cols[index % 6]:
                poster = movie.get("poster_path")

                if poster:
                    st.image(
                        IMAGE_URL + poster,
                        use_container_width=True
                    )

                title = movie.get("title", "Unknown")

                st.markdown(
                    f'<div class="movie-title">{title}</div>',
                    unsafe_allow_html=True
                )

                if movie.get("vote_average"):
                    st.markdown(
                        f'<div class="rating-pill">⭐ {movie.get("vote_average"):.1f}</div>',
                        unsafe_allow_html=True
                    )

                if st.button(
                    "Open",
                    key=f"similar_{movie_id}_{movie.get('id')}"
                ):
                    st.session_state["selected_movie"] = movie.get("id")
                    st.rerun()


if st.session_state["selected_movie"]:

    show_movie_details(
        st.session_state["selected_movie"]
    )

else:

    st.markdown(
        '<div class="brand">CINE<span>MATCH</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero">
            <div class="hero-small">AI powered movie discovery</div>
            <div class="hero-title">Find your next<br>favorite movie.</div>
            <div class="hero-text">
                Discover movies you'll love with intelligent recommendations,
                detailed movie information, trailers, cast, reviews and more.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">🎯 Find a Movie</div>',
        unsafe_allow_html=True
    )

    search_text = st.text_input(
        "",
        placeholder="🔎 Search for a movie...",
        label_visibility="collapsed"
    )

    movie_options = movies["title"].values.tolist()

    if search_text:
        filtered_movies = [
            movie for movie in movie_options
            if search_text.lower() in movie.lower()
        ][:10]

        if filtered_movies:
            selected = st.selectbox(
                "Select movie",
                filtered_movies,
                label_visibility="collapsed"
            )
        else:
            selected = st.selectbox(
                "Select movie",
                movie_options,
                label_visibility="collapsed"
            )
    else:
        selected = st.selectbox(
            "Select movie",
            movie_options,
            label_visibility="collapsed"
        )

    if st.button(
        "✨ Discover Similar Movies",
        use_container_width=True
    ):
        with st.spinner("Finding movies you'll love..."):
            recommendations = recommend(selected)

        st.session_state["recommendations"] = recommendations

    recommendations = st.session_state.get(
        "recommendations",
        []
    )

    if recommendations:
        st.markdown(
            '<div class="section-title">🔥 Recommended For You</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(5)

        for index, movie in enumerate(recommendations):
            with cols[index]:
                movie_card(
                    movie,
                    key_prefix=f"recommendation_{index}"
                )

    st.markdown(
        '<div class="section-title">🍿 Explore More</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-box">
            <div style="font-size:20px;font-weight:800;margin-bottom:8px;">
                Your movie night starts here.
            </div>
            <div style="color:#9295a0;line-height:1.7;">
                Pick a movie, discover similar titles and explore everything
                from ratings and reviews to cast, trailers and more.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="footer">
        <div style="font-size:15px;font-weight:700;color:#a5a7b0;">
            CINE<span style="color:#e50914;">MATCH</span>
        </div>
        <div style="margin-top:6px;">
            AI Powered Movie Discovery • Made by Gitansh Swarnkar ❤️
        </div>
    </div>
    """,
    unsafe_allow_html=True
)