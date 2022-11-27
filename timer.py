from tkinter import *
import time
import pickle
from functools import partial
root = Tk()  #Creating window using Tkinter 
root.title(" Timer ")  #Giving a name to Tkinter window

#Assigning variables to use them later in textboxes
hours = StringVar(value="0")
minutes = StringVar(value="0")
seconds = StringVar(value="0")
timerName = StringVar()
curTime = StringVar()

x = False #Variable used to stop timer in case pause/continue button pressed
timers = [] #Creating empty list to use as a place to store timers saved by user

#Utilizing pickle library to assign values stored in timers.pickle to "timers" list
with open('timers.pickle', 'rb') as f:
    timers = pickle.load(f)

#Function that handles what happens when when pause/continue button pressed by reversing value of x
def buttonPressed(time, saveTime):
    global x
    if x:
        x = False
    else:
        x = True
    global curTime
    root.update()
    loop(time, saveTime)

def intCheck(var):  # Function, that checks if a certain variale is an integer
    if not(str(var).isnumeric()):
        return False
    else:
        return True

#Function that clears Tkinter interface(GUI) by deleting all widgets
def clearGui():
    for w in root.winfo_children(): #This part goes through each child of root and deletes it
        w.destroy()
#Function responsible for drawing main menu
def main_menu():
    clearBoxes()
    time.sleep(1)
    global x
    x = True
    clearGui()
    #Utilizing partial function in button commands is usually necessary
    #because otherwise these function will be called when upper function
    timerButton = Button(root, text="New Timer", command=partial(timer))
    timerButton.grid(column=0, row=0) 
    listButton = Button(root, text="List of saved timers", command=partial(timerList))
    listButton.grid(column=1, row =0)

