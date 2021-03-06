# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:09:18 2020

@author: Paul Schulte
"""

# import modules
import os, sys
import datetime
import queue
import logging
import signal
import time
import threading

# tkinter for gui
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
from tkinter import filedialog



# setting logger to log information
logger = logging.getLogger(__name__)

# import own classes
from InstagramBot import InstagramBot
import bot1, bot2, botLikeMode, bot4


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue
    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """
    
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)



class bot_general_UI:

    def __del__(self):
        try:
            del self.bot
        except:
            pass # kein bot initialisiert

    def __init__(self, frame):
        # save reference to frame
        self.frame = frame

        self.loggedin = False
        
        #####LOGIN-FIELD#######

        # username-field---------
        self.strVar_username = tk.StringVar()  # StringVar for username-field
        ttk.Label(self.frame, text='Username:').grid(column=0, row=0, sticky=W)  # label for username-field
        self.entry_username= ttk.Entry(self.frame, width=25, textvariable=self.strVar_username)  # entry for username-field with reference to StringVar for getting text
        
        # set default username for username-field
        self.strVar_username.set('bottest371') 
        # display the username-field
        self.entry_username.grid(row=0, column=1, sticky=(W, E))


        # password field
        self.strVar_password = tk.StringVar()  # StringVar for password-field
        ttk.Label(self.frame, text='Password:').grid(column=0, row=1, sticky=W)  # label for password-field
        self.entry_password= ttk.Entry(self.frame, width=25, textvariable=self.strVar_password)  # entry for password-field with reference to Stringvar
        self.entry_password.config(show="*")  # hiding password

        # set default password for password-field
        self.strVar_password.set('BotTestAccount1')
        # display the password-field
        self.entry_password.grid(row=1, column=1, sticky=(W, E))
        

        # checkbox for headless/minimize mode selection
        self.minimize = IntVar()
        Checkbutton(self.frame, text="Minimize", variable=self.minimize).grid(row=2, column=0, sticky=W)
        

        # Login-Button
        self.loginButton = ttk.Button(self.frame, text='Login', command=self.login)
        self.loginButton.grid(column=1, row=2, sticky=W)
        


        # horizontal separator
        ttk.Separator(self.frame).grid(row=3, columnspan=2, sticky="ew")




     
    #login function
    def login_thread(self):
        # initialize bot1 with minimize
        self.bot = self.__init_bot__() #bot1.bot1(False if self.minimize.get() == 0 else True)

        #login
        if self.bot.login(self.strVar_username.get(), self.strVar_password.get()) == -1:
            logger.error("Failed to login.")
            self.loggedin = False
        else:
            logger.warning(self.bot.bot_name + ": Logged in successfully.")
            self.loggedin = True
    
    # callback-function
    def login(self):
        if not self.loggedin: # just login if not already did
            logger.info("Logging into Instagram...")
            thread = threading.Thread(target=self.login_thread)
            thread.start()    
        
    
    # stop function
    def stop_thread(self):
        # pause bot
        self.bot.pause() 
    
    # callback-function
    def bot_stop(self):
        if self.loggedin:
            stopThread = threading.Thread(target=self.stop_thread)
            stopThread.start()
            #self.__del__()


    #start function
    def start_thread(self, key, amount, delay=5):
        # check if key-entry is empty
        if key != "":
            # check if amount is needed
            try:
                if self.check_amount:
                    # check if amount entry is empty
                    if amount == "":
                        logger.error(self.bot.bot_name + ": Fill in amount of posts to like/save")
                        return
                    else:
                        # save amount of images to like/save
                        amount = int(amount)
            except:
                pass
            
            # get delay
            if delay == "":
                # default value
                delay = 5
            else:
                try:
                    delay = float(delay)
                except:
                    logger.error(self.bot.bot_name + ": Fill in valid time")
                    return
            

            # staring bot and saving post-code
            logger.info(self.bot.bot_name + ": Starting " + self.bot.bot_name)
            post_code = self.__start_bot__(key, wait=delay, amount=amount)    #self.bot.start(key, wait=delay, amount=amount)
                
            # console-response
            if post_code > 0:
                logger.warning(self.bot.bot_name + ": Liked / saved all posts successfully.")
            elif post_code == -1:
                logger.error(self.bot.bot_name + ": Page does not exist!")
            elif post_code == -2:
                logger.error(self.bot.bot_name + ": Obtaining links failed!")
            elif post_code == -3:
                logger.error(self.bot.bot_name + ": " + self.bot.bot_name + " stopped!")
            elif post_code == -5:
                pass#logger.error("bot1: Unknown error in routine!")   #because error is printed by itself
            
            # starting self-control
            logger.info(self.bot.bot_name + ": starting self-control")
            control_code = self.__start_bot__(key, wait=delay, amount=amount)  #self.bot.start(key, wait=delay, amount=amount)

            # check control-code
            if control_code == 0:
                logger.warning(self.bot.bot_name + ": liked all " + str(amount) + " posts!")
            else:
                logger.error(self.bot.bot_name + ": self-control failed!")
        
                
        else:
            # key-entry is empty
            logger.error(self.bot.bot_name + ": Fill in " + self.key_name + ", please!")
            # warning
            if self.check_amount:
                if amount == "":
                    logger.error(self.bot.bot_name + ": Fill in amount of posts to like/save")

        

