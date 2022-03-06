from email.policy import default
from pickletools import string1
from re import search
from xml.etree.ElementTree import tostring
import spotipy
import heapq
from collections import defaultdict
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="81af6fc56a07407585d60cd986bfd09b",
                                                           client_secret="cfb42163778148aba7c7820fdbf3f20d"))





def getPlaylists(name):
    offset = 0
    resultList = []
    for i in range(2):
        results = sp.search(q=''+name+'', type="playlist", limit=50, offset = offset)
        resultList.append(results)
        offset += 50

    return resultList

def searchPlaylist(playlist_id, songDict, artistDict):
    tracks = sp.playlist_items(playlist_id=playlist_id)
    for track in tracks['items']:
        try:
            songDict[track['track']['name']] += 1
            artistDict[track['track']['name']] = track['track']['artists'][0]['name']
        except:
            pass

    return songDict,artistDict

def getSongs(name):
    resultList = getPlaylists(name=name)
    songList = []
    songDict = defaultdict(int)
    artistDict = defaultdict()
    for each in resultList:
        for playlist in each['playlists']['items']:
            songDict, artistDict = searchPlaylist(playlist['id'], songDict, artistDict)

    for key in songDict:
        songList.append((key, songDict[key], artistDict[key]))
    songList.sort(key=lambda y: y[1], reverse=True)
    return songList


def formatString(songList):

    songDict = {}

    for idx, val in enumerate(songList):
        tempDict = {}
        tempDict['track_name'] = val[0]
        tempDict['artist_name'] = val[2]
        tempDict['frequency'] = val[1]
        songDict[idx + 1] = tempDict

    return songDict











from flask import Flask, redirect, request, render_template, url_for
import startup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        return check_work(request.form.get("emotion"))
    
    return render_template("index.html")

# @app.route("/find_playlist/<emotion>")
def check_work(emotion):

    retSongList = []
    retSongList = getSongs(name=emotion)

    # retSongList = [i for i in range(50)]
    # if nothing was returned from the function, return the default page (has error message)
    if len(retSongList) == 0:
        return render_template("results.html")

    
    if len(retSongList) > 50:
        retSongList = retSongList[0:50]
    retSongList = formatString(retSongList)


    return render_template("results.html", track_list=retSongList)


    

#NOT WORKING, SPOTIFY SIGNIN AUTHENTICATION!
# @app.route('/login/',methods=['POST'])
# def index():
#     response = startup.getUser()
    
#     return redirect(response)

# # @app.route('/callback/<code:byte>')
# @app.route('/callback/')
# def inddex():
#     temp_str = (request.args['code']).encode('UTF-8')


#     # startup.getUserToken(b''+temp_str+'')
#     # startup.getUserToken(code)
#     startup.getUserToken(temp_str)

#     print("access token: ", startup.getAccessToken())

#     return render_template("index.html")

# @app.route('/enter_emotions')
# def get_emotion():
#     return render_template("emotions.html")
