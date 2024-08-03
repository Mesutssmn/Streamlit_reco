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

st.markdown(
    """
    <div class="resizable-image">
        <img src="https://camo.githubusercontent.com/d6071165f118647cd11619ed34fb9f18fe75e2b48656296ee8de22fcfdf1a9cd/68747470733a2f2f6d656469612e74656e6f722e636f6d2f2d6d5f70797974655f674541414141642f77656c636f6d652d7265647461696c732e676966" alt="Resim">
    </div>
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
        <h1 style="color: #0002d1 ;">Discover a New World</h1>
        <hr style="border: none; border-top: 2px solid darkblue;">
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: #999999 ; font-size: 20px;">Level up your gaming experience with our curated game recommendations. From action-packed adventures to mind-bending puzzles, find the perfect game to keep you entertained for hours.</h1>
        <hr style="border: none; border-top: 2px solid darkblue;">
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

    col1, col2, col3 = home_tab.columns([2,2,1])  # Genişlikleri ayarlamak için oranları değiştirdik

    with col1:
        col1.markdown(
        """
        <style>
        .custom-header {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .custom-divider {
            width: 50%;
            border: 1px solid #0002d1;
            margin-bottom: 1rem;
        }
        </style>
        <div class="custom-header">Top Games</div>
        <div class="custom-divider"></div>
        """,
        unsafe_allow_html=True,
    )
        if not upcoming_games_df.empty:
            col1.write(upcoming_games_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            col1.write("No upcoming games found.")

    with col2:
        col2.markdown(
        """
        <style>
        .custom-header {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .custom-divider {
            width: 100%;
            border: 1px solid #0002d1;
            margin-bottom: 1rem;
        }
        </style>
        <div class="custom-header">Play a Game</div>
        <div class="custom-divider"></div>
        """,
        unsafe_allow_html=True,
    )
        


        
        col2.markdown(
    """
    <style>
    .iframe-container {
        width: 150%;
        height: 430px;
        display: flex;
        justify-content: left;
        align-items: left;
    }
    .iframe-container iframe {
        width: 70%;
        height: 100%;
        border: none;
    }
    </style>
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
home_tab.markdown(
        """
        <style>
        .custom-header {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .custom-divider {
            width: 100%;
            border: 1px solid #0002d1;
            margin-bottom: 1rem;
        }
        </style>
        <div class="custom-header">If You Want to Do Something Else, You Can Visit These Pages.</div>
        <div class="custom-divider"></div>
        """,
        unsafe_allow_html=True,
    )      


col1, col2, col3, col4, col5 = home_tab.columns(5)

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