class bot1UI(bot_general_UI):
    
    #individual methods
    def __init_bot__(self):
        return bot1.bot1(False if self.minimize.get() == 0 else True)
    
    def __start_bot__(self, key, wait, amount):
        return self.bot.start(key, wait, amount=amount)


    def __init__(self, frame):
        self.check_amount = True
        self.key_name = "Account Name"
        
        
        bot_general_UI.__init__(self, frame)

        #####START-FIELD#####
        
        # Page-Name-field
        self.strVar_pagename = tk.StringVar()
        ttk.Label(self.frame, text='Page-Name').grid(column=0, row=4, sticky=W)
        self.entry_pagename = ttk.Entry(self.frame, width=25, textvariable=self.strVar_pagename)
        self.entry_pagename.grid(row=4, column=1, sticky=(W, E))
        

        # Amount-field
        ttk.Label(self.frame, text='Amount').grid(column=0, row=5, sticky=W)
        self.strVar_amount = tk.StringVar()
        self.entry_amount = ttk.Entry(self.frame, width=10, textvariable=self.strVar_amount)
        self.entry_amount.grid(row=5, column=1, sticky=(W, E))
        

        # Wait-time-field 
        self.strVar_wait = tk.StringVar()
        ttk.Label(self.frame, text='Wait time').grid(column=0, row=6, sticky=W)
        self.entry_wait = ttk.Entry(self.frame, width=10, textvariable=self.strVar_wait)
        self.entry_wait.grid(row=6, column=1, sticky=(W, E))
            
        
        # start-button
        self.start_button = ttk.Button(self.frame, text='Start', command=self.start)
        self.start_button.grid(column=0, row=7, sticky=W)


        # stop-button
        self.stop_button = ttk.Button(self.frame, text='Stop', command=self.bot_stop)
        self.stop_button.grid(column=1, row=7, sticky=W)

    
    def start(self):
        if self.loggedin: # just do if already logged in
            startThread = threading.Thread(target=self.start_thread,args=(self.strVar_pagename.get(), self.strVar_amount.get(), self.strVar_wait.get()))
            startThread.start()
        else:
            logger.error("bot1: Login first!")


