import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import folium
from streamlit_folium import folium_static, st_folium
from sklearn.neighbors import NearestNeighbors
from folium.plugins import MarkerCluster
from sklearn.preprocessing import StandardScaler
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup

def get_image_from_imdb(imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page for {imdb_id}, Status Code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    image_tag = soup.find("img", {"class": "ipc-image"})

    if image_tag is not None:
        return image_tag["src"]
    else:
        print(f"Image not found for {imdb_id}")
        return None


def get_image_from_steam(steam_id):
    url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{steam_id}/header.jpg"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return url
    else:
        print(f"Failed to retrieve image for {steam_id}, Status Code: {response.status_code}")
        return None


st.set_page_config(layout= 'wide', page_title = 'Miuultainment')

#@st.cache_data
airbnb_data = pd.read_csv('airbnb_data.csv')


#@st.cache_data
meta = pd.read_csv('movie_recommendation_file.csv')

#@st.cache_data
game = pd.read_csv('content2_mst.csv')



cosine_sim = pd.read_csv("cosine_sim_movie.csv")
cosine_sim_game = pd.read_csv("cosine_sim_game.csv")

#@st.cache_data
#def popular_movies():
#    popular_movies = meta[['id', 'imdb_id','title','vote_average', 'vote_count']].sort_values(by='vote_average',ascending=False)[:50].reset_index(drop=True)
#    return popular_movies


st.markdown(
    """
    <style>
    .resizable-image img {
        width: 1400px;
        height: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="resizable-image">
        <img src="https://camo.githubusercontent.com/d6071165f118647cd11619ed34fb9f18fe75e2b48656296ee8de22fcfdf1a9cd/68747470733a2f2f6d656469612e74656e6f722e636f6d2f2d6d5f70797974655f674541414141642f77656c636f6d652d7265647461696c732e676966" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

st.title(':rainbow[MIUULtainment] :house: :movie_camera: :video_game:  :green_book: 🎶')

st.markdown('**Miuultainment: Enjoy a Unique Experience of Entertainment!**')
st.write("""Welcome to Miuultainment, the innovative recommendation site that caters to all your entertainment needs in one place.
Whether you're searching for a fantastic Airbnb for your next vacation, an enchanting book to read, a captivating movie to watch,
 an exciting game to play, or some new music to enjoy, Miuultainment has got you covered.""")



home_tab, airbnb_tab, amazon_tab, tmdb_tab, steam_tab = st.tabs(["Home", "AirBnb", "Amazon", "TMDB", "Steam"])

music_html = """
<audio id="audio1" controls style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mp3">
</audio>

<audio id="audio2" controls style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mp3">
</audio>

<audio id="audio3" controls style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mp3">
</audio>

<audio id="audio4" controls style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mp3">
</audio>

<audio id="audio5" controls style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mp3">
</audio>

<script>
document.addEventListener('DOMContentLoaded', (event) => {
  const tabs = document.querySelectorAll('.stTabs [role="tab"]');

  function playAudio(index) {
    for (let i = 1; i <= 5; i++) {
      let audio = document.getElementById('audio' + i);
      if (audio) {
        audio.pause();
        audio.currentTime = 0; // Reset audio to start
      }
    }
    let currentAudio = document.getElementById('audio' + (index + 1));
    if (currentAudio) {
      currentAudio.play();
    }
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
      playAudio(index);
    });
  });

  playAudio(0); // Play the first audio by default
});
</script>
"""


 #! Home Tab
with home_tab:

    home_tab.header('Discover Your Next Adventure')
    home_tab.write("""At Miuultainment, we believe that every experience should be extraordinary. 
    Our platform curates personalized recommendations based on your preferences, ensuring that you find the perfect match every time.""")

    col_airbnb, col_amazon, col_movie, col_game = home_tab.columns(4)


    col_airbnb.header('Stay in the Best Places')
    airbnb = 'https://cdn.dribbble.com/users/2356828/screenshots/15188850/media/f8152a69b40f21eec559e6e0d05a46f1.gif'
    col_airbnb.image(airbnb, width=300)
    col_airbnb.write("""Explore our extensive collection of top-rated Airbnb's. 
                    From cozy cabins in the woods to luxurious city apartments, we provide you with the best options to make your stay unforgettable.""")

    col_amazon.header('Read Engaging Books')
    amazon = 'https://cdn.dribbble.com/users/154752/screenshots/1244719/book.gif'
    col_amazon.image(amazon, width=300)
    col_amazon.write("""Dive into a world of literature with our handpicked book recommendations. Whether you love fiction, non-fiction, mystery,
                romance, or sci-fi, Miuultainment helps you discover books that you'll love.""")


    col_movie.header('Watch Captivating Movies')
    tmdb = 'https://gifdb.com/images/high/joker-best-movie-ever-bdfw105oiqoupa0l.gif'
    col_movie.image(tmdb, width=230)
    col_movie.write("""Enjoy a cinematic experience with our movie suggestions. Whether you’re into thrillers, comedies, dramas, or documentaries,
                Miuultainment ensures you never run out of great movies to watch.""")

    col_game.header('Play Exciting Games')
    steam = 'https://steamuserimages-a.akamaihd.net/ugc/1263771316472872541/F5A25EF308CE1CF747952AA84205CB9A66841DBE/?imw=512&imh=512&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true'
    col_game.image(steam, width=230)
    col_game.write("""Level up your gaming experience with our curated game recommendations. 
                From action-packed adventures to mind-bending puzzles, find the perfect game to keep you entertained for hours.""")



