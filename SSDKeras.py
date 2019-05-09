'''
SSD Keras Neural Network by
@pierluigiferrari

Repository URL: https://github.com/pierluigiferrari/ssd_keras
Weight h5 URL: https://drive.google.com/file/d/19NIa0baRCFYT3iRxQkOKCD7CpN6BFO8p/view
(if it doesn't work, refer to the repo)

Dependencies:
    Python 3.x
    Numpy
    TensorFlow 1.x
    Keras 2.x
    imageio
    tqdm
    sklearn

'''
from keras import backend as K
from keras.models import load_model
from keras.optimizers import Adam
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from models.keras_ssd512 import ssd_512
from keras_loss_function.keras_ssd_loss import SSDLoss
from keras_layers.keras_layer_AnchorBoxes import AnchorBoxes
from keras_layers.keras_layer_DecodeDetections import DecodeDetections
from keras_layers.keras_layer_DecodeDetectionsFast import DecodeDetectionsFast
from keras_layers.keras_layer_L2Normalization import L2Normalization

class SDDNeuralNetwork512:

    # creates dataframe to label given y values
    def get_pred_csv(self, y_pred):
        return pd.DataFrame(y_pred, columns=['class_id', 'confidence', 'xmin', 'ymin',
                                       'xmax', 'ymax'])

    def predict(self, img, confidence_threshold=0.5):

        input_images = []  # Store resized versions of the images here.
        input_images.append(img)
        input_images = np.array(input_images)

        # predict this image
        y_pred = self.model.predict(input_images)

        # eliminate objects that fall under the confidence threshold
        y_pred_thresh = [y_pred[k][y_pred[k, :, 1] > confidence_threshold] for k in range(y_pred.shape[0])]
        #np.set_printoptions(precision=2, suppress=True, linewidth=90)
        y_pred = y_pred_thresh[0].tolist()

        # get dataset
        return self.get_pred_csv(y_pred)

    # setup neural network
    def __init__(self, weights_path='VGG_VOC0712_SSD_512x512_iter_120000.h5'): # assume weights are in the master folder.

        K.clear_session()  # Clear previous models from memory.

        # load parameters
        self.model = ssd_512(image_size=(512, 512, 3), # 512x512
                        n_classes=20,
                        mode='inference',
                        l2_regularization=0.0005,
                        scales=[0.07, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05],
                        # The scales for MS COCO are [0.04, 0.1, 0.26, 0.42, 0.58, 0.74, 0.9, 1.06]
                        aspect_ratios_per_layer=[[1.0, 2.0, 0.5],
                                                 [1.0, 2.0, 0.5, 3.0, 1.0 / 3.0],
                                                 [1.0, 2.0, 0.5, 3.0, 1.0 / 3.0],
                                                 [1.0, 2.0, 0.5, 3.0, 1.0 / 3.0],
                                                 [1.0, 2.0, 0.5, 3.0, 1.0 / 3.0],
                                                 [1.0, 2.0, 0.5],
                                                 [1.0, 2.0, 0.5]],
                        two_boxes_for_ar1=True,
                        steps=[8, 16, 32, 64, 128, 256, 512],
                        offsets=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                        clip_boxes=False,
                        variances=[0.1, 0.1, 0.2, 0.2],
                        normalize_coords=True,
                        subtract_mean=[123, 117, 104],
                        swap_channels=[2, 1, 0],
                        confidence_thresh=0.5,
                        iou_threshold=0.45,
                        top_k=200,
                        nms_max_output_size=400)

        # load weights
        self.model.load_weights(weights_path, by_name=True)

        # compile model
        adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        ssd_loss = SSDLoss(neg_pos_ratio=3, alpha=1.0)
        self.model.compile(optimizer=adam, loss=ssd_loss.compute_loss)

        # classses (for reference)
        self.classes = ['background',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat',
           'chair', 'cow', 'diningtable', 'dog',
           'horse', 'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor']
