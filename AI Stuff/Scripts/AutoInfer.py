from audio_separator import Separator
from pydub import AudioSegment
import shutil
import os
from yt_dlp import YoutubeDL
import subprocess
#import sys

def infer(URL, DirWAV, SongName, BackingAmp, SingerName, Octave, Module):
    
    #WAV COLLECTION
    #Determine WAV selection
    #A. URL
    #B. WAV File
    #C. Banked Song
    ColletionMethod = 0
    print("Determining Collection Method")
    if(URL != ""): 
        print("URL Was Chosen")
        #WAV_Path = os.path.splitext(os.path.basename(subprocess.getoutput(f'yt-dlp --print filename {URL}')))[0] + ".wav"
        WAV_Path = f'{SongName}.wav'
        ydl_opts = {
            'outtmpl': WAV_Path,
            'final_ext': 'wav',
            'format': 'bestaudio/best',
            'nopart': True,
            'postprocessors':
                [{'key': 'FFmpegExtractAudio',
                'nopostoverwrites': False,
                'preferredcodec': 'wav',
                'preferredquality': '5'}]}
        print("Downloading YouTube Video As WAV.")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(URL)
        print("Done downloading YT WAV")
        #Download URL wav
        #output wav path
        ColletionMethod = 1
        
    elif(DirWAV != ""):
        print("Un-Split Local WAV Chosen")
        #output wav path
        WAV_Path = DirWAV
        ColletionMethod = 1
    elif(SongName != ""):
        print("Banked Song Chosen")
        ColletionMethod = 2
    else:
        print("No Source Material Method Found")
        
    print(f"The song name is saved as: {SongName}\n")
    
    #SPLITING WAV
    #Split WAV if URL or WAV File
    #Clean Up files from split
    #Skip if Banked Song
    #Generate Path For Instrumental & Vocals
    print("Maching collection method to appropiate case")
    match ColletionMethod:
        case 0:
            print("No ColletionMethod set")
            return False
        case 1:
            print("Seperating File.\n")
            separator = Separator(WAV_Path, model_name='UVR_MDXNET_KARA_2', use_cuda=True)
            InstrumentalPath, VocalsPath = separator.separate()
            print("file seperated")
            os.mkdir(f'C:/AI Stuff/Scripts/Splits/{SongName}/')
            os.rename(f'{os.path.splitext(os.path.basename(WAV_Path))[0]}_(Instrumental)_UVR_MDXNET_KARA_2.wav',f'C:/AI Stuff/Scripts/Splits/{SongName}/{SongName}_(Instrumental).wav')
            os.rename(f'{os.path.splitext(os.path.basename(WAV_Path))[0]}_(Vocals)_UVR_MDXNET_KARA_2.wav',f'C:/AI Stuff/Scripts/Splits/{SongName}/{SongName}_(Vocals).wav')
            InstrumentalPath = f'C:/AI Stuff/Scripts/Splits/{SongName}/{SongName}_(Instrumental).wav'
            VocalsPath = f'C:/AI Stuff/Scripts/Splits/{SongName}/{SongName}_(Vocals).wav'
            shutil.move(WAV_Path, f'C:/AI Stuff/Scripts/Splits/{SongName}/{SongName}.wav')
            print("Files renamed & moved into splits directory")
            #URL or Local WAV
            #Construct directory off of song name
            #Split wav in created directory with correct name
            #Move original into directory & rename
            #Delete Original wav
            #output path to vocals & instrumental
        case 2:
            try:
                InstrumentalPath = f'C:/AI Stuff/Scripts/Splits/{SongName}/{SongName}_(Instrumental).wav'
                VocalsPath = f'C:/AI Stuff/Scripts/Splits/{SongName}/{SongName}_(Vocals).wav'
                print("Pre-Splits found.")
            except:
                print("Curently you must use a pre-split from the splits directory. Specifically the host split.")
                return False
            #Banked Song
            #output path to vocals & instrumental
        case default:
            print("Good Luck") 
            return False
    
    
    print(f"\nInstrumentals Path: {InstrumentalPath}")
    print(f"Vocals Path: {VocalsPath}\n")
    
    print("Contructing Singer Directory")
    SingerDirectory = f"C:\AI Stuff\Voice Models\{SingerName}"
    #Get Singer .pth & .index paths
    for file in os.listdir(SingerDirectory):
        if file.endswith(".pth"):
            SingerModel = os.path.join(SingerDirectory, file)[3:]
        if file.endswith(".index"):
            SingerIndex = os.path.join(SingerDirectory, file)[3:]
    print("Singer Directory Constructed\n")
    
    #VOCAL INFERENCE
    bash_command = ["C:\AI Stuff\RVC\go-embed.bat", VocalsPath, SingerModel, SingerIndex, Octave, Module]
    print("Runing Infer Bash Command")
    subprocess.run(bash_command)
    print("Done Infering Vocal Track\n")
    #Infer Vocals with module as singer
    #Prepare infered vocals & instrumental
    InferedVocals = AudioSegment.from_wav("InferedVocals.wav")
    Instrumental = AudioSegment.from_wav(InstrumentalPath)

    
    #AMPLIFICATION, & MERGE
    print("Amping Instrumental")
    Instrumental = Instrumental + int(BackingAmp)
    print("Instrumental Amped")
    print("Overlapping Tracks")
    TracksOverlapped = Instrumental.overlay(InferedVocals, position=0)
    print("Tracks overlapped")
    #Modify Backing with amp
    #Merge InferedVocals with backing
    
    #OUTPUT & CLEANUP
    print("Exporting")
    TracksOverlapped.export(f"Cover of {SongName} by {SingerName} at {Octave} Octave.wav", format="wav")
    print(f"Exported. Saved as Cover of {SongName} by {SingerName} at {Octave} Octave.wav\n")
    #Output Covered Song with Correct Name
    #Clean Up files.(Delete infered vocals)
    print("Cleaing Up Files\n")
    os.remove("InferedVocals.wav")
    print("Files Cleaned Up.\n")
    
    return True
