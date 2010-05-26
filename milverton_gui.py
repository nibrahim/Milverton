#!/usr/bin/env python

import wx

class Milverton(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=True)

    def OnInit(self):
        frame = wx.Frame(None, -1, "Milverton Proxy",
                         pos=(50,50), size=(400,200),
                         style=wx.DEFAULT_FRAME_STYLE,
                         name="Milverton proxy control console")
        frame.CreateStatusBar()

        menu = wx.Menu()
        menu.Append(101, "E&xit", "Exit")
        menubar = wx.MenuBar()
        menubar.Append(menu, "&File")

        frame.SetMenuBar(menubar)
        frame.Show(True)

        self.SetTopWindow(frame)

        self.frame = frame
        return True


    def OnExitApp(self, evt):
        self.frame.Close(True)


    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
            self.window.ShutdownDemo()
        evt.Skip()



if __name__ == "__main__":
    app = Milverton()
    app.MainLoop()
