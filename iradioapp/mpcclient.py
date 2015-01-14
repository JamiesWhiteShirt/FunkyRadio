from mpd import MPDClient, CommandError, ConnectionError
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False

_shuffle = False
_consume = False

client = None

def init():
	global client
	if not client:
		client = MPDClient()
		try:
			client.connect(host=HOST, port=PORT)
		except SocketError:
			client = None
			print("Failed to establish connection to mpc server at %s:%s" % (HOST, PORT))
			return
		if PASSWORD:
			try:
				client.password(PASSWORD)
			except CommandError:
				client = None
				print("Failed to authenticate connection to mpc server at %s:%s with password" % (HOST, PORT))
				return
		client.consume(1 if _consume else 0)
		client.shuffle(1 if _shuffle else 0)

def checkConnection(func, *params):
	global client
	if not client:
		init()
	try:
		return func(*params)
	except ConnectionError:
		client = None
		init()
		try:
			return func(*params)
		except ConnectionError:
			return


def _isPlaying():
	global client
	r = client.status()
	if not r:
		return False
	return r["state"] == "play"

def isPlaying():
	return checkConnection(_isPlaying)

def isShuffeling():
	return _shuffle

def isConsuming():
	return _consume

def _playPause():
	global client
	if isPlaying():
		client.pause()
	else:
		client.play()

def playPause():
	checkConnection(_playPause)

def next():
	global client
	checkConnection(client.next)

def previous():
	global client
	checkConnection(client.previous)

def setVolume(vol):
	global client
	checkConnection(client.setvol,vol)

def addSong(url):
	global client
	checkConnection(client.add, url)

def setShuffle(state):
	global client
	checkConnection(client.shuffle, state)

def getCurrent():
	global client
	return checkConnection(client.currentsong)

def getPlaylist():
	global client
	return checkConnection(client.playlistinfo)