#Function responsible for drawing menu with user-saved timers
def timerList():
    clearGui()
    menu = Button(root, text="menu", command=partial(main_menu))
    menu.grid(column=4, row = 0)
    #Creates buttons and labels for each index in "timers" list
    for i in range (len(timers)):
        #Splitting seconds stored in dictionary for each saved timer into hours, minutes and seconds
        hr = str(int(timers[i]["Current Time"])//3600)
        min = str(timers[i]["Current Time"]//60-(int(hr)*60))
        sec = str(timers[i]["Current Time"]-int(hr)*3600-int(min)*60)
        LabelText = hr+":"+min+":"+sec
        timerNameLabel = Label(root, text = timers[i]["Name"]).grid(column=0, row = i)
        timeLabel = Label(root, text = LabelText).grid(column = 1, row =i)
        #Buttons that call functions with the name of a user-saved timer to delete or start them
        timeStart = Button(root, text = "Start", command = partial(startSave, timers[i]["Name"])).grid(column=2, row = i)
        timeDelete = Button(root, text = "Delete", command = partial(deleteTimer, (timers[i]["Name"]))).grid(column=3,row=i)

#Function that deletes index from list based on the name parameter from taken from dictionary of user-saved timer
#and saves new "timers" list
def deleteTimer(name):
    #Begin cited code
    #https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
    timers.pop(next((index for (index, d) in enumerate(timers) if d["Name"] == name), None))
    #End cited code
    #Utilizing pickle library to "dump"(store) new list into timers.pickle file after deleting index from it
    with open('timers.pickle', 'wb') as f: 
        pickle.dump(timers, f)
    main_menu()

#Function that draws interface for restarted saved timer
def startSave(name):
    global x
    #Begin cited code
    #https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
    timeInSec = timers[next((index for (index, d) in enumerate(timers) if d["Name"] == name), None)]["Current Time"]
    #End cited code
    clearGui()
    x = False
    nameLabel = Label(root, text = name)
    nameLabel.grid(column = 0, row = 1)
    loop(timeInSec, timeInSec)

#Function that restores values of text boxes to default(0)
def clearBoxes():
    global hours
    global minutes
    global seconds
    hours = StringVar(value="0")
    minutes = StringVar(value="0")
    seconds = StringVar(value="0")
    root.update()

#Function responsible to draw interface to give a name to saved timer
def saveTimer(timeV):
    global x
    x = True
    time.sleep(1)
    clearGui()
    name = Entry(root, width=8, textvariable=timerName) #Text box to input name of the timer
    name.grid(column = 0, row = 0)
    done = Button(root, text="Done", command = partial(doneF,timeV))
    done.grid(column = 1, row =0)

#Function that stores data about user-saved timer into a dictionary and then into the "timers" list
def doneF(timeV):
    #If there aren't any timers with the same name as the one taken from text box from funtion "saveTimer" timer is stored
    if not any(q['Name'] == timerName.get() for q in timers):
        t = {
            "Name": timerName.get(),
            "Current Time": timeV
        }
        timers.append(t)
        #Utilizing pickle library to "dump"(store) new list into timers.pickle file after appending it with a new timer
        with open('timers.pickle', 'wb') as f:
            pickle.dump(timers, f)
        main_menu()
    #If requrement wasn't met error message will be displayed for 0.8 seconds
    else:
        errorLabel = Label(root, text ="Error")
        errorLabel.grid(column=1, row = 1)
        root.update()
        time.sleep(0.8)
        errorLabel.destroy()
        root.update()

#Function that draws timer itself and updates it every second
#"atime" parameter is getting less by 1 every second and represents total time in seconds left to countdown
#"saveTime" parameter is constant and utilized in case user wants to save the current timer
def loop(atime, saveTime): 
    global x    
    global curTime
    atime = int(atime)
    #Splitting seconds stored in "atime" into hours, minutes and seconds
    hr = atime//3600
    min = atime//60-((atime//3600)*60)
    sec = atime - hr*3600 - min*60
    #Variable "x" is utilized to pause loop if pause/continue button is pressed
    if not(x):
        Label(root, textvariable=curTime).grid(column=2, row=1) #Timer that shows current time left
        pause = Button(root, text="Pause/Continue", command=partial(buttonPressed, atime, saveTime))
        pause.grid(column = 0, row = 2)
        menu = Button(root, text="Menu", command=partial(main_menu))
        menu.grid(column = 5, row = 1)
        #If timer with inputted time(from text boxes in "timer" function) exists user won't be able to save it
        if not any(q['Current Time'] == saveTime for q in timers): 
            save = Button(root, text = "Save", command = partial(saveTimer, saveTime))
            save.grid(column = 1, row = 2)
        #If timer still has seconds left it will continue decresing 
        if atime > 0:
            curTime.set(str(hr)+":"+str(min)+":"+str(sec)) #Setting time label text
            atime = atime-1
            root.update()
            time.sleep(1)
            loop(atime, saveTime) #Restarting function with "atime" variable decreased by one
        #If timer is finished program will display "Done" message
        else: 
            done = Label(root, text = "Done")
            done.grid(column = 2, row = 2)
            curTime.set(str(0)+":"+str(0)+":"+str(0))
            root.update()
            time.sleep(2)
            done.destroy()
            root.update()



#Function that checks if data inputed into text boxes from "timer" functions are integers and calls "loop" function
def gui():
    if intCheck(hours.get()) and intCheck(minutes.get()) and intCheck(seconds.get()):
        global x
        x = False
        calc = int(hours.get())*60*60+int(minutes.get())*60+int(seconds.get()) #Calculating total time in seconds
        loop(calc, calc) #Function that will draw timer called with total time in seconds
    #If requrement wasn't met error message will be displayed for 0.8 seconds
    else:
        errorLabel = Label(root, text ="Error")
        errorLabel.grid(column=1, row = 1)
        root.update()
        time.sleep(0.8)
        errorLabel.destroy()
        root.update()

#Function that creates interface to start a timer
def timer():
    clearGui()
    #Text boxes for hours, minutes, seconds input by user
    hrField = Entry(root, width=8, textvariable=hours)#Variables assigned at the top of the code are linked to text boxes
    hrField.grid(column=0, row=0) 
    hoursLabel = Label(root, text ="hr")
    hoursLabel.grid(column=1, row = 0)
    minField = Entry(root, width=8, textvariable=minutes)
    minField.grid(column=2, row=0)
    minutesLabel = Label(root, text ="min")
    minutesLabel.grid(column=3, row = 0)
    secField = Entry(root, width=8, textvariable=seconds)
    secField.grid(column=4, row=0)
    secondsLabel = Label(root, text ="sec")
    secondsLabel.grid(column=5, row = 0)
    start = Button(root, text="Start", command=gui)
    start.grid(column=0, row=1)

main_menu()
root.mainloop() #Global loop for the whole window, which updated interface each time button is pressed