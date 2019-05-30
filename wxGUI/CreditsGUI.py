'''
Author: Jan Garong
Date: May 30th, 2019
'''

import wx


class CreditsGUI(wx.Frame):

    def __init__(self):

        # setup window
        wx.Frame.__init__(self, None, wx.ID_ANY, "Credits",
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        # create layout
        self.panel = CreditsPanel(self)
        self.SetSize(0, 0, 300, 160)
        self.Centre()
        self.Layout()
        self.Show()

        # check if it's going to close
        self.instance = wx.SingleInstanceChecker("SingleApp-%s" % wx.GetUserId())
        self.Bind(wx.EVT_CLOSE, self.frame_on_close)

    def frame_on_close(self, event):
        self.Hide()


class CreditsPanel(wx.Panel):

    def __init__(self, frame):
        wx.Panel.__init__(self, frame)

        # create credits
        str_credits = "Developed by:\nJan Garong and Matteo Tempo\n\nssd_keras created by " \
                      "Pierluigi Ferrari\nShortest Path Algorithm by Nicholas Swift" \
                      "\nExample code by waveshare and electronicwings"
        self.credits = wx.StaticText(self, -1, label=str_credits, style=wx.ALIGN_CENTRE_HORIZONTAL)