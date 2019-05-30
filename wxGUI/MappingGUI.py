'''
Author: Jan Garong
Thursday May 28th, 2019
'''

from mappingtools.Mapping import Mapping
from mappingtools import PathFinding as pf
import wx


class MappingGUI(wx.Frame):

    def __init__(self):

        # setup window
        wx.Frame.__init__(self, None, wx.ID_ANY, "Mapping Settings",
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        # create layout
        self.panel = SettingsPanel(self)
        self.SetSize(0, 0, 360, 160)
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
        self.sp_col = self._shortpath_sizer()
        self.buttons_box = self._button_sizer()

        # create layout
        self.vbox.AddSpacer(20)
        self.vbox.Add(self.sp_col)
        self.vbox.AddSpacer(20)
        self.vbox.Add(self.buttons_box)

        # size boxes to fix
        self.SetSizer(self.vbox)
        self.Fit()

    def _shortpath_sizer(self):

        # create ip box components
        startpath_row = wx.BoxSizer(wx.HORIZONTAL)
        endpath_row = wx.BoxSizer(wx.HORIZONTAL)
        lbl_startloc = wx.StaticText(self, label="Starting Location")
        self.start_loc = wx.TextCtrl(self, size=(200, 25))
        lbl_endloc = wx.StaticText(self, label="Ending Location")
        self.end_loc = wx.TextCtrl(self, size=(200, 25))

        # add to box
        startpath_row.Add((10, 10), proportion=1)
        startpath_row.Add(lbl_startloc)
        startpath_row.Add((10, 10), proportion=1)
        startpath_row.Add(self.start_loc)

        # add to box
        endpath_row.Add((10, 10), proportion=1)
        endpath_row.Add(lbl_endloc)
        endpath_row.Add((10, 10), proportion=1)
        endpath_row.Add(self.end_loc)

        # add components to box
        shortpath_col = wx.BoxSizer(wx.VERTICAL)
        shortpath_col.Add(startpath_row)
        shortpath_col.AddSpacer(20)
        shortpath_col.Add(endpath_row)

        return shortpath_col

    def _button_sizer(self):

        # create buttons
        btn_path = wx.Button(self, -1, "Display Path")
        btn_path.Bind(wx.EVT_BUTTON, self.plot_graph)

        # add to panel
        buttons_row = wx.BoxSizer(wx.HORIZONTAL)
        buttons_row.Add((100, 100), proportion=1)
        buttons_row.Add(btn_path)
        buttons_row.Add((100, 100), proportion=1)

        return buttons_row

    # p1 and p2 are tuple coordinates (x, y)
    def plot_graph(self, frame):

        def format_error():

            # show error message
            error_msg = wx.MessageDialog(None, message='Please format coordinates like this: (x, y)',
                                         caption='Error')

            error_msg.ShowModal()
            error_msg.Destroy()

        try:

            def parse_coords(str_item):
                str_lst = str_item.replace('(', '').replace(')', '').replace(',', '').split(' ')
                return int(str_lst[0]), int(str_lst[1])

            # parse to integer
            self.p1 = parse_coords(self.start_loc.GetLineText(0))
            self.p2 = parse_coords(self.end_loc.GetLineText(0))

            # check if they are the same
            if self.p1 == self.p2:
                # show error message
                error_msg = wx.MessageDialog(None, message='Do not write the same coordinate.',
                                             caption='Error')

                error_msg.ShowModal()
                error_msg.Destroy()
                return

            # convert coordinates to indices.
            mp = Mapping()
            mp.read_mppy('temp/map.txt')
            pi, pj = mp.get_index(self.p1)
            li, lj = mp.get_index(self.p2)

            # convert coordinates to indices (reversed coords)
            pf.main((pi, pj), (li, lj), save_path='temp/map_path.png')

            # show success message
            error_msg = wx.MessageDialog(None, message='Created a new path! See Mapping Tab.',
                                         caption='Success')

            error_msg.ShowModal()
            error_msg.Destroy()


        # no map
        except FileNotFoundError:

            # show error message
            error_msg = wx.MessageDialog(None, message='There is no map available.',
                                         caption='Error')

            error_msg.ShowModal()
            error_msg.Destroy()

        # out of bounds
        except TypeError:

            # show error message
            error_msg = wx.MessageDialog(None, message='Make sure coordinates are on '
                                                       'green/yellow/black squares.',
                                         caption='Error')

            error_msg.ShowModal()
            error_msg.Destroy()

        # incorrect format
        except ValueError:
            format_error()

        except IndexError:
            format_error()

