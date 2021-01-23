from pytube import YouTube
from prettytable import PrettyTable
import os
from os import path

link = input("Enter the video link to download: ")

Save_Path = 'VideoDownload'


previousprogress = 0


def progressBar(current, total, bytes_done, bytes_total, barLength = 40):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent/100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %% %s' % (arrow, spaces, percent, str(bytes_done)+"/"+str(bytes_total)), end='\r')


def on_progress(stream, chunk, bytes_remaining):
    global previousprogress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = (int)(bytes_downloaded / total_size * 100)
    if liveprogress > previousprogress:
        previousprogress = liveprogress
        progressBar(liveprogress, 100, round(bytes_downloaded / 1024 / 1024, 2), round(total_size / 1024 / 1024, 2))


VideoInfo = YouTube(link)
VideoInfo.register_on_progress_callback(on_progress)


try:
    global VideoFiles
    VideoFiles = VideoInfo.streams.filter(file_extension="mp4", type="video", progressive="True")

    global AudioFiles
    AudioFiles = VideoInfo.streams.filter(file_extension="mp4", type='audio')

except:
    Exception('Something went wrong')

print()
print()
print()

ChosenType = ""


if VideoFiles[0] and AudioFiles[0]:
    print('Video:', len(VideoFiles))
    print('Audio:', len(AudioFiles))
    print()
    print()
    while ChosenType == "":
        ChosenType = input('Input the type of file you want to download: ')

        if ChosenType == "1" or str.lower(ChosenType) == "video":
            ChosenType = "Video"
        elif ChosenType == "2" or str.upper(ChosenType) == "audio":
            ChosenType = "Audio"
        else:
            print("Please enter a Valid Input")
            ChosenType = ""

elif VideoFiles[0]:
    print("Only Video Formats Found.")
    ChosenType = "Video"
elif AudioFiles[0]:
    print("Only Audio Formats Found.")
    ChosenType = "Audio"
else:
    Exception("Something have gone wrong")

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
            maxmb = round(typ.filesize_approx/1024/1024, 2)
        elif formatres(typ.resolution) >= formatres(maxres):
            if typ.fps >= maxfps:
                maxres = typ.resolution
                maxfps = typ.fps
                maxitagnum = typ.itag
                maxmb = round(typ.filesize_approx / 1024 / 1024, 2)
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
            maxmb = round(typ.filesize_approx / 1024 / 1024, 2)
        elif formatres(typ.abr) >= formatres(maxres):
                maxres = typ.abr
                maxitagnum = typ.itag
                maxmb = round(typ.filesize_approx / 1024 / 1024, 2)
    return maxitagnum, maxres, maxmb
num = 1

Selected = ""

if ChosenType == "Video":
    tab = PrettyTable()
    tab.field_names = ['Index', 'Itag', 'Resolution', 'FPS', 'Size (MB)']
    bestnum = 0
    maxi, maxr, maxf, maxmb = findbestvideo(VideoFiles)
    for video in VideoFiles:
        if video.itag == maxi:
            bestnum = num

        tab.add_row([num, video.itag, video.resolution, video.fps, round(video.filesize_approx/1024/1024, 2)])
        num += 1
    tab.add_row(['', '', '', '', ''])
    tab.add_row(['Best: ', '', '', '', ''])
    tab.add_row([bestnum, maxi, maxr, maxf, maxmb])
    print(tab)

    while Selected == "":
        num = 1
        invalue = input("Enter index or Itag to start download: ")
        if invalue.isdigit():
            for vid in VideoFiles:
                if vid.itag == invalue or num == int(invalue):
                    Selected = vid.itag
                num += 1
            if Selected == "":
                print("Please enter a valid Option")
        else:
            print("Please enter a valid Option")
else:
    tab = PrettyTable()
    tab.field_names = ['Index', 'Itag', 'Quality', 'Size (MB)']
    maxi, maxr, maxmb = findbestaudio(AudioFiles)
    bestnum = 0
    for audio in AudioFiles:
        if audio.itag == maxi:
            bestnum = num
        tab.add_row([num, audio.itag, audio.abr, round(audio.filesize_approx / 1024 / 1024, 2)])
        num += 1

    tab.add_row(['', '', '', ''])
    tab.add_row(['Best: ', '', '', ''])

    tab.add_row([bestnum, maxi, maxr, maxmb])
    print(tab)

    while Selected == "":
        num = 1
        invalue = input("Enter index or Itag to start download: ")
        if invalue.isdigit():
            for vid in AudioFiles:
                if vid.itag == invalue or num == int(invalue):
                    Selected = vid.itag
                num += 1
            if Selected == "":
                print("Please enter a valid Option")
        else:
            print("Please enter a valid Option")

FileName = input("Enter Name to start downloading: ")
Continue = None

try:
    if path.exists(Save_Path):
        if path.exists(Save_Path+'/'+FileName):
            print()
            print()
            print()
            text = "There is already a file called", FileName,'in', Save_Path,'Folder. Please type continue to begin download or type exit to stop. This will remove the old file: '

            while Continue == None:
                val = input(text)
                if str.lower(val) == "continue":
                    Continue = True
                elif str.lower(val) == "exit":
                    Continue = False
                else:
                    print("Please Input a valid value")
        else:
            Continue = True
    else:
        os.mkdir(Save_Path)
        Continue = True
except:
    Exception("A lot went wrong")


if Continue == True:
    print("Starting Download")
    try:
        video = VideoInfo.streams.get_by_itag(Selected)
        video.download(output_path=Save_Path, filename=FileName)
        print()
        print("Download Done.")
        print("Video can be found in", Save_Path, "Folder with file name", FileName+".")

    except:
        Exception("Cannot Download File")

else:
    print("Aborting Download")
