import tkinter
import random
import spotipy
import spotipy.util as util


## Application specific variables
print('Create playlist with random tracks from your saved songs.\n')
print('Enter client/secret IDs. If you are not a Spotify dev., leave blank and push enter.')
print('You will be prompted to give this application access to your Spotify account.\n')
clientID = input('Enter your client ID: ')
secretID = input('Enter your client secret ID: ')

''' If using default Client/Secret ID - Enter here
if clientID == '':
        clientID = ''
        secretID = ''
'''

## Spotify user details
user = input('Enter your Spotify username: ')
print('\nTo obtain playlist ID, right click on playlist and select Copy Playlist URI.')
playlistID = input('Enter your Playlist ID: ')[-22:]


                ## This part needs to be modified
                ## Asking novice EU to navigate to browser is insane
## Authenticating user
#https://developer.spotify.com/web-api/using-scopes/
scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public' 
token = util.prompt_for_user_token(user, scope, clientID, \
            secretID, 'https://www.google.com.au')

sp = spotipy.Spotify(auth=token)
sp.trace = False



## Create list variables
## There's probably a neater way to do this but CBF
tracks = []
tracksA = []
curPlay = []
curPlayA = []
track_ids = []
artistList = []

## Get tracks in library
print('\nGetting library tracks...')
trackIDS = sp.current_user_saved_tracks(limit=50)

while trackIDS['next'] != None:
        trackIDS = sp.next(trackIDS)

        ## Strip out track ID's
        for i in trackIDS['items']:
            tracks.append(i['track']['uri'])

for i in tracks:
        tracksA.append(i[14:])
            

## Get list of current songs in playlist
### This will stop a song being in the playlist twice in a row
# if playlist != ''
#curTracks = sp.user_playlist_tracks(user, playlistID)
#for i in curTracks['items']:
#    curPlay.append(i['track']['uri'])
#for i in curPlay:
#    curPlayA.append(i[14:])

## Creates random list of 30 songs
#Ensures no duplicate artists or tracks in selection
print('Selecting tracks at random...')
while True:
        trackID = random.choice(tracksA)
        ranTrack = sp.track(trackID)

        if trackID in track_ids:
                continue

        for i in ranTrack['artists']:
                if artistList.count(i['id']) > 0:
                        continue
                #elif curPlayA.count(i['id']) > 0:
                        #continue
                else:
                        artistList.append(i['id'])
                        track_ids.append(trackID)
                        
                if len(ranTrack['artists']) > 1:
                        break

        if len(track_ids) == 30:
                break


#Sample of 30 tracks - can include duplicate artists
#track_ids = random.sample(tracksA, 30)

## Deletes current tracks from playlist
#sp.user_playlist_remove_all_occurrences_of_tracks(user, playlistID, curPlayA)


## Creates new playlist
if playlistID == '':
        print('Creating new playlist...')
        sp.user_playlist_create(user, 'UserRandom')

        # Gets ID of created playlist
        userPlaylist = sp.user_playlists(user, limit=50)

        for key in userPlaylist['items']:
                if key['name'] == 'UserRandom':
                        playlistID = key['id']


## Adds tracks to a playlist
print('Adding tracks to playlist...')
sp.user_playlist_replace_tracks(user, playlistID, track_ids)


# This takes a while to complete
## Might be better way to complete

## Confirms songs added to playlist
testListA = []
print('\nTracks added to playlist:')
for i in track_ids:
        testListA.append(sp.track(i))

for i in testListA:
        for key in i['artists']:
                print(key['name'], "-", i['name'])

cont = input("\nPress Enter to close program.\n>")

