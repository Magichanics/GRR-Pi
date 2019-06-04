'''
Author: Jan Garong
May 5th, 2019
'''
from mappingtools.Mapping import Mapping
from preprocessing.VisualizationFunctions import VisualizationFunctions
from preprocessing.SSDKeras import SDDNeuralNetwork512
import pandas as pd
from keras.preprocessing import image
import os
import zipfile
import cv2
from PIL import Image, ImageDraw
import shutil


class CPFunctions(VisualizationFunctions):

    def clear_files(self, path='temp/'):

        # unlink files in folder
        for file in os.listdir(path):
            file_path = os.path.join(path, file)  # get file path

            # remove file
            if os.path.isfile(file_path):
                os.unlink(file_path)

            # remove directory
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def collect_data(self, ip_address, data_path='~/data.zip', # must end with data.zip
                     save_path='temp/'):

        # read from pi robot using commandline and scp
        os.system('scp pi@' + ip_address + ':' + data_path + ' '
                  + save_path)

        # unzip
        with zipfile.ZipFile("temp/data.zip", "r") as zip_ref:
            zip_ref.extractall(save_path)

        # delete data zip file
        os.remove(save_path + 'data.zip')

    def bounding_box(self, img_path, class_id, xmin, ymin, xmax, ymax):

        # load image
        img = Image.open(img_path).convert("RGBA")

        # determine the color
        draw = ImageDraw.Draw(img)
        draw.rectangle(((xmin, ymin), (xmax, ymax)), outline=self.color_tuples[int(class_id)])

        # save image
        img.save(img_path, "PNG")

    def predict_camera_data(self, path='temp/'): # all items will be stored in temp folder

        # get raw dataframe
        cl_df = pd.read_csv(path + 'camera_log.csv')

        # predict the contents within the file
        for i in range(self.start, len(cl_df)):

            # read image to array
            img = cv2.imread(path + cl_df['img_name'].iloc[i])
            img_pil = Image.open(path + cl_df['img_name'].iloc[i]).convert("RGBA")
            img_array = image.img_to_array(img)

            # get prediction dataframe
            pred_df = self.nn.predict(img_array, confidence_threshold=0.8)

            # copy image for predictions
            img_pil.save(path + 'y_' + cl_df['img_name'].iloc[i], "PNG")

            # create bounding boxes on top of the image per object
            for j in range(len(pred_df)):

                # get location
                curr_pred_df = pred_df.iloc[j]

                # create image with bounds
                self.bounding_box(path + 'y_' + cl_df['img_name'].iloc[i],
                                  curr_pred_df['class_id'],
                             curr_pred_df['xmin'], curr_pred_df['ymin'],
                             curr_pred_df['xmax'], curr_pred_df['ymax'])

            # groupby objects, create series and dataframe
            pred_s = pred_df.groupby('class_id').count()['confidence']  # can be any column for []
            pred_df2 = pred_s.copy().to_frame()
            pred_df2.reset_index(inplace=True)

            # iterate through number of unique class_ids
            for f in pred_df2['class_id'].unique():

                # get real class name
                class_name = self.nn.classes[int(f)]

                # check if column exist
                if not class_name in cl_df.columns:
                    cl_df[class_name] = 0

                cl_df[class_name].iloc[i] = pred_s.loc[int(f)]

            # set new starting point
            self.start = i + 1

        # save dataframe
        cl_df.to_csv(path + 'predictions.csv')

    def get_map(self, path='temp/'):

        # read mppy file
        map_obj = Mapping()
        map_obj.read_mppy(path+'map.txt')

        # export to png
        map_obj.to_img(path+'picmap.png')

    def fetch_data(self, ip):

        # extract data
        print('loading robot files...')
        self.collect_data(ip)

        # save files
        print('processing data...')
        self.predict_camera_data()
        print('creating maps...')
        self.get_map()
        print('creating graphs...')
        self.graph_items()

    # initialize neural network
    def __init__(self):

        # inherit visualizations
        VisualizationFunctions.__init__(self)

        # assign weights and neural network
        self.nn = SDDNeuralNetwork512(weights_path='VGG_VOC0712_SSD_512x512_iter_120000.h5')

        # create color tuple list
        self.color_tuples = []
        rgb_values = [100, 150, 200]
        for i_item in rgb_values:
            for j_item in rgb_values:
                for k_item in rgb_values:
                    self.color_tuples.append((i_item, j_item, k_item))
        self.color_tuples = self.color_tuples[:len(self.nn.classes)]

        # create new starting point
        self.start = 0

        # create temporary directory
        if not os.path.exists('temp'):
            os.makedirs('temp')


