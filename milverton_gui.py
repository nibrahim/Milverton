#!/usr/bin/env python
import wx

class MilvertonFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MilvertonFrame,self).__init__(self, parent, title = title, size= (300, 200))
        

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()
