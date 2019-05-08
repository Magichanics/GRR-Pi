from SSDKeras import SDDNeuralNetwork512
from imageio import imread
from keras.preprocessing import image

def img_to_array(img_path):

    # convert image to array to fit into neural network
    img = image.load_img(img_path, target_size=(512, 512))
    img = image.img_to_array(img)
    return img

if __name__ == '__main__':
    nn = SDDNeuralNetwork512(weights_path='VGG_VOC0712_SSD_512x512_iter_120000.h5')
    y_test, modified_img = nn.predict(img_to_array('mp2d.png')) # random map
