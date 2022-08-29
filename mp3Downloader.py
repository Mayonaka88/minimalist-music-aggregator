from __future__ import unicode_literals
import os
import youtube_dl
from youtubesearchpython import VideosSearch

class mp3Downloader():
    def loadSongs(self):
        folder1 = os.listdir("C:/Users/abdal/Desktop/Project/songs")
        for file1 in folder1:
            os.remove(f"C:/Users/abdal/Desktop/Project/songs/{file1}")
        folder2 = os.listdir("C:/Users/abdal/Desktop/Project/temp")
        for file2 in folder2:
            os.remove(f"C:/Users/abdal/Desktop/Project/temp/{file2}")
        
        filepath2=f'C:/Users/abdal/Desktop/Project/songlist.txt'
        filepath1 =f'C:/Users/abdal/Desktop/Project/artists.txt'
        data3 = ["","","","","","","","","","","",""]
        with open(filepath1) as file:
            data1 = file.readlines()
        
        with open(filepath2) as file:
            data2 = file.readlines()
        for x in range(12):
            songNameTemp = data2[x] +"-"+ data1[x]
            data3[x] = songNameTemp
        data3 = list(map(lambda data3: data3.replace('\n',''), data3))
        data3 = list(map(lambda data3: data3.replace('"',''), data3))
        data3 = list(map(lambda data3: data3.replace("'",''), data3))
        return data3

    def downloader(self,urlList, songsList):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'C:/Users/abdal/Desktop/Project/temp/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }
        for url in urlList:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                folder = os.listdir("C:/Users/abdal/Desktop/Project/temp")
                os.rename(f"C:/Users/abdal/Desktop/Project/temp/{folder[0]}", f"C:/Users/abdal/Desktop/Project/songs/{songsList[urlList.index(url)]}"+".mp3")

        return "done"
                



    def getUrl(self,songName):
        songName = songName + " audio"
        videosSearch = VideosSearch(songName, limit = 1)
        videoResult = videosSearch.result()
        videoResult2 = videoResult["result"][0]
        return videoResult2["link"]

    def getUrls(self,songLists):
        urls = [self.getUrl(song) for song in songLists]
        return urls
