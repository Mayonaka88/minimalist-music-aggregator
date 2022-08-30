from swampy.Lumpy import Lumpy
import spotipy
from IPython.display import display
from scipy.spatial.distance import cdist
from tqdm import tqdm_notebook as tqdm
import numpy as np
import numpy_indexed as npi
import pandas
import joblib
from spotipy.oauth2 import SpotifyClientCredentials
from keras.models import load_model
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import plotly.graph_objs as go
import os



std_scaler = joblib.load(f'C:/Users/abdal/Desktop/Project/std_scaler.pkl')
pca = joblib.load(f'C:/Users/abdal/Desktop/Project/pca.pkl')
y_j = joblib.load(f'C:/Users/abdal/Desktop/Project/yeo_johnson.pkl')
model = load_model(f'C:/Users/abdal/Desktop/Project/model.h5')

features = [
    'mode',
    'acousticness',
    'danceability',
    'energy',
    'instrumentalness',
    'liveness',
    'loudness',
    'speechiness',
    'valence',
] 

spootify = spotipy.Spotify(
    client_credentials_manager = SpotifyClientCredentials(
        client_id="",
        client_secret=""
    )
) 

class List_Of_Songs():
    playlists = {}
    def __init__(self, playlistName, song1, song2, song3):
        self.name = playlistName
        List_Of_Songs.playlists[self.name] = self
        self.init_song_strings = []
        self.ResultsOfSearch = []
        self.RecommendedIdsOfTracks = [] 
        self.trax = [] 
        self.df = None 
        self.playlist = None
        self.init_song_strings.append(song1)
        self.init_song_strings.append(song2)
        self.init_song_strings.append(song3)
        self.recommendSongs()
        self.getFeaturesOfSongs()
        self.toTransform()
        self.buildTheListOfSongs() 
        self.previewTheListOfSongs()

        
    def recommendSongs(self):
        print('Obtaining the recommended choices..........')
        for ss in self.init_song_strings:
            r = spootify.search(ss,limit=1)['tracks']['items'][0]
            self.ResultsOfSearch.append({
                        'id':r['id'],
                        'artists':[i['name'] for i in r['artists']],
                        'name':r['name']
                })
        for id_ in tqdm(self.ResultsOfSearch):
            results = spootify.recommendations(seed_tracks = [id_['id']],limit=100)
            for r in results['tracks']:
                if r['id'] not in [i['id'] for i in self.RecommendedIdsOfTracks]:
                    self.RecommendedIdsOfTracks.append({
                        'id':r['id'],
                        'artists':[i['name'] for i in r['artists']],
                        'name':r['name']



                        }) 
        print('Loading.......')
        results_2 = spootify.recommendations(
            seed_tracks = [id_['id'] for id_ in self.ResultsOfSearch],
            limit=100
        )
        count = 0
        for r in results_2['tracks']:
            if r['id'] not in [i['id'] for i in self.RecommendedIdsOfTracks]:
                count += 1
                self.RecommendedIdsOfTracks.append({
                    'id':r['id'],
                    'artists':[i['name'] for i in r['artists']],
                    'name':r['name']


                    }) 
        print('During the runtime, there were',count,'more of songs!')
    
    def getFeaturesOfSongs(self):
        print('Obtaining song features......')
        for id_ in tqdm(self.ResultsOfSearch):
            dict_ = spootify.audio_features(id_['id'])[0]
            dict_.update(id_)
            self.trax.append(dict_)
        n = 100
        results = []
        broken_list = [self.RecommendedIdsOfTracks[i * n:(i + 1) * n] for i in range(
            (len(self.RecommendedIdsOfTracks) + n - 1) // n )]
        for list_ in broken_list:
            results += spootify.audio_features([id_['id'] for id_ in list_])
        for i, id_ in enumerate(self.RecommendedIdsOfTracks):
            results[i].update(id_)
            self.trax.append(results[i])


    def toTransform(self):
        print('Applying the required transformations .....')
        GroupOfColumns = ['id','artists','name','tempo','time_signature','key',] + features
        self.df = pandas.DataFrame(self.trax)[GroupOfColumns].dropna()
        self.df[features[1:]] = std_scaler.transform(y_j.transform(self.df[features[1:]]))
        self.playlist = self.df.iloc[0:3].copy()
        
    def rnn_predict(self):
        return model.predict(np.array(
            [np.array(
                self.playlist[features]
            )]
        ))[0,-1]
    
    @staticmethod
    def similarityOfTempo(n1,n2):
        if n1 <= 0:
             return -1
        n2 *= (n2 > 0)
        return np.cos(2*np.pi*np.log2(n1/n2))
    
    @staticmethod
    def similarityOfKey(s1,s2):
        x1 = s1['key']
        y1 = s1['mode']
        x2 = s2['key']
        y2 = s2['mode']
        x1 += 3*(y1==0)
        x2 += 3*(y2==0)
        x1,x2 = np.remainder((x1,x2),12)
        CirOfFifths = {0:0,7:1,2:2,9:3,4:4,11:5,6:6,1:7,8:8,3:9,10:10,5:11,}
        diff = np.abs(
            CirOfFifths[x1] - npi.remap(x2, list(CirOfFifths.keys()), list(CirOfFifths.values()))
        )
        diff = np.abs((diff>6)*12-diff)
        return 1 - ((diff == 0) + diff - 1)/2.5
    
    def argmin_song(self,songs):
        song = self.playlist.iloc[-1]
        a = 1 #flow - how much to count distance
        b = 1 #sweetness - how much to count key similarity
        g = 1 #smoothness - how much to count tempo similarity
        d = 1.2 #spicynesss - scaler for RNN vector
        distance = cdist([self.rnn_predict()*d],songs[features[1:]])[0]
        similarityOfKey = List_Of_Songs.similarityOfKey(song,songs)
        similarityOfTempo = List_Of_Songs.similarityOfTempo(song['tempo'],songs['tempo']).values
        return songs.reset_index().iloc[np.argmin(
            a*distance - b*similarityOfKey - g*similarityOfTempo
        )]
    
    def buildTheListOfSongs(self):
        print('Ranking the recommended songs for you......')
        for i in tqdm(range(10)):
            songs = self.df[~self.df['id'].isin(self.playlist['id'].to_list())]
            self.playlist = self.playlist.append(self.argmin_song(songs), ignore_index = True)
           
        
    def getArtistPic(x):
    #with open('artists.txt', 'r') as firstfile:
   #text1 = firstfile.readlines()
        results = spootify.search(q='artist:' + x, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            yz = artist['images'][0]['url']
        return yz
                    
    
    def previewTheListOfSongs(self):
        x = self.playlist[['artists','name','id',]]
        display(x)
         #####################
       #REMOVE OLDER VERSIONS#
        #####################
        if os.path.exists(f'C:/Users/abdal/Desktop/Project/artists.txt'):
            os.remove(f'C:/Users/abdal/Desktop/Project/artists.txt')
            
        if os.path.exists(f'C:/Users/abdal/Desktop/Project/songlist.txt'):
            os.remove(f'C:/Users/abdal/Desktop/Project/songlist.txt')
        print ("(1/3)")
         ####################################
       #ARTLIST SAVE, READ, MODIFY AND RESAVE#
        ####################################
        artistlist = self.playlist[['artists']]

        artistlist.to_csv(f'C:/Users/abdal/Desktop/Project/artists.txt', header=None, index=None, sep=' ', mode='a', )
         
        print ("(2/3)")

        with open(f'C:/Users/abdal/Desktop/Project/artists.txt', 'r') as firstfile:
            text1 = firstfile.read()
            text1 = text1.replace("[", "")
            text1 = text1.replace("]", "")

           # If you wish to save the updates back into a cleaned up file
        with open(f'C:/Users/abdal/Desktop/Project/artists.txt', 'w') as firstfile:
             firstfile.write(text1)
                
       #######################################
       #SONGLIST SAVE, READ, MODIFY AND RESAVE#
        #####################################
        songlist = self.playlist[['name']]

        songlist.to_csv(f'C:/Users/abdal/Desktop/Project/songlist.txt', header=None, index=None, sep=' ', mode='a', )

        with open(f'C:/Users/abdal/Desktop/Project/songlist.txt', 'r') as secondfile:
            text2 = secondfile.read()
            text2 = text2.replace("[", "")
            text2 = text2.replace("]", "")

           # If you wish to save the updates back into a cleaned up file
        with open(f'C:/Users/abdal/Desktop/Project/songlist.txt', 'w') as secondfile:
             secondfile.write(text2)
 
    def getArtistPic(x):
        results = spootify.search(q='artist:' + x, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            yz = artist['images'][0]['url']
        return yz

    

