import spotipy
from tkinter import *
import config
import pymongo

#// TODO Try to plug it with MongoDB and rechack data structure
# TODO Create GUI, try to read existing data from db and show at GUI boxes
# TODO Focus on array data, eg artist in festival, how to read all



########### GUI ###################

app = Tk()
app.title('MongoDB')
app.geometry('900x700')
app.resizable(0,0)

#### Festival List BOX ####

festival_box = LabelFrame(app, text= 'Festival', bd=1, relief= GROOVE, labelanchor= 'n')
festival_box.grid(row= 0, column=0)
scrollbar = Scrollbar(festival_box, orient= 'vertical')
festival_list = Listbox(festival_box, height=15, width=30, yscrollcommand=scrollbar.set)
festival_list.grid(row= 0, column= 0, padx= 50, pady= 30)
scrollbar.config(command= festival_list.yview)
scrollbar.grid(row= 0, column= 1)


# Artist List Box

artist_box = LabelFrame(app, text= 'Artist', bd=1, labelanchor= 'n')
artist_box.grid(row= 0, column=1)
scrollbar_artist = Scrollbar(artist_box, orient= 'vertical')
artist_list = Listbox(artist_box, height=15, width=30, yscrollcommand=scrollbar_artist.set)
artist_list.grid(row= 0, column= 1, padx= 50, pady= 30)
scrollbar_artist.config(command= artist_list.yview)
scrollbar_artist.grid(row= 0, column= 2)


# Track List Box

track_box = LabelFrame(app, text= 'Track', bd=1, labelanchor= 'n')
track_box.grid(row= 0, column=2)
scrollbar_track = Scrollbar(track_box, orient= 'vertical')
track_list = Listbox(track_box, height=15, width=30, yscrollcommand=scrollbar_track.set)
track_list.grid(row= 0, column= 2, padx= 50, pady= 30)
scrollbar_track.config(command= track_list.yview)
scrollbar_track.grid(row= 0, column= 3)


# Festival to plot list box
plotting_box = LabelFrame(app, text= 'Selecting festival to plot', bd= 1, labelanchor= 'n')
plotting_box.grid(row= 1, column= 0, columnspan= 2, padx= 20, pady= 40)
scrollbar_plotting = Scrollbar(plotting_box, orient= 'vertical')
plotting_list = Listbox(plotting_box, height= 15, width= 60, yscrollcommand= scrollbar_plotting.set)
plotting_list.grid(row= 1, column=0, padx= 50, pady= 30)
scrollbar_plotting.config(command= plotting_list.yview)
scrollbar_plotting.grid(row=1, column= 1)
# colspan=3



#### Button ####
# Festival add delete button

# Artist Add Del Button



#### Check box for plotting festival


# Plot button
btn_plot = Button(app, text= 'Plot', command= '', width= 10, height=3)
btn_plot.grid(row= 1, column= 2)
app.mainloop()

















class FetchSpoty():
    
    
    def __init__(self, client_id = None, client_secret = None) -> None:
        
        if client_id != None and client_secret != None:
            #try:
            client_cred = spotipy.SpotifyClientCredentials(client_id, client_secret)
            self.sp = spotipy.Spotify(auth_manager= client_cred)
            #except:
        #else:
            #raise 'Client ID and SECRET is Required'
        else:
             self.sp = spotipy.Spotify()
        
        self.required_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                     'liveness', 'valence', 'tempo', 'uri']
        
        
    #def search_artist
    def fetch_features(self, track_uri) -> list: # maybe return a dict
        
        self.track_featres = self.sp.audio_features(track_uri)[0]
        #// TODO restructure to list of track_features
        song_features = {}
        self.track_feature_list = []
        
        for i in self.required_features:
            song_features[i] = self.track_featres[i]
            
        self.track_feature_list.append(song_features.copy())
        
        # TODO Handling of track usi come as a list, loop throgh list and append all features to return
        # ! This return in list, why dont just ret as a dict
        return self.track_feature_list
        
        
            
    def fetch_artist_tracks(self, artist_uri):
        
        # artist_top_tracks return dict with key is 'tracks', which contain list of 10 tracks
        self.top_tracks_list = []
        artist_tracks = self.sp.artist_top_tracks(artist_id= artist_uri, country= 'TH')['tracks']
        #// TODO Restrucre artist_tracks data (above this)
        print(artist_tracks)
        print(type(artist_tracks))
        for i, k in enumerate(artist_tracks):
            top_tracks = {}
            top_tracks['artist'] = artist_tracks[i]['artists'][0]['name']
            top_tracks['uri'] = artist_tracks[i]['uri']
            
            self.top_tracks_list.append(top_tracks.copy())
        
            
        
        return self.top_tracks_list
    
    
    
    
    

    

