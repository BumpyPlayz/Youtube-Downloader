from pytube import YouTube
from pytube import Playlist
from prettytable import PrettyTable
import os
from os import path
import os

Save_Path = 'VideoDownload'

playlist = input("Please enter link to Playlist: ")

global totalsize
totalsize = 0

def progressBar(current, total, bytes_done, bytes_total, barLength=40):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent / 100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %% %s' % (arrow, spaces, percent, str(bytes_done) + "/" + str(bytes_total)),
          end='\r')

previousprogress = 0

def on_progress(stream, chunk, bytes_remaining):
    global previousprogress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = (int)(bytes_downloaded / total_size * 100)
    if liveprogress > previousprogress:
        previousprogress = liveprogress
        progressBar(liveprogress, 100, round(bytes_downloaded / 1024 / 1024, 2), round(total_size / 1024 / 1024, 2))


def findbestvideo(mp4files):
    maxres = None
    maxfps = None
    maxitagnum = None
    maxmb = None

    def formatres(res):
        res = res[:-1]
        res = int(res)
        return res

    for typ in mp4files:
        if maxres == None:
            maxres = typ.resolution
            maxfps = typ.fps
            maxitagnum = typ.itag
            maxmb = round(typ.filesize/1024/1024, 2)
        elif formatres(typ.resolution) >= formatres(maxres):
            if typ.fps >= maxfps:
                maxres = typ.resolution
                maxfps = typ.fps
                maxitagnum = typ.itag
                maxmb = round(typ.filesize / 1024 / 1024, 2)
    return maxitagnum, maxres, maxfps, maxmb

def findbestaudio(audiofil):
    maxres = None
    maxitagnum = None
    maxmb = None

    def formatres(res):
        res = res[:-4]
        res = int(res)
        return res

    for typ in audiofil:
        if maxres == None:
            maxres = typ.abr
            maxitagnum = typ.itag
            maxmb = round(typ.filesize / 1024 / 1024, 2)
        elif formatres(typ.abr) >= formatres(maxres):
                maxres = typ.abr
                maxitagnum = typ.itag
                maxmb = round(typ.filesize / 1024 / 1024, 2)
    return maxitagnum, maxres, maxmb


FileName = input("Enter Name to start downloading: ")
Continue = None

try:
    if path.exists(Save_Path):
        if path.exists(os.path.join(Save_Path, FileName)):
            print()
            print()
            print()
            text = "There is already a file called"+FileName+'in'+Save_Path+'Folder. Please type continue to begin download or type exit to stop. This will remove the old file: '

            while Continue == None:
                val = input(text)
                if str.lower(val) == "continue":
                    Continue = True
                    os.remove(os.path.join(Save_Path, FileName))
                    os.mkdir(os.path.join(Save_Path, FileName))
                elif str.lower(val) == "exit":
                    Continue = False
                else:
                    print("Please Input a valid value")
        else:
            os.mkdir(os.path.join(Save_Path, FileName))
            Continue = True
    else:
        os.mkdir(Save_Path)
        os.mkdir(Save_Path+'/'+FileName)
        Continue = True
except:
    Exception("A lot went wrong")

typeoffile = None

while not typeoffile:
    typeoffile = input('Would you like to download video or audio: ')

    if str.lower(typeoffile)=='video':
        typeoffile='video'
    elif str.lower(typeoffile)=='audio':
        typeoffile='audio'
    else:
        typeoffile=None

totaldownloaded = []

if Continue:
    try:
        pl_response = Playlist(playlist)
        for vid_item in pl_response:
            VideoInfo = YouTube(vid_item)
            VideoInfo.register_on_progress_callback(on_progress)
            VideoFiles = VideoInfo.streams.filter(file_extension="mp4", type="video", progressive="True")
            AudioFiles = VideoInfo.streams.filter(file_extension="mp4", type='audio')
            downloading = None
            if VideoFiles[0] and typeoffile=='video':
                downloading, r, f, mb = findbestvideo(VideoFiles)
                totaldownloaded.append([VideoInfo.title, r,f,mb])
            elif AudioFiles[0] and typeoffile=='audio':
                downloading, r, mb = findbestaudio(AudioFiles)
                totaldownloaded.append([VideoInfo.title, r, mb])
            if downloading:
                Video = VideoInfo.streams.get_by_itag(downloading)
                Video.download(output_path=os.path.join(Save_Path, FileName))
                print()
                print("Download Done.")
                print("Video can be found in", Save_Path+'/'+str(FileName), "Folder with file name", '\"', VideoInfo.title +" \".")
                previousprogress = 0
                totalsize += Video.filesize
            else:
                print("Something went wrong while downloading a video. Video ID:", VideoInfo.title)

            print()

        print()
        print()
        print("All Videos Downloaded")
        num = 1

        if typeoffile=='video':
            newtab = PrettyTable()
            newtab.field_names = ['Index', 'Name', 'Resolution', 'FPS', 'FileSize (MB)']
            for x in totaldownloaded:
                newtab.add_row([num, x[0], x[1], x[2], x[3]])
                num +=1

            newtab.add_row(['Total', '', '', '', ''])
            newtab.add_row([len(totaldownloaded), '', '', '', round(totalsize / 1024 / 1024, 2)])
            print(newtab)
        else:
            newtab = PrettyTable()
            newtab.field_names = ['Index', 'Name', 'Quality', 'FileSize (MB)']
            for x in totaldownloaded:
                newtab.add_row([num, x[0], x[1], x[2]])
                num += 1

            newtab.add_row(['Total', '', '', ''])
            newtab.add_row([len(totaldownloaded), '', '', round(totalsize / 1024 / 1024, 2)])
            print(newtab)
    except:
        print("Unknown Error Occured. Please check the playlist id")