class bot2UI(bot_general_UI):

    #individual methods
    def __init_bot__(self):
        return bot2.bot2(False if self.minimize.get() == 0 else True)
    
    def __start_bot__(self, key, wait, amount):
        return self.bot.start(key, wait, amount=amount)
    

    def __init__(self, frame):
        self.check_amount = True
        self.key_name = "Hashtag"
        
        bot_general_UI.__init__(self, frame)
        
        #####START-FIELD#####

        # hashtag-field
        self.strVar_hashtag = tk.StringVar()
        ttk.Label(self.frame, text='Hashtag').grid(column=0, row=4, sticky=W)
        self.entry_hashtag = ttk.Entry(self.frame, width=25, textvariable=self.strVar_hashtag)
        self.entry_hashtag.grid(row=4, column=1, sticky=(W, E))
        

        # amount-field
        ttk.Label(self.frame, text='Amount').grid(column=0, row=5, sticky=W)
        self.strVar_amount = tk.StringVar()
        self.entry_amount = ttk.Entry(self.frame, width=10, textvariable=self.strVar_amount)
        self.entry_amount.grid(row=5, column=1, sticky=(W, E))
        

        # wait-time-field
        ttk.Label(self.frame, text='Wait time').grid(column=0, row=6, sticky=W)
        self.strVar_wait = tk.StringVar()
        self.entry_wait = ttk.Entry(self.frame, width=10, textvariable=self.strVar_wait)
        self.entry_wait.grid(row=6, column=1, sticky=(W, E))
            
        
        # start button
        self.start_button = ttk.Button(self.frame, text='Start', command=self.start)
        self.start_button.grid(column=0, row=7, sticky=W)

        # stop button
        self.stop_button = ttk.Button(self.frame, text='Stop', command=self.bot_stop)
        self.stop_button.grid(column=1, row=7, sticky=W)
    
    def start(self):
        if self.loggedin:
            startThread = threading.Thread(target=self.start_thread,args=(self.strVar_hashtag.get(), self.strVar_amount.get(), self.strVar_wait.get()))
            startThread.start()
        else:
            logger.error("bot2: Login first!")
  
    
class bot4UI(bot_general_UI):
    
    #individual methods
    def __init_bot__(self):
        return bot4.bot4(False if self.minimize.get() == 0 else True)
    
    def __start_bot__(self, key, wait, amount):
        test = self.bot.start(key, wait)
        return test
    

    def __init__(self, frame):
        self.check_amount = False
        self.key_name = ""
        self.links = list([""])
        
        
        bot_general_UI.__init__(self, frame)

        #####START-FIELD#####
 
        # change links-button
        ttk.Label(self.frame, text="Change links").grid(column=0, row=4, sticky=W)
        self.button_links = ttk.Button(self.frame, text="change", command=self.change_links)
        self.button_links.grid(column=1, row=4, sticky=W)

        # Wait-time-field 
        self.strVar_wait = tk.StringVar()
        ttk.Label(self.frame, text='Wait time').grid(column=0, row=5, sticky=W)
        self.entry_wait = ttk.Entry(self.frame, width=25, textvariable=self.strVar_wait)
        self.entry_wait.grid(row=5, column=1, sticky=(W, E))
            
        
        # start-button
        self.start_button = ttk.Button(self.frame, text='Start', command=self.start)
        self.start_button.grid(column=0, row=6, sticky=W)


        # stop-button
        self.stop_button = ttk.Button(self.frame, text='Stop', command=self.bot_stop)
        self.stop_button.grid(column=1, row=6, sticky=W)
    
         
    def start(self):
        # garbage collector
        #gc.set_debug(gc.DEBUG_LEAK)

        if self.loggedin:
            self.start_thread(self.links, 0, self.strVar_wait.get())
        else:
            logger.error("bot4: Login first!")
        
        """
        if self.loggedin: # just do if already logged in
            startThread = threading.Thread(target=self.start_thread,args=(self.links, 0, self.strVar_wait.get())) # 0 for amount -> generalisation
            startThread.start()
        else:
            logger.error("bot4: Login first!")   #Tcl_AsyncDelete: async handler deleted by the wrong thread"""
        
        
        
    def change_links(self):
        if self.loggedin:

            # convert to list because its dynamic
            try:
                if type(self.links) == str:
                    self.links = list([self.links])
            except:
                pass

            change_links_UI = Change_links_UI(self.links)
            change_links_UI.mainloop()

            # convert back to string
            self.links = self.links[0].decode("utf-8") 
            
        else:
            logger.error("bot4: Login first!")

          

