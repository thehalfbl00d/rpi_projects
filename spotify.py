import time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import datetime

#for matrix
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT, TINY_FONT, SINCLAIR_FONT


load_dotenv()

client_id1 = os.getenv("SPOTIPY_CLIENT_ID")
client_secret1 = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_url1 =os.getenv("SPOTIPY_REDIRECT_URI")

scope1 = "user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id1,
                                               client_secret = client_secret1,
                                               redirect_uri= redirect_url1,
                                               scope=scope1))
                                               
#port settings max7219 display                                           
serial = spi(port = 0, device =0, gpio=noop())
device = max7219(       serial,
                        height = 16,
                        width = 32,
                        block_orientation=-90,
                        rotate=0,           
                        blocks_arranged_in_reverse_order=False,
                        contrast=20)
                                               
def song_api_datacollected():

    everything = sp.current_user_playing_track()

    if everything != None: 
        song_id  = everything["item"]["id"]
        song_name = everything["item"]["name"]
        artist_name = everything["item"]["artists"][0]["name"]
        is_playing = everything["is_playing"]
            
        response = {
                        "song_name": song_name,
                        "artist": artist_name,
                        "status": is_playing,
                        "song_id": song_id
                                } 
        return(response)
                            
    else: 
        return None

# has to be run when triggered, pass a parameter i.e. the string to display it 
def max7219_screen_vomit(msg):
        show_message(device, msg,fill="white", font=proportional(LCD_FONT))

def show_time():
    with canvas(device) as draw:
        draw.text((10,8), "(||)", fill="white")

while 1:
    song_switch = 0
    current = song_api_datacollected()

    if current == None or current['status'] != True:

        show_time()
    else:
        max7219_screen_vomit(f"{current['song_name']} by {current['artist']}")
    time.sleep(1)
