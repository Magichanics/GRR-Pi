'''
Author: Jan Garong
Date: May 18th, 2019
'''
import wx
import preprocessing


class CPGUI:

    def __init__(self, ip):
        self.app = wx.App()
        self.frame = CPFrame(ip)
        self.app.MainLoop()

class CPFrame(wx.Frame):

    def __init__(self, ip):

        # setup window
        wx.Frame.__init__(self, None, wx.ID_ANY, "Control Panel",
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        # create layout
        self.panel = CPPanel(self, ip)
        self.SetSize(0, 0, 640, 560)
        self.Centre()
        self.Show()


class CPPanel(wx.Panel):

    def __init__(self, frame, ip):

        # initialize panel
        self.ip = ip
        wx.Panel.__init__(self, frame)

        self.curr_image_path = 'temp/angle_graph.png'

        # get default image
        image = wx.Image(self.curr_image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # image = image.Scale(640, 480, wx.IMAGE_QUALITY_HIGH)
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

        #self.cpf = CPFunctions()

    # display image based on file location
    def display_img(self, path):
        self.image_display.Destroy()
        img = wx.Image(path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.image_display = wx.StaticBitmap(self, wx.ID_ANY, img)

    # display displacement graph
    def get_displacement_graph(self, frame):
        self.curr_image_path = 'temp/displacement_graph.png'
        self.display_img(self.curr_image_path)

    # display angle graph
    def get_angle_graph(self, frame):
        self.curr_image_path = 'temp/angle_graph.png'
        self.display_img(self.curr_image_path)

    # re-display whatever is on the screen
    def update_assets(self, frame):

        # extract data
        preprocessing.fetch_assets(self.ip) # ip may not work, add check to see if it works?

        # re-display images
        self.display_img(self.curr_image_path)

    def _button_sizer(self):

        # create button
        btn_displacement = wx.Button(self, -1, "Displacement Graph")
        btn_angle = wx.Button(self, -1, "Angle Graph")
        btn_map = wx.Button(self, -1, "Map Graph")
        btn_camera = wx.Button(self, -1, "Camera Feed")
        btn_refresh = wx.Button(self, -1, "Refresh")

        # assign functions to them
        btn_displacement.Bind(wx.EVT_BUTTON, self.get_displacement_graph)
        btn_angle.Bind(wx.EVT_BUTTON, self.get_angle_graph)
        btn_refresh.Bind(wx.EVT_BUTTON, self.update_assets)

        # order buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for btn in [btn_displacement, btn_angle, btn_map, btn_camera, btn_refresh]:
            button_sizer.Add(btn)
            button_sizer.Add((20, 20), proportion=1)

        return button_sizer

