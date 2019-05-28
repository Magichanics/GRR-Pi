'''
Author: Jan Garong
Date: May 20th, 2019
'''

import wx
import os
import shutil
from PIL import Image


class SettingsGUI(wx.Frame):

    def __init__(self):

        # setup window
        wx.Frame.__init__(self, None, wx.ID_ANY, "Control Panel Settings",
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        # create layout
        self.panel = SettingsPanel(self)
        self.SetSize(0, 0, 480, 140)
        self.Centre()
        self.Layout()
        self.Show()

        # check if it's going to close
        self.instance = wx.SingleInstanceChecker("SingleApp-%s" % wx.GetUserId())
        self.Bind(wx.EVT_CLOSE, self.frame_on_close)

    def frame_on_close(self, event):
        self.Hide()


class SettingsPanel(wx.Panel):

    def __init__(self, frame):

        wx.Panel.__init__(self, frame)

        # setup vertical box
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # create panels
        self.ip_row = self._ip_sizer()
        self.buttons_box = self._button_sizer()

        # create layout
        self.vbox.AddSpacer(20)
        self.vbox.Add(self.ip_row)
        self.vbox.AddSpacer(20)
        self.vbox.Add(self.buttons_box)

        # size boxes to fix
        self.SetSizer(self.vbox)
        self.Fit()

    def _ip_sizer(self):

        # create ip box components
        ip_row = wx.BoxSizer(wx.HORIZONTAL)
        lbl_ip = wx.StaticText(self, label="Robot\'s IP Address: ")
        self.ip_box = wx.TextCtrl(self, size=(200, 25))

        # add to box
        ip_row.Add((10, 10), proportion=1)
        ip_row.Add(lbl_ip)
        ip_row.Add((10, 10), proportion=1)
        ip_row.Add(self.ip_box)

        return ip_row

    def _button_sizer(self):

        # create buttons
        btn_manual = wx.Button(self, -1, "User Manual")
        btn_credits = wx.Button(self, -1, "Credits")
        btn_clear = wx.Button(self, -1, "Clear")

        btn_clear.Bind(wx.EVT_BUTTON, self.clear_files)

        # add to panel
        buttons_row = wx.BoxSizer(wx.HORIZONTAL)
        buttons_row.Add((50, 50), proportion=1)
        buttons_row.Add(btn_manual)
        buttons_row.Add((50, 50), proportion=1)
        buttons_row.Add(btn_credits)
        buttons_row.Add((50, 50), proportion=1)
        buttons_row.Add(btn_clear)

        return buttons_row

    # create new placeholder
    def placeholder_asset(self, path):
        img = Image.new('RGB', (640, 480), (0, 0, 0))
        img.save(path, "PNG")

    def clear_files(self, frame, path='temp/'):

        # unlink files in folder
        for file in os.listdir(path):
            file_path = os.path.join(path, file)  # get file path

            # remove file
            if os.path.isfile(file_path):
                os.unlink(file_path)

            # remove directory
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        # create placeholder
        self.placeholder_asset('temp/placeholder.png')

