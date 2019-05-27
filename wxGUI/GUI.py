'''
Author: Jan Garong
Date: May 18th, 2019
'''
import wx
import pandas as pd
from PIL import Image
import PIL
from wxGUI.SettingsGUI import SettingsGUI


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
        self.SetSize(0, 0, 880, 560) # 0,0,640,560
        self.Centre()
        self.Layout()
        self.Show()

        self.Bind(wx.EVT_CLOSE, self.frame_on_close)

    def frame_on_close(self, event):
        self.panel.sgui.Destroy()
        self.Destroy()
        print('Terminating GUI')

class CPPanel(wx.Panel):

    def __init__(self, frame):

        # initialize panel
        self.ip = ''
        wx.Panel.__init__(self, frame)
        self.curr_image_path = 'temp/angle_graph.png'

        # create settings GUI
        self.sgui = SettingsGUI()
        self.sgui.Hide()

        # get default image
        #self.display_img(self.curr_image_path)
        image = wx.Image(self.curr_image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.image_display = wx.StaticBitmap(self, wx.ID_ANY, image, wx.Point(0,0))

        # create row of buttons
        button_sizer = self._button_sizer()

        # add components to vertical box
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # create horizontal box for image, then properties + panels
        self.img_row = wx.BoxSizer(wx.HORIZONTAL)

        # do placements in horizontal box
        self.img_row.Add(self.image_display)
        self.img_row.Add((5, 5), proportion=1)
        self.img_row.Add(self._img_panel())

        self.vbox.Add(self.img_row, proportion=1, flag=wx.ALIGN_CENTER)
        self.vbox.AddSpacer(15)
        self.vbox.Add(button_sizer, proportion=1, flag=wx.ALIGN_CENTER)

        self.SetSizer(self.vbox)
        self.Fit()

        # create placeholder
        self.placeholder_asset('temp/placeholder.png')

        # read dataframe
        try:
            self.cl_df = pd.read_csv('temp/predictions.csv')

        # if there are no csv found
        except FileNotFoundError:
            self.cl_df = pd.DataFrame(columns=['img_name', 'x', 'y', 'seconds', 'angle'])

        # set properties
        self.img_index = len(self.cl_df) - 1
        self.on_camera_tab = False

        self.Bind(wx.EVT_CLOSE, self.frame_on_close)

    # fix please
    def frame_on_close(self, event):
        self.DestroyChildren()

    # display image based on file location
    def display_img(self, path, pic_path='temp/pic_gui.png', is_camera=False):

        # for checking whether it is on tab or not
        if is_camera:
            self.on_camera_tab = True
        else:

            # clear previous information
            self.textbox.SetValue("")
            self.on_camera_tab = False

        try:

            # resize image
            self.resize_for_gui(path, pic_path)

            # replace image
            self.image_display.Destroy()
            img = wx.Image(pic_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.image_display = wx.StaticBitmap(self, wx.ID_ANY, img)

        # display placeholder (black image)
        except FileNotFoundError:
            self.curr_image_path = 'temp/placeholder.png'
            img = wx.Image('temp/placeholder.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.image_display = wx.StaticBitmap(self, wx.ID_ANY, img)

    def _img_panel(self):

        img_vbox = wx.BoxSizer(wx.VERTICAL)

        # create buttons for LR controls
        img_controls = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_left = wx.Button(self, -1, "<")
        self.btn_right = wx.Button(self, -1, ">")

        # bind to function
        self.btn_left.Bind(wx.EVT_BUTTON, self.scroll_left)
        self.btn_right.Bind(wx.EVT_BUTTON, self.scroll_right)

        # place in box
        img_controls.Add((10, 10), proportion=1)
        img_controls.Add(self.btn_left)
        img_controls.Add((5, 5), proportion=1)
        img_controls.Add(self.btn_right)

        # create textbox
        self.textbox = wx.TextCtrl(self, size=(200, 400), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Display stats boxes of images
        img_vbox.AddSpacer(15)
        img_vbox.Add(img_controls)
        img_vbox.AddSpacer(30)
        img_vbox.Add(self.textbox)

        # shift it to the right by a tiny bit
        img_hbox = wx.BoxSizer(wx.HORIZONTAL)
        img_hbox.Add((10, 10), proportion=1)
        img_hbox.Add(img_vbox)

        return img_hbox

    def camera_img_update(self):

        # get filename
        display_img_path = 'temp/y_' + self.cl_df['img_name'].iloc[self.img_index]

        # get image path
        self.resize_for_gui(display_img_path, 'temp/y_camera_gui.png')
        self.curr_image_path = 'temp/y_camera_gui.png'

        # display img
        self.display_img(self.curr_image_path,is_camera=True)

    def display_metadata(self):

        # clear previous information
        self.textbox.SetValue("")

        # put information into \n'd string
        output = ''
        for f in self.cl_df.columns[2:]:

            # get corresponding value to attribute
            value = self.cl_df[f].iloc[self.img_index]

            # check if its not a prediction = 0
            if f in ['img_name', 'x', 'y', 'seconds', 'angle'] or value != 0:

                # add to output
                output += f + ': ' + str(self.cl_df[f].iloc[self.img_index]) + '\n'

        # display information in textbox
        self.textbox.AppendText(output)

    def scroll_left(self, frame):

        # check if it reaches the end of the album + if it's on the camera tab
        if self.on_camera_tab and self.img_index - 1 >= 0:
            self.img_index -= 1
            self.camera_img_update()
            self.display_metadata()

    def scroll_right(self, frame):

        # check if it reaches the end of the album + if it's on the camera tab
        if self.on_camera_tab and self.img_index + 1 <= len(self.cl_df) - 1:
            self.img_index += 1
            self.camera_img_update()
            self.display_metadata()

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

            # set properties
            self.img_index = len(self.cl_df) - 1
            self.on_camera_tab = True

            # display the given information
            self.camera_img_update()
            self.display_metadata()

            # display image
            self.display_img('temp/y_camera_gui.png', is_camera=True)

        except IndexError:

            # show error message
            error_msg = wx.MessageDialog(None, message='Robot has not taken any pictures. Please let it'
                                                       ' run for a few more seconds.',
                                         caption='Error')
            error_msg.ShowModal()
            error_msg.Destroy()

    # from CPFunctions
    def resize_for_gui(self, open_path, save_path, size=480):

        # read image
        img = Image.open(open_path).convert("RGBA")

        # resize image using ratio
        size_ratio = size / img.size[1]
        img = img.resize((int(img.size[0] * size_ratio), int(img.size[1] * size_ratio)), PIL.Image.ANTIALIAS)

        # save image
        img.save(save_path)

    # re-display whatever is on the screen
    def update_assets(self, frame):

        # check if empty
        if self.sgui.panel.ip_box.GetLineText(0) == '':

            # show error message
            error_msg = wx.MessageDialog(None, message='Please enter the Robot\'s IP Address in Settings.',
                                         caption='Error')
            error_msg.ShowModal()
            error_msg.Destroy()

            return

        # get ip address
        self.ip = self.sgui.panel.ip_box.GetLineText(0)
        print(self.ip)

        # having this import statement above destroys the GUI
        import preprocessing

        try:
            # extract data
            preprocessing.fetch_assets(self.ip)  # ip may not work, add check to see if it works?

            # re-display images
            self.display_img(self.curr_image_path)

            # update camera dataframe
            self.cl_df = pd.read_csv('temp/predictions.csv')

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

    # open Settings GUI
    def get_settings(self, frame):

        if self.sgui.instance.IsAnotherRunning():
            return

        # open new window
        #self.sgui = SettingsGUI()
        self.sgui.Show()

    def _button_sizer(self):

        # create buttons
        btn_displacement = wx.Button(self, -1, "Displacement Graph")
        btn_angle = wx.Button(self, -1, "Angle Graph")
        btn_map = wx.Button(self, -1, "Map Graph")
        btn_camera = wx.Button(self, -1, "Camera Feed")
        btn_refresh = wx.Button(self, -1, "Refresh")
        btn_settings = wx.Button(self, -1, "Settings")

        # assign functions to them
        btn_displacement.Bind(wx.EVT_BUTTON, self.get_displacement_graph)
        btn_angle.Bind(wx.EVT_BUTTON, self.get_angle_graph)
        btn_map.Bind(wx.EVT_BUTTON, self.get_map)
        btn_camera.Bind(wx.EVT_BUTTON, self.get_camera_feed)
        btn_refresh.Bind(wx.EVT_BUTTON, self.update_assets)
        btn_settings.Bind(wx.EVT_BUTTON, self.get_settings)

        # order buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for btn in [btn_displacement, btn_angle, btn_map, btn_camera, btn_refresh, btn_settings]:
            button_sizer.Add(btn)
            button_sizer.Add((30, 30), proportion=1)

        return button_sizer

