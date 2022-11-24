import spotipy
from tkinter import *
import config
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint

#// TODO Try to plug it with MongoDB and rechack data structure
#// TODO Create GUI, 
#// TODO try to read existing data from db and show at GUI boxes
#// TODO Function Add button which insert to GUI and Add to DB (festival and artist need to separete function?)
# // Done ? Change Database class to be an treasholder to get values for each keys ???????????
#// ! artist dup
#// TODO Database design change????? how?

#// ? Artist arrtibutes, only uri and get name by fetching, or input both name and uri
#// ? 1 merge track collection to be an array in artist collection
#// TODO ADD artist buttun and function
    #// TODO get artist name function
    #// TODO Remove Artist key frin track array object, 
    #// TODO Get current cursor () return turn name 
    
#// TODO Recheck fetch features function is it return as list >> then call it at artist_confirm butto
#// TODO READ Each DJ in festival when cursored at festival (fetch_data_cursor_select()) 
    #// TODO Fetch all artist in festival name
#// TODO READ ALL SONG FEATURE WHEN ARTIST WAS SELECT
#// TODO Delete button (artist), change to delete artist from selected festival
#// TODO Artist click confirm() insert name 
#// TODO Duplicate artist, dont add if artist existing
#// TODO Add festival list to lower list box  
    #// TODO at fetch_all_at_open ->> insert to lower list box 
    #// TODO add or delete festival button -> insert and delete from lower list box
# TODO// Filter and plot
    #// TODO multiple selection to lower list box
    #// ? HOW TO PLOT,, find each festivals and set to dataframe
    
# TODO Agg average audio_features for each dj then festival
    # ? IF CAN NOT AGG IN CURRENT DATABASE STRUCTURE, CREATE NEW FUNCTION TO REDESIGN DB STRUCTURE
# * เขียน function ใหม่ในตอน fetch_track ให้มันหาค่า average ของ features ทั้งหมดออกมา
# * เสร็จแล้ว เขียน avg_[features]: value ลงใน db เหมือน popuritiy (ทำในfunction เดียวกับตอน popularity เลย)
# * โดยใช้ตัวแปรในรูปแบบ avg_dance = SpotyClass.avg_dance <--- Get arrtibutes มันมา 
#// * Focus on array data, eg artist in festival, how to read all


class FetchSpoty():
    """FetchSpoty Class contains methods that involed to the spotify api, using spotipy library
    Mathods are filtering only needed data and create new structure of datas.
    Then it will return datas that's fit in app and db term
    Class methods will called from button and database function
    """
    
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
                     'liveness', 'valence', 'tempo']#, 'uri']
        
        
    def fetch_features(self, track_uri) -> dict:
        
        self.track_featres = self.sp.audio_features(track_uri)[0]
        self.song_features = {}
        
        for i in self.required_features:
            self.song_features[i] = self.track_featres[i]
            
        
        return self.song_features.copy()
        
        
    def fetch_artist_tracks(self, artist_uri, get_features= bool):
        
        # get artist name and details
        self.artist_details = self.sp.artist(artist_uri)
        self.artist_name = self.artist_details['name']
        self.popularity = self.artist_details['popularity']
        
        # artist_top_tracks return dict with key is 'tracks', which contain list of 10 tracks
        self.top_tracks_list = []
        artist_tracks = self.sp.artist_top_tracks(artist_id= artist_uri, country= 'TH')['tracks']

        for i, k in enumerate(artist_tracks):
            top_tracks = {}
            top_tracks['uri'] = artist_tracks[i]['uri']
            top_tracks['name'] = artist_tracks[i]['name']
            if get_features:
                top_tracks['features'] = self.fetch_features(top_tracks['uri'])
            self.top_tracks_list.append(top_tracks.copy())
            
        return self.top_tracks_list
    

    

############## User's playist analytics zone ##################
    
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
                if get_features == True:
                    
                    a_pl_dict['tracks'] = self.fetch_tracks_in_playlist(playlist_uri = playlist['uri'], uri_only= True)
                
                else:
                    a_pl_dict['tracks'] = []
                
                pl_list.append(a_pl_dict.copy())

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
        
