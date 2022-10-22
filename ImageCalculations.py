import numpy
from skimage import io
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

IMG_PATH = 'C:/Users/mabo2/Desktop/ArtCards/cards'
PLACEHOLDER = 'C:/Users/mabo2/Desktop/ArtCards/placeholder.png'
COL_LENGTH = 14
COL_HEIGHT = 11

def average_colour(file):
    img = io.imread(file)
    average = img.mean(axis=0).mean(axis=0)
    return average


def calc_colour(directory, coll=None):
    cards = []
    for (directory_path, directory_name, filenames) in os.walk(directory):
        for file in filenames:
            c = average_colour(str(directory_path).replace('\\','/')+"/"+file)
            n = str(file)[str(file).find('_')+1:-4]
            if coll is None:
                cards.append([n, c])
            else:
                set_name, number = n.split("_")
                number = int(number)
                if number in coll[set_name]:
                    cards.append([n, c])

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
    colour_list = calc_colour(IMG_PATH, read_collected())
    print(colour_list) #hier sind noch super viele drin
    result = {}
    for card in colour_list:
        d = 10000.0
        pos = []
        for i in range(len(img)): #ab hier geht es glaube schief irgenwo
            for j in range(len(img[0])):
                if [i, j] in result.values():
                    pass
                else:
                    new_d = colour_distance(img[i][j],card[1])
                    if new_d < d:
                        d = new_d
                        pos = [i,j]
        result[card[0]] = pos[0] * COL_LENGTH + pos[1]
        print(result) #weil hier sind glaube nur noch die drin die auch angezeigt werden ...
    inv = dict((v, k) for k, v in result.items())
    print(inv)
    return inv

def visualize(dict):
    fig, axs = plt.subplots(COL_HEIGHT, COL_LENGTH)
    for i in range(COL_HEIGHT):
        for j in range(COL_LENGTH):
            try:
                index = i * COL_LENGTH + j
                img_short = dict[index] + '.png'
                folder = img_short[0:4]
                img_name = [f for f in os.listdir(IMG_PATH + '/' + folder) if img_short in f]
                print(IMG_PATH + '/' + folder + '/' + img_name[0])
                image = mpimg.imread(IMG_PATH + '/' + folder + '/' + img_name[0])
            except:
                image = mpimg.imread(PLACEHOLDER)
            axs[i,j].imshow(image, origin='lower')
            axs[i,j].axis('off')
    plt.axis('off')
    plt.show()


def convert_to_png():
    for (directory_path, directory_name, filenames) in os.walk(IMG_PATH):
        for file in filenames:
            im = Image.open(directory_path + '/' + file)
            im.save(directory_path + '/' + file)


#convert_to_png()

visualize(optimize_layout("C:/Users/mabo2/Desktop/ArtCards/gradient14x11.png"))
#print(optimize_layout("C:/Users/mabo2/Desktop/ArtCards/gradient14x11.png"))


