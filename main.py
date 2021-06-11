import pafy
import vlc
import urllib.request
import re
from time import sleep
from progress.bar import FillingSquaresBar
from youtubesearchpython import PlaylistsSearch

#	HOLDS ALL PLAYED VIDEOS
played = []

#	FUNCTION TO PLAY AUDIO
def playvideo(url):
	#	INITIALIZE VIDEO
	video = pafy.new(url)
	audio = video.getbestaudio()
	media = vlc.MediaPlayer(audio.url)

	#	PRINT VIDEO DETAILS
	print("\n--------------------------------------------------------------------------------")
	print("\nNOW PLAYING: \n\t" + video.title)
	#print (video.duration)
	print("\tViews:  " + f"{video.viewcount:,d}" + "\t\t\tDuration:  " + video.duration)

	#	ITITIALIZE PROGRESS BAR
	bar = FillingSquaresBar("\tPlaying for:", max=(video.length))

	#	START PLAYER
	media.play()

	while media.is_playing() == False:
		pass
	
	#	INCREMENT BAR
	bar.next()
	while media.is_playing():
		sleep(1)
		#media.stop()			#	FOR BUG FIXING
		bar.next()
	bar.finish()

#	FUNCTION TO KEEP PLAYING SONGS
def autoplay(url):
	#	ADD URL TO LIST OF PLAYED SONGS
	played.append(url)
	#	PLAY CURRENT VIDEO
	playvideo(url)

	#	CHANGE CURRENT VIDEO TO NEXT ONE
	html = urllib.request.urlopen(url)
	video_ids_dupes = re.findall(r"watch\?v=(\S{11})", html.read().decode())
	video_ids = []

	#	REMOVE DUPLICATES FROM LIST
	for i in video_ids_dupes:
		if i not in video_ids and "https://www.youtube.com/watch?v="+i not in played:
			video_ids.append(i)
	url = ("https://www.youtube.com/watch?v=" + video_ids[0])
	
	#	RECURSION PAGMAN
	autoplay(url)

#	FUNCTION TO TAKE FIRST VIDEO FROM YOUTUBE SEARCH PAGE
def search_youtube(search):
	search_url = "https://www.youtube.com/results?search_query=" + search.replace(" ", "+")
	html = urllib.request.urlopen(search_url)
	video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
	url = ("https://www.youtube.com/watch?v=" + video_ids[0])
	return url

#	FUNCTION TO PLAY VIDEOS IN A PLAYLIST
def play_playlist(url):

	html = urllib.request.urlopen(url)
	video_ids_dupes = re.findall(r"watch\?v=(\S{11})", html.read().decode())
	video_ids = []

	#	REMOVE DUPLICATES FROM LIST
	for i in video_ids_dupes:
		if i not in video_ids and "https://www.youtube.com/watch?v="+i not in played:
			video_ids.append(i)

	for i in video_ids:
		playvideo("https://www.youtube.com/watch?v="+i)

#	FUNCTION TO TAKE FIRST PLAYLIST FROM YOUTUBE SEARCH PAGE
def search_playlist(search):
	playlistsSearch = PlaylistsSearch(search, limit = 1)
	play_playlist(playlistsSearch.result()["result"][0]["link"])

#	MAIN SCRIPT FUNCTION
def main():

	print("")
	print("\t █████╗ ██╗   ██╗██████╗ ██╗ ██████╗ ██╗     ██╗███╗   ██╗███████╗")
	print("\t██╔══██╗██║   ██║██╔══██╗██║██╔═══██╗██║     ██║████╗  ██║██╔════╝")
	print("\t███████║██║   ██║██║  ██║██║██║   ██║██║     ██║██╔██╗ ██║█████╗  ")
	print("\t██╔══██║██║   ██║██║  ██║██║██║   ██║██║     ██║██║╚██╗██║██╔══╝  ")
	print("\t██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝███████╗██║██║ ╚████║███████╗")
	print("\t╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝")
                                                                  
	flag = 0

	while flag != 7:
		
		#	ALL OPTIONS
		print("================================================================================")
		print("1. Video URL\n2. Video URL (Autoplay)\n3. Video Search\n4. Video Search (Autoplay)\n5. Playlist URL\n6. Playlist search\n7. Exit")
		print("================================================================================")
		
		#	ENTER CHOICE
		flag = int(input("Enter number for choice: "))

		if flag == 1:
			#	INPUT VIDEO URL
			url = input("Enter URL: ")
			#url = "https://www.youtube.com/watch?v=8UVNT4wvIGY"	# For bug fixing
			playvideo(url)

		elif flag == 2:
			#	INPUT VIDEO URL
			url = input("Enter URL: ")
			#url = "https://www.youtube.com/watch?v=2ZIpFytCSVc"	# For bug fixing
			autoplay(url)

		elif flag == 3:
			#	INPUT SEARCH TERM
			search = input("Enter search term: ")
			#search = "Stephen - play me like a violin"				# For bug fixing
			url = search_youtube(search)
			playvideo(url)

		elif flag == 4:
			#	INPUT SEARCH TERM
			search = input("Enter search term: ")
			#search = "Stephen - play me like a violin"				# For bug fixing
			url = search_youtube(search)
			autoplay(url)

		elif flag == 5:
			#	INPUT PLAYLIST URL
			url = input("Enter playlist url: ")
			play_playlist(url)

		elif flag == 6:
			#	INPUT SEARCH TERM
			search = input("Enter search term:")
			search_playlist(search)

		else:
			print("\nPleas input number between 0 and 8")

if __name__ == "__main__":
	main()