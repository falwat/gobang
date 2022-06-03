"""
Base Mainwindos class that contain menubar, toolbar, statusbar and mainframe.

Copyright (c) 2022 falwat, under MIT License.
"""
from tkinter import *
from tkinter import ttk

class Mainwindow(ttk.Frame):
    def __init__(self, master : Tk, **kw):
        super().__init__(master, **kw)

        # tool bar
        self.toolbar = ttk.Frame(self, padding='3 3 3 3')
        # mainframe. 
        # all widget need to add to mainframe, 
        # except menubar item, toolbar item and statusbar item
        self.mainframe = ttk.Frame(self, padding='3 3 3 3')
        # status bar
        self.statusbar = ttk.Frame(self, padding='3 3 3 0')

        self.toolbar.grid(column=0, row=0, sticky=NSEW)
        self.mainframe.grid(column=0, row=1, sticky=NSEW)
        self.statusbar.grid(column=0, row=2, sticky=NSEW)
        self.grid(column=0, row=0, sticky=NSEW)

        self.master.option_add('*tearOff', FALSE)
        # Create Menubar
        win = self.winfo_toplevel()
        self.menubar = Menu(win)
        win['menu'] = self.menubar

        self.statusmsg = StringVar()
        self.statusLabel = Label(self.statusbar, textvariable=self.statusmsg)
        self.statusLabel.grid(column=0, row=0, sticky=SW)

        self.toolbar.rowconfigure(0, weight=1)
        self.statusbar.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
    
    def showmessage(self, msg : str):
        self.statusmsg.set(msg)

