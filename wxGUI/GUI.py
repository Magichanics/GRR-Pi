'''
Author: Jan Garong
Date: May 18th, 2019
'''
import wx
import pandas as pd
from PIL import Image
import PIL
# from wxGUI.SettingsGUI import SettingsGUI


class CPGUI:

    def __init__(self):
        self.app = wx.App()
        self.frame = CPFrame()
        self.app.MainLoop()


class CPFrame(wx.Frame):

    def __init__(self):

        # setup window
        wx.Frame.__init__(self, None, wx.ID_ANY, "Control Panel",
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        # create layout
        self.panel = CPPanel(self)
        self.SetSize(0, 0, 640, 560)
        self.Centre()
        self.Layout()
        self.Show()

    #     self.Bind(wx.EVT_CLOSE, self.FrameOnClose)
    #
    # def FrameOnClose(self, event):
    #     #self.DestroyChildren()
    #     self.Destroy()

class CPPanel(wx.Panel):

    def __init__(self, frame):

        # initialize panel
        self.ip = '192.168.2.101'
        wx.Panel.__init__(self, frame)
        self.curr_image_path = 'temp/angle_graph.png'

        # create settings GUI
        # self.sgui = SettingsGUI()
        # self.sgui.Hide()

        # get default image
        image = wx.Image(self.curr_image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.image_display = wx.StaticBitmap(self, wx.ID_ANY, image)

        # create row of buttons
        button_sizer = self._button_sizer()

        # add components to vertical box
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.image_display, proportion=1, flag=wx.ALIGN_CENTER)
        self.vbox.AddSpacer(15)
        self.vbox.Add(button_sizer, proportion=1, flag=wx.ALIGN_CENTER)

        self.SetSizer(self.vbox)
        self.Fit()

        # create placeholder
        self.placeholder_asset('temp/placeholder.png')

        # self.cpf = CPFunctions()
        # self.Bind(wx.EVT_CLOSE, self.FrameOnClose)

    # fix please
    # def FrameOnClose(self, event):
    #     self.DestroyChildren()

    # display image based on file location
    def display_img(self, path, pic_path='temp/pic_gui.png'):
        try:

            # resize image
            self.resize_for_GUI(path, pic_path)

            # replace image
            self.image_display.Destroy()
            img = wx.Image(pic_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.image_display = wx.StaticBitmap(self, wx.ID_ANY, img)

        # display placeholder (black image)
        except FileNotFoundError:
            self.curr_image_path = 'temp/placeholder.png'
            img = wx.Image('temp/placeholder.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.image_display = wx.StaticBitmap(self, wx.ID_ANY, img)

    # display displacement graph
    def get_displacement_graph(self, frame):
        self.curr_image_path = 'temp/displacement_graph.png'
        self.display_img(self.curr_image_path)

    # display angle graph
    def get_angle_graph(self, frame):
        self.curr_image_path = 'temp/angle_graph.png'
        self.display_img(self.curr_image_path)

    # display map
    def get_map(self, frame):
        self.curr_image_path = 'temp/picmap.png'
        self.display_img(self.curr_image_path)

    def get_camera_feed(self, frame):

        try:

            # get last predicted image
            cl_df = pd.read_csv('temp/camera_log.csv')
            display_img_path = 'temp/y_' + cl_df['img_name'].iloc[len(cl_df) - 1]
            self.resize_for_GUI(display_img_path, 'temp/y_camera_gui.png')
            self.curr_image_path = 'temp/y_camera_gui.png'

            # display image
            self.display_img('temp/y_camera_gui.png')

        except IndexError:
            # show error message
            error_msg = wx.MessageDialog(None, message='Robot has not taken any pictures. Please let it'
                                                       ' run for a few more seconds.',
                                         caption='Error')

            error_msg.ShowModal()
            error_msg.Destroy()

            # img = wx.Image('temp/placeholder.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            # self.curr_image_path = 'temp/placeholder.png'
            # self.image_display = wx.StaticBitmap(self, wx.ID_ANY, img)

    # from CPFunctions
    def resize_for_GUI(self, open_path, save_path, size=480):

        # read image
        img = Image.open(open_path).convert("RGBA")

        # resize image using ratio
        size_ratio = size / img.size[1]
        img = img.resize((int(img.size[0] * size_ratio), int(img.size[1] * size_ratio)), PIL.Image.ANTIALIAS)

        # save image
        img.save(save_path)

    # re-display whatever is on the screen
    def update_assets(self, frame):

        # having this import statement above destroys the GUI
        import preprocessing

        try:
            # extract data
            preprocessing.fetch_assets(self.ip) # ip may not work, add check to see if it works?

            # re-display images
            self.display_img(self.curr_image_path)

        except FileNotFoundError:

            # show error message
            error_msg = wx.MessageDialog(None, message='Cannot retrieve robot data. Check the Robot\'s IP '
                                                       'address or run the robot first.',
                                         caption='Error')

            error_msg.ShowModal()
            error_msg.Destroy()

    # create black 640 x 480
    def placeholder_asset(self, path):
        img = Image.new('RGB', (640, 480), (0, 0, 0))
        img.save(path, "PNG")

    # # open Settings GUI
    # def get_settings(self, frame):
    #
    #     if self.sgui.instance.IsAnotherRunning():
    #         return
    #
    #     # open new window
    #     #self.sgui = SettingsGUI()
    #     self.sgui.Show()

    def _button_sizer(self):

        # create button
        btn_displacement = wx.Button(self, -1, "Displacement Graph")
        btn_angle = wx.Button(self, -1, "Angle Graph")
        btn_map = wx.Button(self, -1, "Map Graph")
        btn_camera = wx.Button(self, -1, "Camera Feed")
        btn_refresh = wx.Button(self, -1, "Refresh")
        # btn_settings = wx.Button(self, -1, "Settings")

        # assign functions to them
        btn_displacement.Bind(wx.EVT_BUTTON, self.get_displacement_graph)
        btn_angle.Bind(wx.EVT_BUTTON, self.get_angle_graph)
        btn_map.Bind(wx.EVT_BUTTON, self.get_map)
        btn_camera.Bind(wx.EVT_BUTTON, self.get_camera_feed)
        btn_refresh.Bind(wx.EVT_BUTTON, self.update_assets)
        # btn_settings.Bind(wx.EVT_BUTTON, self.get_settings)

        # order buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for btn in [btn_displacement, btn_angle, btn_map, btn_camera, btn_refresh]:
            button_sizer.Add(btn)
            button_sizer.Add((5, 5), proportion=1)

        return button_sizer