############## User's playist analytics zone ##################
    """
    dict key for each track
self.tracks_list.append({
    'name': track_name,
    'artist': track_artist,
    'added_date': track_added_date,
    'uri': track_uri 
})
    """                   
    """
    DONE
    ต้องเปลี่ยนเพื่อให้ไม่เก็บ Track details ซับซ้อน โดยที่ a_pl_dict['tracks'] เก็บแค่ uri 
    เพื่อนำ uri ไปเสิชหา detail ใน collection['tracks'] เท่านั้น
    """
    
    def fetch_user_playlist(self ,userid: str, get_features = True) -> list:
        "This method return a list of  playist which contained uri, name, tracks (list) as a dict keys"
        # create empty list and dict for append details
        pl_list = []
        a_pl_dict = dict()

        playlists = self.sp.user_playlists(userid)
        while playlists:
            for playlist in playlists['items']:

                a_pl_dict['uri'] = playlist['uri']
                a_pl_dict['name'] = playlist['name']
                
                # Fetch tracks in playlist
                # TODO// Call fetch_tracks_from_playlist()
                if get_features == True:
                    
                    #a_pl_dict['tracks'] = self.fetch_tracks_in_playlist(playlist_uri = playlist['uri'])
                    a_pl_dict['tracks'] = self.fetch_tracks_in_playlist(playlist_uri = playlist['uri'], uri_only= True)
                
                else:
                    a_pl_dict['tracks'] = []
                
                #print(a_pl_dict)
                pl_list.append(a_pl_dict.copy())
                #print(pl_list)

            if playlists['next']:
                playlists = self.sp.next(playlists)
            else:
                playlists = None
                print('Fetching complete')

        return pl_list
        
        
    def fetch_tracks_in_playlist(self, playlist_uri= None, uri_only= bool):
        
        """ uri_only false when used with mongodb database 
            in case that already have separating song collection
            uri_only == False will return list of dict {uri: 'track_uri'}
        """
        self.tracks_list = []
        tracks = self.sp.playlist_tracks(playlist_uri= playlist_uri)
        
        # loop through all tracks and get details
        for i in range(len(tracks['items'])):
            if uri_only == False:
                track_name = tracks['items'][i]['track']['name']
                track_artist = tracks['items'][i]['track']['artists'][0]['name']
                # * maybe chack track_artist to be [], thats collect all feauturing artsits, to fetch using for loop in range len
                track_added_date = tracks['items'][i]['added_at']
                track_uri = tracks['items'][i]['track']['uri']
                track_n_artists = len(tracks['items'][i]['track']['artists'])
                print('Number of artist collaborate', track_n_artists)

                # set all value dict and append dicts to a list element 

                self.tracks_list.append({
                    'name': track_name,
                    'artist': track_artist,
                    'added_date': track_added_date,
                    'uri': track_uri 
                })
                
            else:
                track_uri = tracks['items'][i]['track']['uri']
                self.tracks_list.append({'uri': track_uri})
    
        return self.tracks_list
        

class MongoConnect():
    
    """This class is called by button function 
    """
    
    def __init__(self, url, pwd) -> None:
        # connect
        url = url.replace('<password>', pwd)
        self.client = pymongo.MongoClient(url)
        # select each collection to vars
        self.db = self.client['Spoty']
        self.db_col_festival = self.db['festival']
        self.db_col_artist = self.db['artist']
        self.db_col_track = self.db['track']
        
        self.collection_params = {
            'festival': self.db_col_festival,
            'artist': self.db_col_artist,
            'track': self.db_col_track
        }
        
        return
    
    def db_add(self, col: str, doc: list):
        
        db_id = self.collection_params[col].insert_many(doc)
        
        return db_id
    
    
    def db_del(self, col, query: list):
        
        if isinstance(query) == list:
            for i in range(len(query)):
                db_id = self.collection_params[col].delete_one(query[i])
        else:
            db_id = self.collection_params[col].delete_one(query)
            
        return db_id
    
    # called when change dj uri
    def db_update(self, col, query: list, new_value: dict):
        
        new_value = {
            '$set': new_value
        }
        for i in range(len(query)):
            db_id = self.collection_params[col].update_one(query[i], new_value)
        
        return db_id
    
    # used when open program to show all festivals in database
    def db_read_all(self, col, ):
        return
    
    # read all use in case to show all djs, all tracks feature
    # when festival was selected
    def db_read_specific(self, col):
        return

    # # read all data in each collection 
    # def db_read_all_at_start():
    #     return

if __name__ == '__main__2':
    """
    เมื่อ cursor จิ้มที่ festival ไหน ให้ไป read DJ ในส่วนนั้น
    เช่นกันกับ DJ เมื่อจิ้มอันไหน ให้แสดงรายชื่อเพลง
    """
    
    ### DUMMY DOC ###
    firstfes = [{'name': 'firstfes',
                'artist': [{'uri': 'spotify:artist:0AvGycOEDZTaBFLCaiGd9S', 'name': 'dj1'}]
            }]
    firstartist = [{'name': 'dj1',
                   'uri': 'spotify:artist:0AvGycOEDZTaBFLCaiGd9S'}]
    
    from pprint import pprint
    
    # charlie artist uri = 'spotify:artist:7wO5pqunGUkJCQsJohcteb
    uri = 'spotify:track:1xddmaN7Ivc2SQ940oBskZ'
    
    #pluged = fetch_spoty()
    pluged = FetchSpoty(config.sptf_client_id, config.sptf_client_secret)
    #test = pluged.fetch_features(uri)
    top_tracks = pluged.fetch_artist_tracks('spotify:artist:0AvGycOEDZTaBFLCaiGd9S')
    print(top_tracks)
    print('total tracks :',len(top_tracks))
    
    
    db = MongoConnect(config.mongodb_url, config.mongo_pwd)
    # พยายามทำให้ festival ที่เขียนข้างล่างนี่เป็นตัวแปร ที่เปลี่ยนตาม หมวดของ listbox ที่คลิ้ก
    # โดยอาจจะใช้เป็น param ว่าคลิ้ก add/del จากกล่องไหน
    db.db_add('festival', firstfes)
    db.db_add('artist', firstartist)

    
    features = []
    
    ####  Use this loop to create data at DB #####
    for i in range(len(top_tracks)):
        print('-----------------')
        feature = pluged.fetch_features(top_tracks[i]['uri'])[0]
        print('features ', feature)
        features.append(feature)
        
    db.db_add('track', features)
        
    # [features.append(pluged.fetch_features(top_tracks[x]['uri'])) for x in range(len(top_tracks)) ]
    # pprint(features)
    # pprint(features[0])        
    # pprint(features[0][0])        
