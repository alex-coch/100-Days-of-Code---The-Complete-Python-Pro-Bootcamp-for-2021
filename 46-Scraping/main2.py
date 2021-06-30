import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="1da2a06e7f61487bbed4df8813832005",
        client_secret="4781f347ab1649018e9d0c756c98e23d",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]