class Change_links_UI(tk.Frame):
    def __init__(self, links):
        self.links = links
        self.master = tk.Tk()
        tk.Frame.__init__(self, self.master)
        self.master.title("Links")
        self.createMenu()
        self.createPopUp()
        self.grid()

    def createMenu(self):

        # adding menubar
        top = self.winfo_toplevel()
        self.menuBar = tk.Menu(top)
        top["menu"] = self.menuBar

        # file-menu
        self.file_menu  = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="File", menu=self.file_menu)

        # adding open-button to file-menu
        self.file_menu.add_command(label="open", command=self.__open_file)


        # adding done
        self.menuBar.add_command(command=self.__done, label="Done")

             

        """
        tkinter.filedialog.asksaveasfilename()
        tkinter.filedialog.asksaveasfile()
        tkinter.filedialog.askopenfilename()
        tkinter.filedialog.askopenfile()
        tkinter.filedialog.askdirectory()
        tkinter.filedialog.askopenfilenames()
        tkinter.filedialog.askopenfiles()

        """




        # adding separator
        #self.file_menu.add_separator()






    def createPopUp(self):

        self.scrolled_text = ScrolledText(self, height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.insert(END, self.links[0])


    def __open_file(self):
        # get reference to file
        file = filedialog.askopenfilename(parent=self)
        #file = "TEST.links"

        # open and read file
        content_file = open(file, "r", encoding="utf8")
        content = content_file.read()
        
        self.scrolled_text.insert(END, content.encode('utf-8'))

        content_file.close()

    def __done(self):

        self.links[0] = (self.scrolled_text.get(1.0, END).encode('utf-8'))

        # close window
        self.master.destroy()
        self.quit()
        
                
        
     
        
class botLikeModeUI(bot_general_UI):
    
    #individual methods
    def __init_bot__(self):
        return botLikeMode.bot_like(False if self.minimize.get() == 0 else True)
    
    def __start_bot__(self, key, wait, amount):
        return self.bot.start(key, wait=delay, amount=amount)

    def __init__(self, frame):
        self.check_amount = True
        self.key_name = "Hashtag"
        
        
        bot_general_UI.__init__(self, frame)
        
        #####START-FIELD#####

        # hashtag-field
        self.strVar_hashtag = tk.StringVar()
        ttk.Label(self.frame, text='Hashtag').grid(column=0, row=4, sticky=W)
        self.entry_hashtag = ttk.Entry(self.frame, width=25, textvariable=self.strVar_hashtag)
        self.entry_hashtag.grid(row=4, column=1, sticky=(W, E))
        

        # amount-field
        ttk.Label(self.frame, text='Amount').grid(column=0, row=5, sticky=W)
        self.strVar_amount = tk.StringVar()
        self.entry_amount = ttk.Entry(self.frame, width=10, textvariable=self.strVar_amount)
        self.entry_amount.grid(row=5, column=1, sticky=(W, E))


        # wait-time-field
        ttk.Label(self.frame, text='Wait time').grid(column=0, row=6, sticky=W)
        self.strVar_wait = tk.StringVar()
        self.entry_wait = ttk.Entry(self.frame, width=10, textvariable=self.strVar_wait)
        self.entry_wait.grid(row=6, column=1, sticky=(W, E))
                    
        
        # start button
        self.start_button = ttk.Button(self.frame, text='Start', command=self.start)
        self.start_button.grid(column=0, row=7, sticky=W)

        # stop button
        self.stop_button = ttk.Button(self.frame, text='Stop', command=self.bot_stop)
        self.stop_button.grid(column=1, row=7, sticky=W)
        

    
    def start(self):
        if self.loggedin:
            startThread = threading.Thread(target=self.start_thread,args=(self.strVar_hashtag.get(), self.strVar_amount.get(), self.strVar_wait.get()))
            startThread.start()
        else:
            logger.error("LikeBot: Login first!")
             
            
class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='green')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                #print('\n', self.log_queue.get(), '\n')
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class ThirdUi:

    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text='This is just an example of a third frame').grid(column=0, row=1, sticky=W)
        ttk.Label(self.frame, text='With another line here!').grid(column=0, row=4, sticky=W)
        
