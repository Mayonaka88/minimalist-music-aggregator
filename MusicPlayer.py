from tkinter import *
from tkinter.font import BOLD
import time
import threading
from numpy.core.numeric import True_
import pygame
from Test import List_Of_Songs
from mp3Downloader import mp3Downloader
from artistPic import getArtistPic
import os
import base64
from urllib.request import urlopen
import requests
from PIL import ImageTk, Image


class MusicPlayer:
    def __init__(self):
        self.root = Tk()
        self.newPlayList()
        pygame.init()
        pygame.mixer.init()

    def run(self):
        self.root.mainloop()

    def mainWindowSetUp(self):

        folder = os.listdir("C:/Users/abdal/Desktop/Project/playlistName")
        self.playlistDisplayName = folder[0]
        self.playlistDisplayName = self.playlistDisplayName.replace('.txt', '')
        os.rename(f"C:/Users/abdal/Desktop/Project/playlistName/{folder[0]}", f"C:/Users/abdal/Desktop/Project/playlistName/playlistName.txt")

        self.root.title("Music Player")
        self.root.geometry("1000x600")
        self.root.resizable(width=FALSE, height=FALSE)
        self.root["bg"] = "#202020"

        self.track = StringVar()
        self.status = 0

        self.label1 = Text(self.root, font=("Catamaran", 32, BOLD), foreground="white",state='disabled',borderwidth=0,cursor="arrow",bg="#202020")
        self.label1.place(x=220,y=10, height=60,width=750)
        self.label1.configure(state='normal')
        self.label1.insert('end',"      "+self.playlistDisplayName)
        self.label1.configure(state='disabled')
        self.canvas1 = Canvas(self.label1, width = 50, height = 50, background="#202020", bd =0, highlightthickness=0, relief='ridge')      
        self.canvas1.place(x=0,y=0, height=60,width=60)
        self.playlistLogo = PhotoImage(file = f"C:/Users/abdal/Desktop/Project/Icons/playlist.png")
        self.playlistLogo = self.playlistLogo.subsample(2, 2)
        self.canvas1.create_image(30,30, image=self.playlistLogo)

        self.sideBar1 = Text(self.root, font=("Catamaran", 18, BOLD), foreground="white",state='disabled',borderwidth=0,cursor="arrow",bg="#0f0f0f",padx=20,pady=5)
        self.sideBar1.place(x=0,y=0, height=480,width=200)

        self.label2 = Text(self.root, font=("Catamaran", 18, BOLD), foreground="white",state='disabled',borderwidth=0,cursor="arrow",bg="#0f0f0f",padx=25,pady=5)
        self.label2.place(x=0,y=75, height=250,width=200)
        self.label2.tag_configure("logos", foreground="white",font=("Catamaran", 12,BOLD))
        self.label2.tag_configure("favSong", foreground="white",font=("Catamaran", 10))
        self.label2.configure(state='normal')
        self.label2.insert('end',"♥ Favorites" + "\n")
        self.label2.configure(state='disabled')

        self.refreshButton2 = Button(self.root,bg="#202020", text="  Refresh Playlist  ",font=("Catamaran", 12,BOLD),foreground="white",bd=0,command=lambda: self.refreshList())
        self.refreshButton2.place(x=15,y=15, height=50,width=170)

        self.addFavoriteButton = Button(self.root,bg="#202020", text="  + Add to Favorites  ",font=("Catamaran", 12,BOLD),foreground="white",bd=0,command=lambda: self.addToFavorites())
        self.addFavoriteButton.place(x=15,y=409, height=60,width=170)

        self.addFavoriteLabel = Label(self.root,bg="#202020", text="Track",font=("Catamaran", 14,BOLD,),foreground="white",bd=0,justify='center')
        self.addFavoriteLabel.place(x=15,y=345, height=50,width=80)

        self.addFavoriteEntry = Entry(self.root,bg="#202020",font=("Catamaran", 20,BOLD,),foreground="white",bd=0,justify='center')
        self.addFavoriteEntry.place(x=105,y=345, height=50,width=80)

        self.songDesplay = Text(self.root, font=("Arial", 12), foreground="gray",state='disabled',borderwidth=0,cursor="arrow",bg="#202020",pady=10)
        self.songDesplay.place(x=210,y=80, height=400,width=770)
        self.songDesplay.tag_configure("songs", foreground="white",font=("Catamaran", 12, BOLD), background="#0f0f0f")
        self.songDesplay.tag_configure("Artist", foreground="white",font=("Catamaran", 10 ), background="#0f0f0f")
        self.songDesplay.tag_configure("Space", foreground="white",font=("Catamaran", 2 ), background="#0f0f0f")
        self.songDesplay.tag_configure("index1", foreground="white",font=("Catamaran", 16, BOLD ), background="#0f0f0f")
        self.songDesplay.tag_configure("index2", foreground="#0f0f0f",font=("Catamaran", 16, BOLD ), background="#0f0f0f")

        self.songFileNameList = os.listdir(f'C:/Users/abdal/Desktop/Project/songs')
        self.songFileNameList = list(map(lambda songFileNameList: songFileNameList.replace('.mp3',''), self.songFileNameList))
        self.numberOfSongsInFile = len(self.songFileNameList)
        self.songNameFromList = ["","","","","","","","","","","",""]
        self.artistNameFromList = ["","","","","","","","","","","",""]

        for song in range(self.numberOfSongsInFile):

            self.fullSongNameFromList = self.songFileNameList[song]
            self.splitTitle = self.fullSongNameFromList.split("-")
            self.songNameFromList[song] = self.splitTitle[0]
            self.artistNameFromList[song] = self.splitTitle[1]

            self.songDesplay.configure(state='normal')
            self.songDesplay.insert('end',"\n"+ "\n","Space")
            self.songDesplay.insert('end',"   ","index1")
            self.songDesplay.insert('end', str(song+1)+")","index1")
            self.songDesplay.insert('end',"    ","index1")
            self.songDesplay.insert('end',self.songNameFromList[song] + "\n","songs")
            self.songDesplay.insert('end',"   ","index2")
            self.songDesplay.insert('end', str(song+1)+")","index2")
            self.songDesplay.insert('end',"    ","index2")
            self.songDesplay.insert('end',self.artistNameFromList[song]+ "\n","Artist")
            self.songDesplay.insert('end',"\n"+ "\n","Space")
            self.songDesplay.insert('end',"\n")
            self.songDesplay.configure(state='disabled')

        self.label4 = Text(self.root, font=("Arial", 12), foreground="white",state='disabled',borderwidth=0,cursor="arrow",bg="#2d2d2d",pady=20,padx=130)
        self.label4.place(x=0,y=480, height=120,width=1000)
        self.label4Cover = Text(self.root, font=("Arial", 12), foreground="white",state='disabled',borderwidth=0,cursor="arrow",bg="#2d2d2d",pady=20,padx=130)
        self.label4Cover.place(x=500,y=480, height=120,width=1000)
        self.label4.tag_configure("songs", foreground="white",font=("Catamaran", 20, BOLD), background="#0f0f0f")
        self.label4.tag_configure("Artist", foreground="white",font=("Catamaran", 14 ), background="#0f0f0f")
        self.label4.tag_configure("Space", foreground="white",font=("Catamaran", 7 ), background="#2d2d2d")

        self.songSelected(1)
        self.songTemp = 1

        self.refreshButton = Button(self.root,bg="#2d2d2d", text="↻",font=("Cambria Math", 32,BOLD),foreground="white",bd=0,command=lambda: self.refreshList())
        self.refreshButton.place(x=929,y=25, height=50,width=50)

        self.trackIndexSelector = Entry(self.root,bg="#0f0f0f",font=("Catamaran", 32,BOLD,),foreground="white",bd=0,justify='center')
        self.trackIndexSelector.place(x=815,y=500, height=75,width=75)

        self.playTrackLabel = Label(self.root,bg="#0f0f0f", text="Play Track:",font=("Catamaran", 32,BOLD,),foreground="white",bd=0,justify='center')
        self.playTrackLabel.place(x=550,y=500, height=75,width=250)

        self.playButton = Button(self.root,bg="#0f0f0f", text="▶",font=("Cambria Math", 38,BOLD),foreground="white",bd=0,command=lambda: self.playSong())
        self.playButton.place(x=905,y=500, height=75,width=75)

    def addToFavorites(self):
        self.songFavoriteIndex = self.addFavoriteEntry.get()

        self.songFileNameList = os.listdir(f'C:/Users/abdal/Desktop/Project/songs')
        self.songFileNameList = list(map(lambda songFileNameList: songFileNameList.replace('.mp3',''), self.songFileNameList))
        self.numberOfSongsInFile = len(self.songFileNameList)

        if self.songFavoriteIndex.isalpha():
            self.addFavoriteEntry.configure(foreground="red")
        else:
            self.songFavoriteIndex = int(self.songFavoriteIndex)
            if self.songFavoriteIndex < (self.numberOfSongsInFile) + 1 and self.songFavoriteIndex > 0:
                self.addFavoriteEntry.configure(foreground="white")

                self.songToFavorite = self.songFileNameList[self.songFavoriteIndex - 1]
                self.songToFavoriteSplit=self.songToFavorite.split('-')
                self.newFavoriteArtist = self.songToFavoriteSplit[1]
                self.newFavoritesong = self.songToFavoriteSplit[0]
                self.addedNewFavorite = self.newFavoriteArtist + " - " + self.newFavoritesong

                self.label2.configure(state='normal')
                self.label2.insert('end',"♪", "logo")
                self.label2.insert('end',"   "+self.addedNewFavorite+"\n", "favSong")
                self.label2.configure(state='disabled')
                self.addFavoriteEntry.delete(0, END)
            else:
                self.addFavoriteEntry.configure(foreground="red")

    def songSelected(self, songIndex):
        self.selectedSong = self.songNameFromList[songIndex-1]
        self.selectedArtist = self.artistNameFromList[songIndex-1]

        if "," in self.selectedArtist:
            self.selectedArtist.split(",")
            self.selectedArtist2 = self.selectedArtist[0]
            picUrl = getArtistPic(self.selectedArtist2)
        else:
            picUrl = getArtistPic(self.selectedArtist)

        img_data = requests.get(picUrl).content
        with open(f'C:/Users/abdal/Desktop/Project/Icons/artistPic.png', 'wb') as handler:
            handler.write(img_data)


        self.canvas3 = Canvas(self.root,bg="#2d2d2d", bd =0, highlightthickness=0, relief='ridge')      
        self.canvas3.place(x=15,y=487, height=110,width=110)
        self.playlistLogo2 = Image.open(f'C:/Users/abdal/Desktop/Project/Icons/artistPic.png')
        self.playlistLogo3 = self.playlistLogo2.resize((round(self.playlistLogo2.size[0]*0.20), round(self.playlistLogo2.size[1]*0.20)))
        self.playlistLogo4 = ImageTk.PhotoImage(self.playlistLogo3)
        self.canvas3.create_image(40,40, image=self.playlistLogo4)


        self.label4.configure(state='normal')
        self.label4.delete("1.0", END)
        self.label4.insert('end',"  "+self.selectedSong+"  ","songs")
        self.label4.insert('end',"\n", "Space")
        self.label4.insert('end',"   "+self.selectedArtist+"   ","Artist")
        self.label4.configure(state='disabled')
    
    def refreshList(self):
        
        self.songFileNameList = os.listdir(f'C:/Users/abdal/Desktop/Project/songs')
        self.songFileNameList = list(map(lambda songFileNameList: songFileNameList.replace('.mp3',''), self.songFileNameList))
        self.numberOfSongsInFile = len(self.songFileNameList)
        self.songNameFromList = ["","","","","","","","","","","",""]
        self.artistNameFromList = ["","","","","","","","","","","",""]

        self.songDesplay.destroy()
        self.songDesplay = Text(self.root, font=("Arial", 12), foreground="gray",state='disabled',borderwidth=0,cursor="arrow",bg="#202020",pady=10)
        self.songDesplay.place(x=210,y=80, height=400,width=770)
        self.songDesplay.tag_configure("songs", foreground="white",font=("Catamaran", 12, BOLD), background="#0f0f0f")
        self.songDesplay.tag_configure("Artist", foreground="white",font=("Catamaran", 10 ), background="#0f0f0f")
        self.songDesplay.tag_configure("Space", foreground="white",font=("Catamaran", 2 ), background="#0f0f0f")
        self.songDesplay.tag_configure("index1", foreground="white",font=("Catamaran", 16, BOLD ), background="#0f0f0f")
        self.songDesplay.tag_configure("index2", foreground="#0f0f0f",font=("Catamaran", 16, BOLD ), background="#0f0f0f")

        for song in range(self.numberOfSongsInFile):

            self.fullSongNameFromList = self.songFileNameList[song]
            self.splitTitle = self.fullSongNameFromList.split("-")
            self.songNameFromList[song] = self.splitTitle[0]
            self.artistNameFromList[song] = self.splitTitle[1]

            self.songDesplay.configure(state='normal')
            self.songDesplay.insert('end',"\n"+ "\n","Space")
            self.songDesplay.insert('end',"   ","index1")
            self.songDesplay.insert('end', str(song+1)+")","index1")
            self.songDesplay.insert('end',"    ","index1")
            self.songDesplay.insert('end',self.songNameFromList[song] + "\n","songs")
            self.songDesplay.insert('end',"   ","index2")
            self.songDesplay.insert('end', str(song+1)+")","index2")
            self.songDesplay.insert('end',"    ","index2")
            self.songDesplay.insert('end',self.artistNameFromList[song]+ "\n","Artist")
            self.songDesplay.insert('end',"\n"+ "\n","Space")
            self.songDesplay.insert('end',"\n")
            self.songDesplay.configure(state='disabled')

    def playSong(self):
        selectedSong = self.trackIndexSelector.get()
        if selectedSong.isalpha():
            selectedSong = self.songTemp
            self.trackIndexSelector.delete(0, END)
        else:
            selectedSong = int(selectedSong)
        
        self.songFileNameList = os.listdir(f'C:/Users/abdal/Desktop/Project/songs')
        self.songFileNameList = list(map(lambda songFileNameList: songFileNameList.replace('.mp3',''), self.songFileNameList))
        self.numberOfSongsInFile = len(self.songFileNameList)

        if selectedSong < (self.numberOfSongsInFile) + 1 and selectedSong > 0:
            self.trackIndexSelector.configure(foreground="white")
            self.songSelected(selectedSong)
            if self.songTemp == selectedSong:
                if self.status == 1:
                    pygame.mixer.music.pause()
                    self.status = 2
                    self.songTemp = selectedSong
                    self.playButton.configure(text="▶")
                else:
                    pygame.mixer.music.unpause()
                    self.status = 1
                    self.songTemp = selectedSong
                    self.playButton.configure(text="⏸")
            else:
                    folder = os.listdir(f"C:/Users/abdal/Desktop/Project/songs")
                    pygame.mixer.music.load(f"C:/Users/abdal/Desktop/Project/songs/{folder[selectedSong -1]}")
                    pygame.mixer.music.play()
                    self.status = 1
                    self.songTemp = selectedSong
                    self.playButton.configure(text="⏸")
        else:
            self.trackIndexSelector.configure(foreground="red")

    def newPlayList(self):

        #Fixed dimentions and the title of the window are declared here
        self.root.title("New Playlist")
        self.root.geometry("1000x600")
        self.root.resizable(width=FALSE, height=FALSE)
        self.root["bg"] = "#202020"
        
        #The welcome message is created here using labels
        self.label1 = Label(self.root, text="Welcome to Tuney",  width="12", height=5,bd=0, background="#202020",foreground='white',font=("Catamaran", 50))
        self.label1.place(x=225,y=5, height=100, width=550)

        self.label2 = Label(self.root, text="Your own personal minimal music aggregator!",  width="12", height=5,bd=0, background="#202020",foreground='white',font=("Catamaran", 16))
        self.label2.place(x=250,y=90, height=50, width=500)

        self.label8 = Label(self.root, text="Just enter three songs and Tuney will find the best songs for your taste", background="#202020", width="12", height=5,bd=0,foreground='white',font=("Catamaran", 12))
        self.label8.place(x=250,y=140, height=40, width=500)

        #This label is empty until the user tries to proceed without filling out the form
        self.label3 = Label(self.root, text="",  width="12", height=5,bd=0,foreground='red',font=("Catamaran", 12,BOLD),background="#202020")
        self.label3.place(x=250,y=180, height=30, width=500)

        #These labels are used to display the criteria of the form
        self.label9 = Label(self.root, text="Playlist Name:",  width="12", height=5,bd=0,foreground='white',font=("Catamaran", 20),background="#2d2d2d")
        self.label9.place(x=250,y=225, height=50, width=190)
        
        self.label4 = Label(self.root, text="First song:",  width="12", height=5,bd=0,foreground='white',font=("Catamaran", 20),background="#2d2d2d")
        self.label4.place(x=250,y=300, height=50, width=190)

        self.label5 = Label(self.root, text="Second song:",  width="12", height=5,bd=0,foreground='white',font=("Catamaran", 20),background="#2d2d2d")
        self.label5.place(x=250,y=375, height=50, width=190)

        self.label6 = Label(self.root, text="Third song:",  width="12", height=5,bd=0,foreground='white',font=("Catamaran", 20),background="#2d2d2d")
        self.label6.place(x=250,y=450, height=50, width=190)
        
        #Here is where the textboxes the user writes in are created
        self.chatWindow4 = Text(self.root, bd=1, bg="white",  width="50", height="8", font=("Catamaran", 16), foreground="white", padx=10, pady=10,wrap=WORD,background="#0f0f0f",borderwidth=0)
        self.chatWindow4.place(x=450,y=225, height=50, width=300)
        
        self.chatWindow1 = Text(self.root, bd=1, bg="white",  width="50", height="8", font=("Catamaran", 16), foreground="white", padx=10, pady=10,wrap=WORD,background="#0f0f0f",borderwidth=0)
        self.chatWindow1.place(x=450,y=300, height=50, width=300)

        self.chatWindow2 = Text(self.root, bd=1, bg="white",  width="50", height="8", font=("Catamaran", 16), foreground="white", padx=10, pady=10,wrap=WORD,background="#0f0f0f",borderwidth=0)
        self.chatWindow2.place(x=450,y=375, height=50, width=300)

        self.chatWindow3 = Text(self.root, bd=1, bg="white",  width="50", height="8", font=("Catamaran", 16), foreground="white", padx=10, pady=10,wrap=WORD,background="#0f0f0f",borderwidth=0)
        self.chatWindow3.place(x=450,y=450, height=50, width=300)

        #Here is where the button is created. When the button is pressed, it will call the toLoadingScreen() function
        self.button1 = Button(self.root, text="Create Playlist",  width="12", height=5,bd=0, bg="#2d2d2d", activebackground="white",foreground='#ffffff',font=("Catamaran", 20), command=lambda: self.toLoadingScreen(None))
        self.button1.place(x=250,y=525, height=50, width=500)

    def toLoadingScreen( self, event):
        #this function is used to get data from the textboxes and save them 
        #then it calls on the mainWindowSetUp() function which is where the user can interact with the chatbot
        
        #here the user data are saved in global variables so it can be used later
        #the get() function extracts the data from the textboxes and saves them in thier respective variable
        global playlistName
        global song1
        global song2
        global song3
        self.playlistName = self.chatWindow4.get("1.0", END)
        self.song1 = self.chatWindow1.get("1.0", END)
        self.song2 = self.chatWindow2.get("1.0", END)
        self.song3 = self.chatWindow3.get("1.0", END)

        self.filePlaylistTitle = self.playlistName
        self.filePlaylistTitle = self.filePlaylistTitle.split('\n')

        folder = os.listdir("C:/Users/abdal/Desktop/Project/playlistName")
        os.rename(f"C:/Users/abdal/Desktop/Project/playlistName/{folder[0]}", f"C:/Users/abdal/Desktop/Project/playlistName/{self.filePlaylistTitle[0]}"+".txt")



        #if the textboxes are left empty, the variables will save "\n"
        #by using this if statment, we force the user to fill out the form so they can proceed
        if self.playlistName == "\n" or self.song1 == "\n" or self.song2 == "\n" or self.song3 == "\n" :
            self.label3.config(text="Please enter valid information to proceed", foreground="red")
        else:
            #if the textboxes are filled out, then all the elements of the login page are deleted so we can have an empty window that the other function can use
            self.label1.destroy()
            self.label2.destroy()
            self.label3.destroy()
            self.label4.destroy()
            self.label5.destroy()
            self.label6.destroy()
            self.label9.destroy()
            self.label8.destroy()
            self.chatWindow1.destroy()
            self.chatWindow2.destroy()
            self.chatWindow3.destroy()
            self.chatWindow4.destroy()
            self.button1.destroy()
            #after all the elements are removed, the function that houses the chat bot is called upon
            self.loadingScreen()
        
    def loadingScreen(self):
        self.root.title("New Playlist")
        self.root.geometry("1000x600")
        self.root.resizable(width=FALSE, height=FALSE)
        self.root["bg"] = "#202020"
        self.label1 = Text(self.root, bd=0, background="#202020",foreground='white',font=("Catamaran", 150,BOLD),state='disabled')
        self.label1.place(x=190,y=50, height=500, width=700)

        recommenderTimer = threading.Timer(90.0, self.mainWindowSetUp)
        recommenderTimer.start()

        loadingTimer = threading.Timer(1.0, self.recommendation)
        loadingTimer.start()

        animationTimer1 = threading.Timer(25.0, self.loadingAnimation1)
        animationTimer1.start()
        animationTimer2 = threading.Timer(50.0, self.loadingAnimation2)
        animationTimer2.start()
        animationTimer3 = threading.Timer(75.0, self.loadingAnimation1)
        animationTimer3.start()

        animationTimer4 = threading.Timer(90.0, self.label1.destroy)
        animationTimer4.start()

        downloaderTimer = threading.Timer(30.0, self.downloadSongs)
        downloaderTimer.start()

        second=StringVar()
        second.set("00")

        self.Label2 = Label(self.root, bd=0,foreground='white',font=("Catamaran", 20),background="#2d2d2d",text="Please wait for the playlist to be created")
        self.Label2.place(x=200,y=375, height=50, width=600)

        self.secondsLabel = Label(self.root, bd=0,foreground='white',font=("Catamaran", 20),background="#0f0f0f",textvariable=second)
        self.secondsLabel.place(x=470,y=450, height=50, width=50)

        animationTimer5 = threading.Timer(90.0, self.secondsLabel.destroy)
        animationTimer5.start()
        animationTimer6 = threading.Timer(90.0, self.Label2.destroy)
        animationTimer6.start()

        temp = 90
        while temp >-1:
            second.set(temp)
            self.root.update()
            time.sleep(1)
            temp = temp -1
    
    def loadingAnimation1(self):
        self.label1.configure(state='normal')
        self.label1.insert('end',"◕ ")
        self.label1.configure(state='disabled')

    def loadingAnimation2(self):
        self.label1.configure(state='normal')
        self.label1.insert('end',"◡ ")
        self.label1.configure(state='disabled')

    def downloadSongs(self):
        mp3Download = mp3Downloader()
        songs = mp3Download.loadSongs()
        urls = mp3Download.getUrls(songs)
        downloader1 = mp3Download.downloader(urls, songs)

    def recommendation(self):
        self.recommender = List_Of_Songs(self.playlistName,self.song1, self.song2, self.song3 )




 
if __name__ == "__main__":
    musicPlayer1 = MusicPlayer()
    musicPlayer1.run()