import glob
import os
import tkinter
from tkinter import filedialog
from winotify import Notification
import AutoInfer
#How to init the GUI
#Generate list of banked songs
#send to dropdown
def initGUI(self):
    BankedSongs = []
    GlobedSongsList = glob.glob("C:\AI Stuff\Scripts\Splits\*")
    for song in GlobedSongsList:
        BankedSongs.append(os.path.basename(song))

    self.banked_input.addItems(BankedSongs)


    #Generate list of singers
    #send to dropdown
    Signers = []
    GlobedSingersList = glob.glob("C:\AI Stuff\Voice Models\*")
    for singer in GlobedSingersList:
        if 'zip' in singer:
            pass
        else:
            Signers.append(os.path.basename(singer))
    self.singer_input.addItems(Signers)
    
    InferQue = []
    return InferQue


    #How to Construct A Que
    #Get Respective wav dir/path
    #Get song name
    #Get octave
    #Get amp
    #Get url
    #Get singer directory
    #Get module
    #Get banked song dir

    

class que:
  def __init__(self, URL, DirWAV, SongName, BackingAmp, SingerName, Octave, Module):
    self.URL = URL
    self.DirWAV = DirWAV
    self.SongName = SongName
    self.BackingAmp = BackingAmp
    self.SingerName = SingerName
    self.Octave = Octave
    self.Module = Module
    

    
    
#BUTTONS

##Browse Button for local WAV
def BrowseWAV():
    ##Bring UP Directory Browser in set location downloads
    tkinter.Tk().withdraw()
    try:
        DirWAV = filedialog.askopenfilename(initialdir='C:\AI Stuff\Scripts\Splits', filetypes=[("WAV", "*.wav")])
        self.split_input.setPlainText(DirWAV)
    except:
        print("Browse Cancelled\n")

##Add to que button
def AddQue(self, InferQue):
    ##Create New Class
    ##Get set class to values
    ##send class to infer que
    print("Adding New Infer To Que")
    
    
    SongName = self.song_input.toPlainText()
    print(f"Song Input Gathered: {SongName}")
    Octave = self.octave_input.value()
    print(f"Octave Gathered: {Octave}")
    BackingAmp = self.amp_input.value()
    print(f"Amplification Gathered: {BackingAmp}")
    URL =  self.url_input.toPlainText()
    print(f"URL Gathered: {URL}")
    DirWAV = self.split_input.toPlainText()
    print(f"DirWAV Gathered: {DirWAV}")
    SingerName =  self.singer_input.currentText()
    print(f"SingerName Gathered: {SingerName}")
    BankedSongName = self.banked_input.currentText()
    print(f"BankedSongName Gathered: {BankedSongName}")
    if self.pm_check.isChecked():
        Module = 'pm'
    elif self.harvest_check.isChecked():
        Module = 'harvest'
    elif self.rvmpe_check.isChecked():
        Module = 'rmvpe'
    elif self.crepe_check.isChecked():
        Module = 'crepe'
    else:
        print("No module button checked")
        return False
    print(f"Module gathered: {Module}")
    if (SongName == ''):
        SongName = BankedSongName
    
    print("Creating Temp Class")
    TempQueClass = que(URL, DirWAV, SongName, BackingAmp, SingerName, str(Octave), Module)
    print("Appending Class")
    InferQue.append(TempQueClass)
    print("Class Appended")
    print(f"Que List Contains:\n {InferQue}")
    
    #I dont think we should reset all choices
    QueDisplayName = TempQueClass.SongName + ' by ' + TempQueClass.SingerName + ' at ' + str(TempQueClass.Octave)
    print(f"Add Que Name To Display as: {QueDisplayName}")
    
    self.que_display.addItem(QueDisplayName)
    print("Que Name added\n")
    

def RunInferJob(self, InferQue):
    ##For loop through inferque with infer.py
    print("Runing Infer Against Que\n")
    self.progressBar.setValue(0)
    self.progressBar.setMaximum(len(InferQue))
    for inferJob in InferQue:
        print(f"Runing InferJob of: {inferJob.SongName} by {inferJob.SingerName} at {str(inferJob.Octave)}")
        URL = inferJob.URL
        DirWAV = inferJob.DirWAV
        SongName = inferJob.SongName
        BackingAmp = inferJob.BackingAmp
        SingerName = inferJob.SingerName
        Octave = inferJob.Octave
        Module = inferJob.Module
        AutoInfer.infer(URL, DirWAV, SongName, BackingAmp, SingerName, Octave, Module)
        print("InferJob Completed. Moving to next if there's remaing.\n")
        self.progressBar.setValue(self.progressBar.value()+1)
    
    self.que_display.clear()
    if (self.song_input.toPlainText() != ''):
        self.song_input.clear()
    if (self.split_input.toPlainText() != ''):
        self.split_input.clear()
    if (self.url_input.toPlainText() != ''):
        self.url_input.clear()
    
    print("All InferJobs Done\n")
    self.progressBar.setValue(0)
    CompletionNotify = Notification(app_id="AI Cover Script", title="Completed", msg="The inference is done.", duration="short")
    CompletionNotify.show()
    InferQue.clear()
