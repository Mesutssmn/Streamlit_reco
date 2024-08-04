import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup

# HTML içeriği
html_content = '''
<ol class="list-collection__content--numbered list-collection__content ">
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/diablo-iv/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot1"><p class="list-item__title text-bold ">Diablo IV</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">Jun 6, 2023</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/the-legend-of-zelda-tears-of-the-kingdom/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot2"><p class="list-item__title text-bold ">The Legend of Zelda: Tears of the Kingdom</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">May 12, 2023</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/star-wars-jedi-survivor/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot3"><p class="list-item__title text-bold ">Star Wars Jedi: Survivor</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">Apr 28, 2023</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/final-fantasy-xvi/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot4"><p class="list-item__title text-bold ">Final Fantasy XVI</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">Jun 22, 2023</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/starfield/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot5"><p class="list-item__title text-bold ">Starfield</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">Sep 6, 2023</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/dead-island-2/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot6"><p class="list-item__title text-bold ">Dead Island 2</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">Apr 21, 2023</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/redfall/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot7"><p class="list-item__title text-bold ">Redfall</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">May 2, 2023</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/suicide-squad-kill-the-justice-league/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot8"><p class="list-item__title text-bold ">Suicide Squad: Kill The Justice League</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">Mar 26, 2024</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/street-fighter-6/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot9"><p class="list-item__title text-bold ">Street Fighter 6</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">Jun 2, 2023</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
<li class="list-item width-100 overflow--hidden flexbox-row flexbox-nowrap flexbox-align-center "><div class="list-item__content flexbox-flex-even "><a href="/games/assassins-creed-mirage/" class="js-click-tag" data-click-tag="front_door|topgames|overall|slot10"><p class="list-item__title text-bold ">Assassin's Creed Mirage</p></a><div class="card-metadata "><div class="symbol-text hide-icon"><i class=" "><svg width="79.91" height="80" viewBox="0 0 79.91 80" aria-hidden="true" class="symbol symbol-comment text-medium "><path d="M39.83 0C17.73 0 0 14.33 0 32c0 13.12 10.17 24.39 24.17 29.33V80L40 64c22.09 0 39.91-14.33 39.91-32S61.92 0 39.83 0Z"></path></svg></i><span class="text-small ">Oct 5, 2023</span></div></div><div class="dn"><span id="_qualtrics_release_indicator">released</span></div></div></li>
</ol>
'''

# BeautifulSoup kullanarak HTML içeriğini parse etme
soup = BeautifulSoup(html_content, 'html.parser')
games_list = soup.find_all('li', class_='list-item')

# Oyun bilgilerini toplama
games_data = []
base_url = "https://www.gamespot.com"
for game in games_list:
    title_tag = game.find('p', class_='list-item__title')
    date_tag = game.find('span', class_='text-small')
    link_tag = game.find('a', href=True)
    if title_tag and date_tag and link_tag:
        title = title_tag.text.strip()
        release_date = date_tag.text.strip()
        game_url = base_url + link_tag['href']
        games_data.append(
            {"Game Title": f"<a href='{game_url}' target='_blank'>{title}</a>", "Release Date": release_date})

# DataFrame oluşturma
upcoming_games_df = pd.DataFrame(games_data)

# Çıkış tarihini datetime formatına çevirme ve sıralama
upcoming_games_df['Release Date'] = pd.to_datetime(upcoming_games_df['Release Date'])
upcoming_games_df = upcoming_games_df.sort_values('Release Date', ascending=False)


def get_image_from_steam(steam_id):
    url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{steam_id}/header.jpg"
    response = requests.get(url)
    if response.status_code == 200:
        return url
    else:
        return None


# Sayfa ayarları
st.set_page_config(layout='wide', page_title='Steam')

# Load the data
game = pd.read_csv('content2_mst.csv')


