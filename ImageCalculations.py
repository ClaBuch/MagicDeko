import PIL.Image
import numpy
from skimage import io
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import xml.etree.ElementTree as ET
from sklearn.cluster import KMeans

tree = ET.parse('config.xml')

IMG_PATH = tree.find('img_path').text
PLACEHOLDER = tree.find('placeholder_path').text
GRADIENT = tree.find('gradient_path').text
COL_LENGTH = 14
COL_HEIGHT = 11

def average_colour(file):
    img = io.imread(file)
    average = img.mean(axis=0).mean(axis=0)
    return average


def calc_colour(directory, coll=None, ret_names=True):
    cards = []
    for (directory_path, directory_name, filenames) in os.walk(directory):
        for file in filenames:
            c = average_colour(str(directory_path).replace('\\','/')+"/"+file)
            n = str(file)[:-4]
            if coll is None:
                if ret_names:
                    cards.append([n, c])
                else:
                    cards.append(c)
            else:
                set_name, number, c_name = n.split("_")
                number = int(number)
                if number in coll[set_name]:
                    if ret_names:
                        cards.append([n, c])
                    else:
                        cards.append(c)
    return cards


def read_collected():
    collection = {}
    with open("cards.txt",'r') as file:
        set_name = ""
        for line in file.readlines():
            if line[0].isdigit():
                cards = [int(x) for x in line.split(",")]
                collection[set_name] = cards
                set_name = ""
            else:
                set_name = line[:-1]
    return collection


def read_gradient(path):
    img = io.imread(path)
    return img


def colour_distance(colour1, colour2):
    dist = 0.0
    for i in range(3):
        dist += (colour1[i]-colour2[i])**2
    dist = numpy.sqrt(dist)
    return dist


def optimize_layout(path):
    img = read_gradient(path)
    colour_list = calc_colour(IMG_PATH)#read_collected()
    print(colour_list)
    result = {}

    for i in range(COL_HEIGHT):
        for j in range(COL_LENGTH):
            d = 10000.0
            c = None
            for card in colour_list:
                    new_d = colour_distance(img[i][j],card[1])
                    if new_d < d:
                        d = new_d
                        c = card
            if c is not None and d<150:
                result[i*COL_LENGTH+j] = c[0]
                colour_list.remove(c)
    return result

def visualize(dict):
    fig, axs = plt.subplots(COL_HEIGHT, COL_LENGTH)
    for i in range(COL_HEIGHT):
        for j in range(COL_LENGTH):
            try:
                index = i * COL_LENGTH + j
                img_short = dict[index] + '.png'
                folder = img_short[0:4]
                path = IMG_PATH + folder + '/' + img_short
                image = PIL.Image.open(path)
                print(IMG_PATH + folder + '/' + img_short)
            except:
                image = mpimg.imread(PLACEHOLDER)
            axs[i,j].imshow(image, origin='upper')
            axs[i,j].axis('off')
    plt.axis('off')
    plt.show()


def convert_to_png():
    for (directory_path, directory_name, filenames) in os.walk(IMG_PATH):
        for file in filenames:
            im = Image.open(directory_path + '/' + file)
            im.save(directory_path + '/' + file)


#convert_to_png()

visualize(optimize_layout(GRADIENT))


#km = KMeans(n_clusters=16)
#feats = numpy.array(calc_colour(IMG_PATH, coll=read_collected(),ret_names=False))
#km.fit(feats)
#print(km.cluster_centers_)
