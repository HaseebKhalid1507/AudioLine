import pafy
import vlc
import urllib.request
import re
from time import sleep
from rich.progress import track, Progress
from youtubesearchpython import PlaylistsSearch
from os import system
import sys


def isWindows():
    if sys.platform == "win32":
        return True
    elif sys.platform == "linux" or sys.platform == "linux2":
        return False
    else:
        raise OSError("Unsupported Operating System! [WIN/LINUX ONLY]")


def cls():
    if isWindows():
        system("cls")
    else:
        system("clear")


class AudioLine:
    """ The Main Object for the AudioLine Process to Utilize. """

    def __init__(self):
        self.played = []
        self.video_ids = []
        self.media = None

    #	FUNCTION TO PLAY AUDIO
    def playvideo(self, url):
        #	INITIALIZE VIDEO
        video = pafy.new(url)
        audio = video.getbestaudio()
        self.media = vlc.MediaPlayer(audio.url)

        #	PRINT VIDEO DETAILS
        print("\n--------------------------------------------------------------------------------")
        print("\nNOW PLAYING: \n\t" + video.title)
        # print (video.duration)
        print("\tViews:  " + f"{video.viewcount:,d}" + "\t\t\tDuration:  " + video.duration)
        print("\t\t\tPress 'CTRL+C' to Skip Song!")

        with Progress(transient=True) as prog:
            song_play = prog.add_task("[green]Playing Song", total=video.length)

            #	START PLAYER
            self.media.play()

            while self.media.is_playing() == False:
                pass

            while self.media.is_playing():
                sleep(1)
                prog.update(song_play, advance=1)

        print("DONE PLAYING %s!" % video.title)


    #	FUNCTION TO KEEP PLAYING SONGS
    def autoplay(self,url):
        #	ADD URL TO LIST OF PLAYED SONGS
        self.played.append(url)
        #	PLAY CURRENT VIDEO
        self.playvideo(url)

        #	CHANGE CURRENT VIDEO TO NEXT ONE
        html = urllib.request.urlopen(url)
        video_ids_dupes = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        #	REMOVE DUPLICATES FROM LIST
        for i in video_ids_dupes:
            if i not in self.video_ids and "https://www.youtube.com/watch?v=" + i not in self.played:
                self.video_ids.append(i)
        url = ("https://www.youtube.com/watch?v=" + self.video_ids[0])

        #	RECURSION PAGMAN
        self.autoplay(url)

    #	FUNCTION TO TAKE FIRST VIDEO FROM YOUTUBE SEARCH PAGE
    def search_youtube(self, search):
        search_url = "https://www.youtube.com/results?search_query=" + search.replace(" ", "+")
        html = urllib.request.urlopen(search_url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = ("https://www.youtube.com/watch?v=" + video_ids[0])
        return url

    #	FUNCTION TO PLAY VIDEOS IN A PLAYLIST
    def play_playlist(self, url):

        html = urllib.request.urlopen(url)
        video_ids_dupes = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        #	REMOVE DUPLICATES FROM LIST
        for i in video_ids_dupes:
            if i not in self.video_ids and "https://www.youtube.com/watch?v=" + i not in self.played:
                self.video_ids.append(i)

        for i in self.video_ids:
            self.playvideo("https://www.youtube.com/watch?v=" + i)

    #	FUNCTION TO TAKE FIRST PLAYLIST FROM YOUTUBE SEARCH PAGE
    def search_playlist(self, search):
        playlistsSearch = PlaylistsSearch(search, limit=1)
        self.play_playlist(playlistsSearch.result()["result"][0]["link"])

    #	MAIN SCRIPT FUNCTION
    def menu(self):

        flag = 0

        while flag != 7:

            cls()

            print("")
            print("\t █████╗ ██╗   ██╗██████╗ ██╗ ██████╗ ██╗     ██╗███╗   ██╗███████╗")
            print("\t██╔══██╗██║   ██║██╔══██╗██║██╔═══██╗██║     ██║████╗  ██║██╔════╝")
            print("\t███████║██║   ██║██║  ██║██║██║   ██║██║     ██║██╔██╗ ██║█████╗  ")
            print("\t██╔══██║██║   ██║██║  ██║██║██║   ██║██║     ██║██║╚██╗██║██╔══╝  ")
            print("\t██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝███████╗██║██║ ╚████║███████╗")
            print("\t╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝")
            print("\t════════════════════════ v1.0.0 REWRITE ══════════════════════════")

            #	ALL OPTIONS
            print("================================================================================")
            print(
                "1. Video URL\n2. Video URL (Autoplay)\n3. Video Search\n4. Video Search (Autoplay)\n5. Playlist URL\n6. Playlist Search\n7. Exit")
            print("================================================================================")

            #	ENTER CHOICE
            flag = int(input("Enter Number for Choice: "))

            if flag == 1:
                #	INPUT VIDEO URL
                url = input("Enter URL: ")
                # url = "https://www.youtube.com/watch?v=8UVNT4wvIGY"	# For bug fixing
                try:
                    self.playvideo(url)
                except KeyboardInterrupt:
                    self.media.stop()
                    del self.media
                    pass

            elif flag == 2:
                #	INPUT VIDEO URL
                url = input("Enter URL: ")
                # url = "https://www.youtube.com/watch?v=2ZIpFytCSVc"	# For bug fixing
                try:
                    self.autoplay(url)
                except KeyboardInterrupt:
                    self.media.stop()
                    del self.media
                    self.video_ids.clear()
                    pass

            elif flag == 3:
                #	INPUT SEARCH TERM
                search = input("Enter Search Term: ")
                # search = "Stephen - play me like a violin"				# For bug fixing
                url = self.search_youtube(search)
                try:
                    self.playvideo(url)
                except KeyboardInterrupt:
                    self.media.stop()
                    del self.media
                    pass

            elif flag == 4:
                #	INPUT SEARCH TERM
                search = input("Enter Search Term: ")
                # search = "Stephen - play me like a violin"				# For bug fixing
                url = self.search_youtube(search)
                try:
                    self.autoplay(url)
                except KeyboardInterrupt:
                    self.media.stop()
                    del self.media
                    self.video_ids.clear()
                    pass

            elif flag == 5:
                #	INPUT PLAYLIST URL
                url = input("Enter Playlist URL: ")
                try:
                    self.play_playlist(url)
                except KeyboardInterrupt:
                    self.media.stop()
                    del self.media
                    self.video_ids.clear()
                    pass

            elif flag == 6:
                #	INPUT SEARCH TERM
                search = input("Enter Search Term: ")
                try:
                    self.search_playlist(search)
                except KeyboardInterrupt:
                    self.media.stop()
                    del self.media
                    self.video_ids.clear()
                    pass

            elif flag == 7:
                exit(7)

            else:
                print("\nPleas Input a Number Between 1 and 7!")

if __name__ == '__main__':
    al = AudioLine()
    al.menu()