@st.cache_data
def calculate_cosine_sim(dataframe):
    tfidf = TfidfVectorizer(stop_words='english')
    dataframe['overview'] = dataframe['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(dataframe['overview'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim


cosine_sim_game = calculate_cosine_sim(game)

st.markdown(
    """
    <style>
    .stApp {
        margin: 0;
        padding: 0;
    }
    .css-18e3th9 {
        gap: 0 !important;
    }
    .css-1cpxqw2 {
        padding: 0 !important;
        margin: 0 !important;
    }
    .resizable-image {
        padding: 0;
        margin: 0;
    }
    .resizable-image img {
        width: 100%;
        height: 400px;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/t1KbzWJ9sGkAAAAd/elden-ring-action-rpg.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

col2.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/Z5t0eehZn3gAAAAd/darksiders_2-prince-of-persia.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

col3.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/sctssthXIm8AAAAC/play-game.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

col4.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/BDValJzc6P4AAAAC/rdr2.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

col5.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/COG1mdmj0X0AAAAd/swtor-the-old-republic.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: #A0622D ;">Discover a New World</h1>
        <hr style="border: none; border-top: 2px solid #A0622D;">
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: #999999 ; font-size: 20px;">Level up your gaming experience with our curated game recommendations. From action-packed adventures to mind-bending puzzles, find the perfect game to keep you entertained for hours.</h1>
        <hr style="border: none; border-top: 2px solid #A0622D;">
    </div>
    """,
    unsafe_allow_html=True,
)

if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = 'Home'

def set_active_tab(tab_name):
    st.session_state['active_tab'] = tab_name

home_tab, steam_tab = st.tabs(["Home", "GameSelect"])

with home_tab.container():
    set_active_tab('Home')

with home_tab:
        home_tab.markdown(
        """
        <div class="title-background">Top Games</div>
        <div class="custom-divider"></div>
        """,
        unsafe_allow_html=True,
    )
        home_tab.write("")
        home_tab.write("")
        home_tab.write("")
        home_tab.write("")
        home_tab.write("")
        home_tab.write("")

col1, col2, col3 = home_tab.columns([1,0.8,1])

col1.markdown(
        """
        <iframe width="550" height="430" src="https://www.youtube.com/embed/iaJ4VVFGIa8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        """,
        unsafe_allow_html=True
    )
if not upcoming_games_df.empty:
    col2.write(upcoming_games_df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
col2.write("No upcoming games found.")
home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")
col3.markdown(
    """
    <iframe width="600" height="430" src="https://www.youtube.com/embed/kfYEiTdsyas" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """,
    unsafe_allow_html=True,
)

home_tab.markdown(
    """
    <style>
    .title-background {
        background-color: #A0622D; /* Background color */
        color: black; /* Text color */
        padding: 10px; /* Padding for spacing */
        text-align: center; /* Center align text */
        border-radius: 100px; /* Rounded corners */
        font-size: 32px; /* Font size */
        font-weight: bold; /* Font weight */
    }
    </style>
    """,
    unsafe_allow_html=True
)

home_tab.markdown(
    """
    <style>
    .title-background {
        background-color: #A0622D; /* Background color */
        color: black; /* Text color */
        padding: 10px; /* Padding for spacing */
        text-align: center; /* Center align text */
        border-radius: 100px; /* Rounded corners */
        font-size: 32px; /* Font size */
        font-weight: bold; /* Font weight */
    }
    /* Responsive düzenleme */
    @media (max-width: 1200px) {
        iframe {
            height: 300px; /* Daha küçük ekranlar için iframe yüksekliği */
        }
        .title-background {
            font-size: 24px; /* Daha küçük ekranlar için font boyutu */
            padding: 8px; /* Daha küçük ekranlar için padding */
        }
    }
    @media (max-width: 768px) {
        iframe {
            height: 200px; /* Daha küçük ekranlar için iframe yüksekliği */
        }
        .title-background {
            font-size: 18px; /* Daha küçük ekranlar için font boyutu */
            padding: 6px; /* Daha küçük ekranlar için padding */
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)
)
        home_tab.markdown('<div class="title-background">Play a Game</div>', unsafe_allow_html=True)

        home_tab.write("")
        home_tab.write("")
        home_tab.write("")
        home_tab.write("")
        home_tab.markdown(
    """
    <style>
    .iframe-container {
        width: 850px; /* Aynı genişlik */
        height: 500px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-left: auto; /* Ortalamak için */
        margin-right: auto; /* Ortalamak için */
    }
    .iframe-container iframe {
        width: 1000px; /* Aynı genişlik */
        height: 100%;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    
        home_tab.markdown(
            """
            <div class="iframe-container">
                <iframe src="https://games.construct.net/1690/latest"></iframe>
            </div>
            """,
            unsafe_allow_html=True,
        )


home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")

home_tab.markdown('<div class="title-background">Discover Your Next Adventure!</div>', unsafe_allow_html=True)
home_tab.write("")
home_tab.write("")
with home_tab.container():  # 'home_tab' yerine st.container kullanın

    col1, col2, col3, col4, col5, col6 = st.columns([1, 0.45, 0.45, 0.45, 1,0.5], gap='large')

    # ! airbnb column
    image_airbnb = "https://media1.tenor.com/m/rsSIoLjds9UAAAAC/airbnb-door.gif"
    redirect_airbnb = "https://animerecommendations.streamlit.app/"

    html_airbnb = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_airbnb}" target="_blank">
            <img src="{image_airbnb}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">AIRBNB</div>
        </a>
    </div>
    """

    col2.markdown(html_airbnb, unsafe_allow_html=True)


    # ! imdb column
    image_movie = 'https://media.tenor.com/HJTXKCtOYwgAAAAM/perfect-popcorn.gif'
    redirect_movie = "https://appent-g9qe2nhwhrvvgnhkqybvzq.streamlit.app/"

    html_movie = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_movie}" target="_blank">
            <img src="{image_movie}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">MOVIE</div>
        </a>
    </div>
    """

    col3.markdown(html_movie, unsafe_allow_html=True)


    # ! amazon column
    image_amazon = "https://c.tenor.com/xrld-zE_4IAAAAAd/tenor.gif"
    redirect_amazon = "https://www.amazon.com/Best-Books-of-2024-So-Far/b?ie=UTF8&node=3003015011"
    html_amazon = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_amazon}" target="_blank">
            <img src="{image_amazon}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">BOOK</div>
        </a>
    </div>
    """

    col4.markdown(html_amazon, unsafe_allow_html=True)

    # ! anime column
    image_anime = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2NrbXY3a3ptbDY0d256N2dtN2xkOTV1eXpnMGpvbG5obWlla29mZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/11KzOet1ElBDz2/giphy.webp"
    redirect_anime = "https://animerecommendations.streamlit.app/"

    html_anime = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_anime}" target="_blank">
            <img src="{image_anime}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">ANIME</div>
        </a>
    </div>
    """
    col5.markdown(html_anime, unsafe_allow_html=True)






# Steam Tab
with steam_tab:
    def content_based_recommender_game(title, cosine_sim_game, dataframe):
        indices = pd.Series(dataframe.index, index=dataframe['title'])
        indices = indices[~indices.index.duplicated(keep='last')]
        game_index = indices[title]
        similarity_scores = cosine_sim_game[game_index]
        similarity_scores_df = pd.DataFrame(similarity_scores, index=dataframe.index, columns=["score"])
        game_indices = similarity_scores_df.sort_values(by="score", ascending=False).index[1:11]
        return dataframe.loc[game_indices]


    if 'selected_game' not in st.session_state:
        st.session_state.selected_game = None

    if 'filter_by_genre' not in st.session_state:
        st.session_state.filter_by_genre = None

    if 'recommendations_df' not in st.session_state:
        st.session_state.recommendations_df = None

    # Seçim kutusu ve butonu aşağıya taşıma
    game_options = ["Choose a Game"] + list(game.title.unique())
    selected_game = st.selectbox('Choose a game you like.', options=game_options, index=0)

    if selected_game != "Choose a Game":
        st.write("Would you like to filter the recommendations by genre?")
        filter_by_genre = st.radio("Filter by genre?", ("No", "Yes"), index=0)

        if filter_by_genre == "Yes":
            st.session_state.filter_by_genre = True
            genre_options = ['Action', 'Adventure', 'Casual', 'Indie', 'Racing', 'RPG', 'Simulation', 'Sports', 'Strategy',
                            'Massively Multiplayer']
            selected_genre = st.multiselect('Select Genres', options=genre_options)
        else:
            st.session_state.filter_by_genre = False

        # Stil ayarları
        st.markdown("""
            <style>
            .stButton button {
                background-color: #a3c9f1 !important;
                color: blue !important;
                padding: 10px 24px !important;
                border: none !important;
                cursor: pointer !important;
                text-align: center !important;
                font-size: 16px !important;
                border-radius: 5px !important;
            }
            </style>
        """, unsafe_allow_html=True)

        show_recommendations = st.button('Show Recommendations')

        if show_recommendations and selected_game != "Choose a Game":
            st.session_state.selected_game = selected_game
            try:
                st.session_state.recommendations_df = content_based_recommender_game(title=selected_game,
                                                                                    cosine_sim_game=cosine_sim_game,
                                                                                    dataframe=game)

                if st.session_state.filter_by_genre and selected_genre:
                    genre_pattern = '|'.join(selected_genre)
                    filtered_recommendations_df = st.session_state.recommendations_df[
                        st.session_state.recommendations_df['genres'].str.contains(genre_pattern, na=False)]

                    if filtered_recommendations_df.empty:
                        st.warning("There is no result for these genres.")
                    else:
                        for index, game_col in enumerate(st.columns(5)):
                            if index < len(filtered_recommendations_df):
                                game_row = filtered_recommendations_df.iloc[index]
                                game_id = game_row['app_id']
                                game_title = game_row['title']
                                game_rating = game_row['rating']  # Rating kolonunu ekle
                                game_col.markdown(
                                    f"<a href='https://store.steampowered.com/app/{game_id}' target='_blank'><img src='{get_image_from_steam(game_id)}' style='max-width:100%;'></a>",
                                    unsafe_allow_html=True)
                                game_col.subheader(f"**{game_title}**", divider="violet")
                                game_col.write(f"Rating: {game_rating}")
                else:
                    for index, game_col in enumerate(st.columns(5)):
                        if index < len(st.session_state.recommendations_df):
                            game_row = st.session_state.recommendations_df.iloc[index]
                            game_id = game_row['app_id']
                            game_title = game_row['title']
                            game_rating = game_row['rating']  # Rating kolonunu ekle
                            game_col.markdown(
                                f"<a href='https://store.steampowered.com/app/{game_id}' target='_blank'><img src='{get_image_from_steam(game_id)}' style='max-width:100%;'></a>",
                                unsafe_allow_html=True)
                            game_col.subheader(f"**{game_title}**", divider="violet")
                            game_col.write(f"Rating: {game_rating}")
            except KeyError:
                st.error("Please select a valid game.")