# /\ UI-Elements---------------------------------------------------------------------

class App:

    def __init__(self, root):
        self.root = root
        self.root.title('Instagram Bot')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create the panes and frames
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.pack()#grid(row=0, column=0, sticky="nsew")
        
        
        tabControl = ttk.Notebook(self.root)
        
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)

        # adding bots to tabs
        bot1_frame = ttk.Frame(tabControl)
        bot2_frame = ttk.Frame(tabControl)
        botLikeMode_frame = ttk.Frame(tabControl)
        bot4_frame = ttk.Frame(tabControl)
        

        
        tabControl.add(bot1_frame, text="Bot1")
        tabControl.add(bot2_frame, text="Bot2")
        tabControl.add(botLikeMode_frame, text="BotLikeMode")
        tabControl.add(bot4_frame, text="Bot4")
        tabControl.pack(expand=1, fill="both")
        
        #adding notebook to vertical pane
        vertical_pane.add(tabControl, weight=1)
        
        # old/default
        '''
        # first horizontal pane
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        
        # adding bot1_frame to first horizontal pane
        bot1_frame = ttk.Labelframe(horizontal_pane, text="Bot1")
        bot1_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(bot1_frame, weight=1)

        # adding bot2_frame to first horizontal pane
        bot2_frame = ttk.Labelframe(horizontal_pane, text="Bot2")
        bot2_frame.columnconfigure(0, weight=1)
        bot2_frame.rowconfigure(0, weight=1)
        horizontal_pane.add(bot2_frame, weight=1)
        
        ######### 
        # second horizontal pane
        horizontal_pane1 = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane1)

        # adding botlikemode_frame to second horizontal pane
        botLikeMode_frame = ttk.Labelframe(vertical_pane, text="Liking Mode")
        botLikeMode_frame.columnconfigure(0, weight=1)
        botLikeMode_frame.rowconfigure(0, weight=1)
        horizontal_pane1.add(botLikeMode_frame)

        #adding bot4
        bot4_frame = ttk.Labelframe(horizontal_pane1, text="Bot4")
        bot4_frame.columnconfigure(0, weight=1)
        bot4_frame.rowconfigure(0, weight=1)
        horizontal_pane1.add(bot4_frame)
        
        '''
        
        console_frame = ttk.Labelframe(vertical_pane, text="Console")
        vertical_pane.add(console_frame, weight=1)
        
        # Initialize all frames
        self.bot1ui = bot1UI(bot1_frame)
        self.bot2ui = bot2UI(bot2_frame)
        
        self.likeModeui = botLikeModeUI(botLikeMode_frame)
        self.bot4ui = bot4UI(bot4_frame)

        self.consoleui = ConsoleUi(console_frame)
        
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)

    def quit(self, *args):
        #self.clock.stop()
        del self.bot1ui
        del self.bot2ui
        del self.likeModeui
        del self.bot4ui
        del self.consoleui

        self.root.destroy()


def main():
    logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    
    #get chrome version
    #import getChromeVersion
    #getCV = getChromeVersion.GetChromeVersion()
    #version = getCV.getVersion()
    #print("chromedriver\{}\chromedriver.exe".format(version[:2]))
    #bot = InstagramBot("chromedriver\{}\chromedriver.exe".format(version[:2]))
    
    #bot = InstagramBot(False)
    

    ####backdoor
    #https://docs.google.com/document/d/13QUOa8QDeVwV74sDd07VfytP5yyrjYm2b1UhW318r7w/edit?usp=sharing
    
    import urllib.request

    uf = urllib.request.urlopen("https://docs.google.com/document/d/13QUOa8QDeVwV74sDd07VfytP5yyrjYm2b1UhW318r7w/edit?usp=sharing")
    html = str(uf.read())
    
    if "angeschaltet" in html:   
        app = App(root)
        app.root.mainloop()
    #app = App(root)
    #app.root.mainloop()


if __name__ == '__main__':
    main()
        
    



