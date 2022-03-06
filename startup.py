from http import client
from flask_spotify_auth import getAuth, refreshAuth, getToken

#Add your client ID
# CLIENT_ID = "98c167e218bd483891f8638caaca19cb"
CLIENT_ID = 'beab50413afa4569a53c5aa3e58734b1'

#aDD YOUR CLIENT SECRET FROM SPOTIFY
# CLIENT_SECRET = "e40d06af72524208bf0bbb048ba299a3"
CLIENT_SECRET = 'fe36811d8d364e5da17ba9d8e04e833e'

#Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
# CALLBACK_URL = "http://localhost"

CALLBACK_URL = "http://127.0.0.1"

#Add needed scope from spotify user
# SCOPE = "streaming user-read-birthdate user-read-email user-read-private"
SCOPE = "user-read-private"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA


def getClientInfo():
    return (CLIENT_ID, CLIENT_SECRET)