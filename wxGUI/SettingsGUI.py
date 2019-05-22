'''
Author: Jan Garong
Date: May 20th, 2019
'''

# import wx
#
# class SettingsGUI(wx.Frame):
#
#     def __init__(self):
#
#         # setup window
#         wx.Frame.__init__(self, None, wx.ID_ANY, "Control Panel Settings",
#                           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
#
#         # create layout
#         self.SetSize(0, 0, 480, 360)
#         self.Centre()
#         self.Layout()
#         self.Show()
#
#         self.instance = wx.SingleInstanceChecker("SingleApp-%s" % wx.GetUserId())
#         self.Bind(wx.EVT_CLOSE, self.FrameOnClose)
#
#     def FrameOnClose(self, event):
#
#         self.Hide()