#! TMDB tab
with tmdb_tab:


    def content_based_recommender(title, cosine_sim, dataframe):
        # index'leri olusturma
        indices = pd.Series(dataframe.index, index=dataframe['title'])
        indices = indices[~indices.index.duplicated(keep='last')]
        # title'ın index'ini yakalama
        movie_index = indices[title]
        # Benzerlik skorlarını alma
        cosine_sim_matrix = cosine_sim.values
        similarity_scores = cosine_sim_matrix[movie_index]
        # Eğer similarity_scores 3D bir dizi ise (örneğin, [1, 9548, 9548]), 2D'ye dönüştürme
        if similarity_scores.ndim == 3:
            similarity_scores = similarity_scores.squeeze()  # 3D'den 2D'ye sıkıştırma
        # Benzerlik skorlarını DataFrame'e dönüştürme
        similarity_scores_df = pd.DataFrame(similarity_scores, index=dataframe.index, columns=["score"])
        # Kendisi haric ilk 10 filmi getirme
        movie_indices = similarity_scores_df.sort_values(by="score", ascending=False).index[1:6]
        # Film bilgilerini döndürme
        return dataframe.loc[movie_indices]

    tmdb_col1, tmdb_col2, tmdb_col3 = tmdb_tab.columns([1,2,1])
    selected_movie = tmdb_col2.selectbox('Choose a movie you like.', options= meta.title.unique())


    recommendations_df = content_based_recommender(title=selected_movie,cosine_sim=cosine_sim,dataframe=meta)
    movie_1, movie_2, movie_3, movie_4, movie_5 = tmdb_tab.columns(5)


    tmdbcol1, tmdbcol2, tmdbcol3 = tmdb_tab.columns([1,0.5,1], gap='large')
    recommend_button = tmdbcol2.button('Recommend a Movie')

    if recommend_button:
        # Önerilen filmleri göster
        for index, movie_col in enumerate([movie_1, movie_2, movie_3, movie_4, movie_5]):
            # `recommendations_df` DataFrame'inden film ID'sini ve başlığını al
            if index < len(recommendations_df):
                movie_row = recommendations_df.iloc[index]
                movie_id = movie_row['id']
                movie_title = movie_row['title']

                # `meta` DataFrame'inde film ID'sine göre arama yap
                movie = meta.loc[meta['id'] == movie_id]  # Meta DataFrame'inde id sütununa göre arama yap

                if movie.empty:
                    continue  # Film bulunamadıysa bir sonraki filme geç

                imdb_id = movie['imdb_id'].values[0]  # Numpy array'den str'e dönüştürme

                movie_col.subheader(f"**{movie_title}**")

                # Resim URL'sini alma ve kontrol etme
                image_url = get_image_from_imdb(imdb_id)
                if image_url:
                    movie_col.image(image_url,width = 200, use_column_width=True)
    st.markdown(music_html, unsafe_allow_html=True)

