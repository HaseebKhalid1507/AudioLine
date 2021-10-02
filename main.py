import pafy , vlc , urllib.request , re , inquirer , sys
from time import sleep
from rich.progress import track, Progress
from youtubesearchpython import PlaylistsSearch
from os import system
from colors import bcolors

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

        #	ADD URL TO LIST OF PLAYED SONGS
        self.played.append(url)

        #	INITIALIZE VIDEO
        video = pafy.new(url)
        audio = video.getbestaudio()
        self.media = vlc.MediaPlayer(audio.url)

        #	PRINT VIDEO DETAILS
        print(f"\n{'-' * 70}\n")

        print(bcolors.HEADER + "Now Playing: " + bcolors.OKCYAN + video.title)
        print(bcolors.HEADER + "\nViews: " + bcolors.OKCYAN + f"{video.viewcount:,d}")
        print(bcolors.HEADER + "\nDuration: " + bcolors.OKCYAN + video.duration)
        print(bcolors.WARNING + "\nPress 'CTRL+C' to Skip Song!\n" + bcolors.ENDC)

        with Progress(transient=True) as prog:
            song_play = prog.add_task(
                "[green]Playing Song", total=video.length)

            #	START PLAYER
            self.media.play()

            while self.media.is_playing() == False:
                pass

            while self.media.is_playing():
                sleep(1)
                prog.update(song_play, advance=1)

        print(bcolors.OKGREEN + "DONE PLAYING %s!" % video.title)

    #	FUNCTION TO KEEP PLAYING SONGS
    def autoplay(self, url):
        #	PLAY CURRENT VIDEO
        self.playvideo(url)

        self.video_ids = []
        video_ids_dupes = []
        #	CHANGE CURRENT VIDEO TO NEXT ONE
        html = urllib.request.urlopen(url)
        video_ids_dupes = re.findall(
            r"watch\?v=(\S{11})", html.read().decode())

        #	REMOVE DUPLICATES FROM LIST
        for i in video_ids_dupes:
            if "https://www.youtube.com/watch?v=" + i not in self.played:
                self.autoplay("https://www.youtube.com/watch?v=" + i)
                # RECURSION PAGMAN

    #	FUNCTION TO TAKE FIRST VIDEO FROM YOUTUBE SEARCH PAGE

    def search_youtube(self, search: str):
        # Check if the given search term is a valid youtube video link
        if(search.startswith("https://www.youtube.com")):
            res = urllib.request.urlopen(search)

            if(res.getcode() == 200):
                return search

        search_url = "https://www.youtube.com/results?search_query={}" + search.replace(" ", "+")

        html = urllib.request.urlopen(search_url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = ("https://www.youtube.com/watch?v=" + video_ids[0])
        return url

    #	FUNCTION TO PLAY VIDEOS IN A PLAYLIST
    def play_playlist(self, url):

        html = urllib.request.urlopen(url)
        video_ids_dupes = re.findall(
            r"watch\?v=(\S{11})", html.read().decode())

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

        cls()

        print(bcolors.HEADER + "")
        print("\t █████╗ ██╗   ██╗██████╗ ██╗ ██████╗ ██╗     ██╗███╗   ██╗███████╗")
        print("\t██╔══██╗██║   ██║██╔══██╗██║██╔═══██╗██║     ██║████╗  ██║██╔════╝")
        print("\t███████║██║   ██║██║  ██║██║██║   ██║██║     ██║██╔██╗ ██║█████╗  ")
        print("\t██╔══██║██║   ██║██║  ██║██║██║   ██║██║     ██║██║╚██╗██║██╔══╝  ")
        print("\t██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝███████╗██║██║ ╚████║███████╗")
        print("\t╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝")
        print("\t════════════════════════ v1.0.0 REWRITE ══════════════════════════" , bcolors.ENDC , "\n")

        questions = [
            inquirer.List('option',
                        message="Choose An Option",
                        choices=['Video Search/URL', 'Video Search/URL (Autoplay)', 'Playlist URL', 'Playlist Search', 'Exit'],
                    ),
        ]

        flag = inquirer.prompt(questions)["option"]

        #	ENTER CHOICE
        if flag == "Video Search/URL":
            #	INPUT SEARCH TERM
            search = input(bcolors.OKCYAN + "Enter Search Term/URL: " + bcolors.ENDC)
            print(bcolors.ENDC , end="")
            # search = "Stephen - play me like a violin"				# For bug fixing
            url = self.search_youtube(search)
            try:
                self.playvideo(url)
            except KeyboardInterrupt:
                self.media.stop()
                del self.media
                # Terminate the program on KeyBoardInterrupt
                exit()

        elif flag == "Video Search/URL (Autoplay)":
            #	INPUT SEARCH TERM
            search = input(bcolors.OKCYAN + "Enter Search Term/URL: " + bcolors.ENDC)
            # search = "off the grid"				# For bug fixing
            url = self.search_youtube(search)
            try:
                self.autoplay(url)
            except KeyboardInterrupt:
                self.media.stop()
                del self.media
                self.video_ids.clear()
                exit()

        elif flag == 'Playlist URL':
            #	INPUT PLAYLIST URL
            url = input(bcolors.OKCYAN + "Enter Playlist URL: " + bcolors.ENDC)

            try:
                self.play_playlist(url)
            except KeyboardInterrupt:
                self.media.stop()
                del self.media
                self.video_ids.clear()
                exit()

        elif flag == 'Playlist Search':
            #	INPUT SEARCH TERM
            search = input(bcolors.OKCYAN + "Enter Search Term: " + bcolors.ENDC)
            
            try:
                self.search_playlist(search)
            except KeyboardInterrupt:
                self.media.stop()
                del self.media
                self.video_ids.clear()
                exit()
                

        elif flag == 'Exit':
            exit()


if __name__ == '__main__':
    al = AudioLine()
    try:
        al.menu()
    except:
        print(bcolors.FAIL + "Exiting...")