# DATABASE CLASS
class MongoConnect():
    
    """All about database connections are in this class methods
    Method created to be placeholders for any CRUDs 
    which is will called by button function in purposes
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
        
        if isinstance(doc, list):
            db_id = self.collection_params[col].insert_many(doc)
        else:
            db_id = self.collection_params[col].insert_one(doc)
        
        return db_id
    
    def db_add_festival(self, name, year, col= 'festival'):
        
        doc = {'name': name, 'year': year, 'artist': []}
        db_id = self.collection_params[col].insert_one(doc)
        
        return
    
    
    def db_add_artist(self, artist_name, artist_uri, popularity , fes_name, fes_year, track: list, col1= 'artist', col2= 'festival'): 
        """function to add artist to db, if artist already exist in db which mean
        they were in others festival, This function will not fetch its details 
        but add ref_id to artist instead """
        # Check if arist existing in DB
        query = {'name': artist_name}
        ret = self.collection_params[col1].find_one(query)
        if ret == None:
            # add new artist
            artist_doc = {'name': artist_name, 'uri': artist_uri, 'popularity': popularity, 'track': track}
            artist_ret = self.collection_params[col1].insert_one(artist_doc)
            artist_id = artist_ret.inserted_id
            print('-------------')
            print('ID :',artist_id)
            print(type(artist_id))
        
        # else: get object id to refer in festival collection   
        else:
            print('Artist details in database already')
            artist_id = ret['_id']
        
        # push artist id to festival
        festival_doc = {'name': artist_name, 'ref_id': artist_id}
        db_id = self.collection_params[col2].update_one(
            {'name': fes_name, 'year': fes_year},
            {'$push': {'artist': festival_doc}}
        )
        
        return db_id
        
    def db_del_artist_from_festival(self, fes_name, artist_name):
        
        self.collection_params['festival'].update_one(
            {'name': fes_name},
            {'$pull': {'artist': {'name': artist_name}}}
        )
        
        return
    def db_del(self, col, query: list):
        
        if isinstance(query, list):
            for i in range(len(query)):
                db_id = self.collection_params[col].delete_one(query[i])
        else:
            db_id = self.collection_params[col].delete_one(query)
        print(db_id)
    
            
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
    def db_read_all(self, col):
        #data = [x for x in self.collection_params[col].find()]
        data = []
        for d in self.collection_params[col].find():
            data.append(d)
        
        return data
    

    def db_read_artist_from_fes(self, fes_name, year) -> list:
        # get all artist name in fesname
        name = self.collection_params['festival'].find_one({'name': fes_name, 'year': year})['artist']
        lst_artists = [d['name'] for d in name]
        # return lsit of name
        return lst_artists
    
    def db_read_track_from_artist(self, artist_name):
        tracks = self.collection_params['artist'].find_one({'name': artist_name})['track']
        lst_tracks = [t['name'] for t in tracks]
        #for i in tracks:
            
        return lst_tracks
    
    def db_read_artist_popularity(self, artist_name) -> int:
        pops = self.collection_params['artist'].find_one({'name': artist_name})['popularity']
        return pops
    
    def db_read_track_list(self, artist_name):
        data = self.collection_params['artist'].find_one({'name': artist_name})['track']
        return data
    
    # def db_read_dj_data(self, artist_name):


########### GUI ###################

app = Tk()
app.title('MongoDB')
app.geometry('900x700')
app.resizable(0,0)

#### Festival List BOX ####

def get_name_for_next_listbox(lst_box_name):
    if lst_box_name == 'festival':
        name_year = festival_list.get(festival_list.curselection())
        if ',' in name_year:
            name = name_year.split(',')[0]
            year = int(name_year.split(',')[1].strip())
        print(name)
    
        # clear artist box
        artist_list.delete(0, END)
        # read all artist in fesname and insert it to artst box
        artists_name = mongo_plug.db_read_artist_from_fes(name, year)
        print(artists_name)
        print(type(artists_name))
        for i in artists_name:
            print(i)
            artist_list.insert(0, i)
    elif lst_box_name == 'artist':
        print('!!!!!!!!! Artist selected !!!!!!!!!')
        name = artist_list.get(artist_list.curselection())
        if ',' in name: 
            name = name.split(',')[0]
        print(name)
        track_list.delete(0, END)
        # get tracks by artist
        tracks_name = mongo_plug.db_read_track_from_artist(name)
        for i in tracks_name:
            print(i)
            track_list.insert(0, i)
        # insert tracks to track_list

festival_box = LabelFrame(app, text= 'Festival', bd=1, relief= GROOVE, labelanchor= 'n')
festival_box.grid(row= 0, column=0)
scrollbar = Scrollbar(festival_box, orient= 'vertical')
festival_list = Listbox(festival_box, height=15, width=30, yscrollcommand=scrollbar.set, exportselection= False)
festival_list.grid(row= 0, column= 0, padx= 50, pady= 30)
scrollbar.config(command= festival_list.yview)
scrollbar.grid(row= 0, column= 1)

# test bind for get item in list box
festival_list.bind('<<ListboxSelect>>', lambda x: get_name_for_next_listbox('festival'))

# Artist List Box

artist_box = LabelFrame(app, text= 'Artist', bd=1, labelanchor= 'n')
artist_box.grid(row= 0, column=1)
scrollbar_artist = Scrollbar(artist_box, orient= 'vertical')
artist_list = Listbox(artist_box, height=15, width=30, yscrollcommand=scrollbar_artist.set, exportselection= False)
artist_list.grid(row= 0, column= 1, padx= 50, pady= 30)
scrollbar_artist.config(command= artist_list.yview)
scrollbar_artist.grid(row= 0, column= 2)

artist_list.bind('<<ListboxSelect>>', lambda x: get_name_for_next_listbox('artist'))

# Track List Box

track_box = LabelFrame(app, text= 'Track', bd=1, labelanchor= 'n')
track_box.grid(row= 0, column=2)
scrollbar_track = Scrollbar(track_box, orient= 'vertical')
track_list = Listbox(track_box, height=15, width=30, yscrollcommand=scrollbar_track.set)
track_list.grid(row= 0, column= 2, padx= 50, pady= 30)
scrollbar_track.config(command= track_list.yview)
scrollbar_track.grid(row= 0, column= 3)


# Festival to plot list box
plotting_box = LabelFrame(app, text= 'Select festival to plot', bd= 1, labelanchor= 'n')
plotting_box.grid(row= 1, column= 0, columnspan= 2, padx= 20, pady= 40)
scrollbar_plotting = Scrollbar(plotting_box, orient= 'vertical')
plotting_list = Listbox(plotting_box, height= 15, width= 60, yscrollcommand= scrollbar_plotting.set, selectmode= MULTIPLE)
plotting_list.grid(row= 1, column=0, padx= 50, pady= 30)
scrollbar_plotting.config(command= plotting_list.yview)
scrollbar_plotting.grid(row=1, column= 1)


#### Button ####
# Festival add delete button
btn_add_fes = Button(festival_box, text= 'Add', command= lambda: add_fes_click(festival_list))
btn_add_fes.grid(row= 1, column=0)

btn_del_fes = Button(festival_box, text= 'Delete', command= lambda: del_click(festival_list, col= 'festival'))
btn_del_fes.grid(row= 1, column=1)


# Artist Add Del Button
btn_add_artist = Button(artist_box, text= 'Add', command= lambda: add_artist_click(artist_list))
btn_add_artist.grid(row= 1, column=1)

btn_del_artist = Button(artist_box, text= 'Delete', command= lambda: del_click(artist_list, col= 'artist'))
btn_del_artist.grid(row= 1, column=2)


def plot_click(lst_box= plotting_list):
    
    """Plot button function, getting all selected items in plotting list box,
    Then iterate each item and call db_read function to fetch artists and poplaraites.
    Calculate mean of artists in festival and append it to prepared dataframe 
    """

    # create dataframe
#    df = pd.DataFrame(columns=['festival_name', 'festival_year', 'avg_popularity', 
#                               'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
#                               'instrumentalness', 'liveness', 'valence', 'tempo'])
    df = pd.DataFrame(columns=['festival_name', 'festival_year', 'avg_popularity', 
                               'danceability', 'energy', 'speechiness', 'acousticness',
                               'instrumentalness', 'liveness', 'valence', 'tempo'])
    
    
    fes_lst_index = lst_box.curselection()
    for ind in fes_lst_index:
        # create list for popularities
        lst_pops = []
        i = lst_box.get(ind)
        print('--------------------------')
        print(i)
        name = i.split(',')[0]
        year = int(i.split(',')[1].strip())
        print('Name :', name)
        print('Year :', year)
        
        # find data and plot
        # get artist who play at festival
        lst_artists = mongo_plug.db_read_artist_from_fes(name, year)
        #loop throgh list of artist and get popularities
        for i in lst_artists:
            pops = mongo_plug.db_read_artist_popularity(i)
            lst_pops.append(pops)
            print('#################')
            print(lst_pops)
            print('for pop', i , pops)
        
        avg_pop = (sum(lst_pops)/ len(lst_pops))/100
        print('Check Average')
        print('Average :',avg_pop)
        
        lst_for_df = [name, year, avg_pop]
        # cal average features
        for i in cal_average_to_plot(lst_artists):
            lst_for_df.append(i)
        
        # Add average to list for df
        # df.loc[len(df)] = [name, year, avg_pop].copy()
        print(df)
        print(lst_for_df)
        df.loc[len(df)] = lst_for_df

    print(df)
    # plot bar df
    df.sort_values(by= ['festival_year'], inplace= True)
    df.set_index(['festival_year', 'festival_name'], inplace= True)
    ax = df.plot(kind= 'bar')
    ax.set_title('Average Audio Features of top tracks from dj which play in each music festivals')
    plt.show()
    
    return

def cal_average_to_plot(dj_name_list):
    
    # dct_lst = {'danceability': [], 'energy': [] , 'loudness': [], 'speechiness': [], 'acousticness': [], 'instrumentalness': [], 'liveness': [], 'valence': [], 'tempo': []}
    dct_lst = {'danceability': [], 'energy': [] , 'speechiness': [], 'acousticness': [], 'instrumentalness': [], 'liveness': [], 'valence': [], 'tempo': []}
    avg_lst = []
    for i in dj_name_list:
        track_list = mongo_plug.db_read_track_list(i)
        for track in track_list:
            for k, v in track['features'].items():
                if k != 'loudness':
                    dct_lst[k].append(v)
    
    for k in dct_lst.keys():
        if k != 'loudness':
            avg = sum(dct_lst[k]) / len(dct_lst[k])
            if k == 'tempo':
                avg = avg/100
            avg_lst.append(avg)
        
    return avg_lst

#// ! 2 functions ข้างล่าง ยังแปลกๆ ไปคิดใหม่ หรือแยกฟังค์ชันไปเลย
def add_fes_click(lst_box):   # lst_box depend on which button clicked
    
    # vars
    temp_name = StringVar()
    temp_year = IntVar()
    
    
    # show new window to get input for each values
    add_fes_screen = Toplevel(app)
    add_fes_screen.title('Adding festival to database')
    
    # Add label
    Label(add_fes_screen, text= 'Enter new festival name to add new festival').grid(row=0, sticky=N, pady=10)
    Label(add_fes_screen, text= 'Name').grid(row=1, sticky=W, pady=10)
    Label(add_fes_screen, text= 'Year').grid(row=2, sticky=W, pady=10)
    
    # Add Entry
    Entry(add_fes_screen, textvariable= temp_name).grid(row=1, column=0)
    Entry(add_fes_screen, textvariable= temp_year).grid(row=2, column=0)
    
    # notif
    notif = Label(add_fes_screen)
    notif.grid(row=4, sticky=N, pady=10)
    
    Button(add_fes_screen, text= 'Comfirm', command= lambda :add_fes_confirm(lst_box, temp_name, temp_year, add_fes_screen, notif)).grid(row=3, sticky=N, pady=10)
    
    
    return

def add_fes_confirm(lst_box, temp_name, temp_year, screen, notif):
    
    #// TODO ADD array to data value for artist
    name = temp_name.get()
    year = temp_year.get()
    
    # insert data(name) to list box
    lst_box.insert(0, ('{}, {}'.format(name, year)))
    # insert to lower list box
    plotting_list.insert(0, ('{}, {}'.format(name, year)))
    
    
    # add new festival
    mongo_plug.db_add_festival(name, year) #<<< add dj new placeholder

    # notif
    #notif.config(fg='green', text= 'Add to database complete')
    
    # destroy toplevel window
    screen.destroy()
    return True

def add_artist_click(lst_box):
    
    # vars
    temp_uri = StringVar()
    
    # show new window to get input for each values
    add_artist_screen = Toplevel(app)
    add_artist_screen.title('Adding artist to database')
    
    # Add label
    Label(add_artist_screen, text= 'Enter new artist name to add to selected festival').grid(row=0, sticky=N, pady=10)
    Label(add_artist_screen, text= 'Uri').grid(row=1, sticky=W, pady=10)
    
    # Add Entry
    Entry(add_artist_screen, textvariable= temp_uri).grid(row=1, column=0)
    
    # notif
    notif = Label(add_artist_screen)
    notif.grid(row=4, sticky=N, pady=10)
    
    
    Button(add_artist_screen, text= 'Comfirm and Fetch Audio Features',
           command= lambda :add_artist_comfirm(lst_box, temp_uri, add_artist_screen, notif)).grid(row=3, sticky=N, pady=10)

    return

def add_artist_comfirm(lst_box, temp_uri, screen, notif):
    
    uri = temp_uri.get()
    if ',' in uri:
        uri = uri.split(',')


    # GET FESTIVALNAME by cursor 
    fes_get = festival_list.get(festival_list.curselection()).split(',')
    fes_name = fes_get[0]
    fes_year = int(fes_get[1].strip())
    def inside_add_artist(uri):
        # fetch artist tracks
        tracks = sp.fetch_artist_tracks(uri, get_features= True)
        pprint(tracks)
        name = sp.artist_name # get name from spotify
        pprint(name)
        # add data to db
        mongo_plug.db_add_artist(name, uri, sp.popularity, fes_name, fes_year, tracks)
        lst_box.insert(0 ,name)
    
    if isinstance(uri, list):
        for i in uri:
            inside_add_artist(i.replace(' ', ''))
    else:
        inside_add_artist(uri)
    
    # fetch_feature and append to db['artist'] [track] # maybe fetch before add to db and addding at the same time
    screen.destroy()
    
    return


def del_click(lst_box, col: str):

    # get name from curselection that will be used as query to delete at db
    name_year = lst_box.get(lst_box.curselection()) # get value where cursor select
    print(name_year)
    if ',' in name_year:
        name = name_year.split(',')[0]
    else:
        name = name_year
    print(name)
    lst_box.delete(lst_box.curselection()) # delete item in listbox
    
    # delete in db 
    if col == 'festival':
        mongo_plug.db_del(col, query= {'name': name})
    
        # delete from plotting list box
        plotting_list_ind = plotting_list.get(0, END).index(name_year)
        print(plotting_list_ind)
        plotting_list.delete(plotting_list_ind)
        
    else: # artist
        fes_name = festival_list.get(festival_list.curselection())
        if ',' in fes_name:
            fes_name = fes_name.split(',')[0]
        if col == 'artist':
            mongo_plug.db_del_artist_from_festival(fes_name, name)
        
    return


def fetch_data_at_open(col, lst_box, what_key: str):
    # fetch all festival data base and insert to festival_list_box
    data = mongo_plug.db_read_all(col)
    try:
        for i in data:
            lst_box.insert(0,('{}, {}').format(i[what_key], i['year'])) # TODO ['year']
            # lower lst box
            plotting_list.insert(0,('{}, {}').format(i[what_key], i['year']))
        return True
    except:
        return False



# Plot button
btn_plot = Button(app, text= 'Plot', command= lambda: plot_click(plotting_list), width= 10, height=3, fg= 'green')
btn_plot.grid(row= 1, column= 2)









if __name__ == '__main__':
    ###### Init process
    # connoect mongodb
    mongo_plug = MongoConnect(config.mongodb_url, pwd= config.mongo_pwd)
    # fetch all festival in database
    fetch_data_at_open('festival', festival_list, 'name')
    # get developers account and connect to spotipy
    sp = FetchSpoty(config.sptf_client_id, config.sptf_client_secret)
    app.mainloop()
    
    
    ### TES AND DEV CODE ###
    # firstfes = [{'name': 'firstfes',
    #             'artist': [{'uri': 'spotify:artist:0AvGycOEDZTaBFLCaiGd9S', 'name': 'dj1'}]
    #         }]
    # firstartist = [{'name': 'dj1',
    #                'uri': 'spotify:artist:0AvGycOEDZTaBFLCaiGd9S'}]
    
    # from pprint import pprint
    
    # # charlie artist uri = 'spotify:artist:7wO5pqunGUkJCQsJohcteb
    # uri = 'spotify:track:1xddmaN7Ivc2SQ940oBskZ'
    
    # #pluged = fetch_spoty()
    # pluged = FetchSpoty(config.sptf_client_id, config.sptf_client_secret)
    # #test = pluged.fetch_features(uri)
    # top_tracks = pluged.fetch_artist_tracks('spotify:artist:0AvGycOEDZTaBFLCaiGd9S')
    # print(top_tracks)
    # print('total tracks :',len(top_tracks))
    
    
    # db = MongoConnect(config.mongodb_url, config.mongo_pwd)
    # # พยายามทำให้ festival ที่เขียนข้างล่างนี่เป็นตัวแปร ที่เปลี่ยนตาม หมวดของ listbox ที่คลิ้ก
    # # โดยอาจจะใช้เป็น param ว่าคลิ้ก add/del จากกล่องไหน
    # db.db_add('festival', firstfes)
    # db.db_add('artist', firstartist)

    
    # features = []
    
    # ####  Use this loop to create data at DB #####
    # for i in range(len(top_tracks)):
    #     print('-----------------')
    #     feature = pluged.fetch_features(top_tracks[i]['uri'])[0]
    #     print('features ', feature)
    #     features.append(feature)
        
    # db.db_add('track', features)
        
    # # [features.append(pluged.fetch_features(top_tracks[x]['uri'])) for x in range(len(top_tracks)) ]
    # # pprint(features)
    # # pprint(features[0])        
    # # pprint(features[0][0])        