with airbnb_tab:

    airbnb_col1, airbnb_col2, airbnb_col3, airbnb_col4 = airbnb_tab.columns(4)
    selected_neighboorhood = airbnb_col1.selectbox('Neighboord', options= airbnb_data.neighbourhood_group.unique())

    price_min = airbnb_col2.number_input('Min. Price', min_value=0, max_value= int(airbnb_data.price.max()), value = 0)
    price_max = airbnb_col2.number_input('Max. Price', min_value=1, max_value = int(airbnb_data.price.max()), value= 999)
    selected_room_type = airbnb_col3.selectbox('Room Type', options = airbnb_data['room type'].unique())
    selected_cancellation_policy = airbnb_col4.selectbox('Cancellation Policy', options = airbnb_data['cancellation_policy'].unique())


    airbnb_tab.markdown("""
        <style>
        .space-above {
            margin-top: 20px;
        }
        .stButton>button {
            background-color: #a3c9f1;
            color: #000000;
        }
        </style>
        """, unsafe_allow_html=True)

    aircol1, aircol2, aircol3 = airbnb_tab.columns([1,0.5,1], gap='large')
    airrecommend_button = aircol2.button('Recommend AirBnb')


    def recommend_airbnb(user_neighbourhood_group,user_price_range_min,user_price_range_max, user_room_type, user_cancellation_policy, num_neighbors=2,num_recommendations = 500,limit = 3):

        # Kullanıcı kriterlerine göre filtreleme
        filtered_listings = airbnb_data[
            (airbnb_data['neighbourhood_group'] == user_neighbourhood_group) &
            (airbnb_data['price'] >= user_price_range_min) &
            (airbnb_data['price'] <= user_price_range_max) &
            (airbnb_data['room type'] == user_room_type) &
            (airbnb_data['cancellation_policy']==user_cancellation_policy)
        ]


        if filtered_listings.empty:
            airbnb_tab.text("Kriterlere uygun sonuç bulunamadı.")
            return None

        # Kullanılacak özellikleri seçelim
        features = airbnb_data[['price', "service fee", 'number of reviews', 'review rate number', 'lat', 'long']]
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        # K-Nearest Neighbors modelini oluşturalım
        knn = NearestNeighbors(n_neighbors=num_neighbors, algorithm='auto')
        knn.fit(features_scaled)

        # Filtrelenmiş evlerin özelliklerini alalım
        filtered_features = filtered_listings[['price', "service fee", 'number of reviews', 'review rate number', 'lat', 'long']]
        filtered_features_scaled = scaler.transform(filtered_features)

        # Benzer evleri bulalım
        distances, indices = knn.kneighbors(filtered_features_scaled)

        # Benzer ev ilanlarının bilgilerini alalım
        recommended_listings = airbnb_data.iloc[indices.flatten()]

        # Yalnızca review rate number 3 ve üzeri olanları filtreleyelim
        recommended_listings = recommended_listings[recommended_listings['review rate number'] >= limit]

        if recommended_listings.empty:
            airbnb_tab.text(f"Review rate number {limit} ve üzeri uygun sonuç bulunamadı.")
            return None

        # Review rate number'a göre büyükten küçüğe sıralayalım
        recommended_listings = recommended_listings.sort_values(by='review rate number', ascending=False)

        # İlk num_recommendations tanesini seçelim
        top_recommendations = recommended_listings.head(num_recommendations)
        top_recommendations['number of reviews'] = top_recommendations['number of reviews'].astype(int)
        # Ortalama konumu bulalım
        avg_lat = top_recommendations['lat'].mean()
        avg_long = top_recommendations['long'].mean()

        # Haritayı oluştur
        map_ = folium.Map(location=[avg_lat, avg_long], zoom_start=10)
        marker_cluster = MarkerCluster().add_to(map_)

        for idx, row in top_recommendations.iterrows():
            folium.Marker(
                location=[row['lat'], row['long']],
                popup=f"<strong>{row['NAME']}</strong><br>Price: ${row['price']}<br>Service Fee: ${row['service fee']}<br>Review Rate: {row['review rate number']}<br>Number of Reviews: {row['number of reviews']}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(marker_cluster)
        # Haritayı Jupyter Notebook içinde görüntüle
        return map_, top_recommendations


    if airrecommend_button:
        if price_min > price_max:
            airbnb_tab.text('Minimum Price cannot be bigger than Maximum Price')
        else:
            map_, recommendations = recommend_airbnb(user_neighbourhood_group = selected_neighboorhood, user_price_range_min = price_min,
                user_price_range_max=price_max, user_room_type = selected_room_type,user_cancellation_policy= selected_cancellation_policy)

            folium_static(map_, width=1750 , height=600)
    st.markdown(music_html, unsafe_allow_html=True)

with amazon_tab:
    st.subheader("Sekme 4")
    st.write("Burada Sekme 4 içeriği bulunacak.")

with steam_tab:

    def content_based_recommender_game(title, cosine_sim_game, dataframe):
        # index'leri olusturma
        indices = pd.Series(dataframe.index, index=dataframe['title'])
        indices = indices[~indices.index.duplicated(keep='last')]
        # title'ın index'ini yakalama
        game_index = indices[title]
        # Benzerlik skorlarını alma
        cosine_sim_matrix = cosine_sim_game.values
        similarity_scores = cosine_sim_matrix[game_index]
        # Benzerlik skorlarını DataFrame'e dönüştürme
        similarity_scores_df = pd.DataFrame(similarity_scores, index=dataframe.index, columns=["score"])
        game_indices = similarity_scores_df.sort_values(by="score", ascending=False).index[1:11]
        return dataframe.loc[game_indices]


    steam_col1, steam_col2, steam_col3 = steam_tab.columns([1, 2, 1])
    selected_game = steam_col2.selectbox('Choose a game you like.', options=game.title.unique())

    recommendations_df = content_based_recommender_game(title=selected_game, cosine_sim_game=cosine_sim_game, dataframe=game)
    game_1, game_2, game_3, game_4, game_5 = steam_tab.columns(5)
    game_6, game_7, game_8, game_9, game_10 = steam_tab.columns(5)

    gamecol1, gamecol2, gamecol3 = steam_tab.columns([2, 1, 2], gap='large')
    recommend_button = gamecol2.button('Recommend a Game')

    if recommend_button:
        for index, game_col in enumerate([game_1, game_2, game_3, game_4, game_5,game_6, game_7, game_8, game_9, game_10]):
            if index < len(recommendations_df):
                game_row = recommendations_df.iloc[index]
                game_id = game_row['app_id']
                game_title = game_row['title']
                game_col.subheader(f"**{game_title}**")
                image_url = get_image_from_steam(game_id)
                if image_url:
                    game_col.image(image_url, width=200, use_column_width=True)

    st.markdown(music_html, unsafe_allow_html=True)

