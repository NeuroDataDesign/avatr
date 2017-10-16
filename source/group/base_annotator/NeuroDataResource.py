import pickle
import numpy as np
from skimage import io
from intern.remote.boss import BossRemote
from intern.resource.boss.resource import ChannelResource
import cmd
import sys

class NeuroDataResource:
    def __init__(self, host, token, collection, experiment, chanList):
        self._collection = collection
        self._experiment = experiment
        self._bossRemote = BossRemote({'protocol':'https',
                                       'host':host,
                                       'token':token})
        self._chanList = {}
        for chanDict in chanList:
            try:
                self._chanList[chanDict['name']] = ChannelResource(chanDict['name'],
                                                                   collection,
                                                                   experiment,
                                                                   'image',
                                                                   datatype=chanDict['dtype'])
            except:
                #TODO error handle here
                raise Exception("Failed to load")
                sys.exit(1)

    def assert_channel_exists(self, channel):
        return channel in self._chanList.keys()


    def get_cutout(self, chan, zRange=None, yRange=None, xRange=None):
        if not chan in self._chanList.keys():
            print('Error: Channel Not Found in this Resource')
            sys.exit(1)
            return
        if zRange is None or yRange is None or xRange is None:
            print('Error: You must supply zRange, yRange, xRange kwargs in list format')
            sys.exit(1)
        data = self._bossRemote.get_cutout(self._chanList[chan],
                                           0,
                                           xRange,
                                           yRange,
                                           zRange)
        return data

def save_image(datadir, filename, data):
    try:
        filename = datadir + filename
        io.imsave(filename, data)
    except:
        raise Exception("Data could not be saved")


def get_host_token(filename = "neurodata.cfg"): #expects neurodata.cfg file format
    print("\n Loading neurodata.cfg \n")
    host = None
    token = None
    try:
        with open(filename, "r") as f:
            for line in f:
                if line.startswith("host"):
                    host = line.split(" ")[-1]
                if line.startswith("token"):
                    token = line.split(" ")[-1]
    except:
        raise Exception("neurodata.cfg file not found.\n")
        sys.exit(1)
    if host == None:
        raise Exception("Host not found\n")
        sys.exit(1)
    if token == None:
        raise Exception("Token not found\n")
        sys.exit(1)
    print("Loaded host: " + host)
    print("Loaded token: " + token)
    return host, token


def get_validated_user_input(prompt, type_):
    while True:
        ui = input(prompt)
        if (type(ui) == type(type_)):
            break
        else:
            print("Invalid input, please try again\n")
            continue
    return ui

def user_get_neurodata_resource(host, token):
    print("\n Specify Boss Resource, User input REQUIRED \n")

    col = get_validated_user_input("Collection: ", "str")
    exp = get_validated_user_input("Experiment: ", "str")
    channel = get_validated_user_input("Channel: ", "str")
    dtype = get_validated_user_input("Datatype: ", "str")

    print("\n Loading Boss Resource... \n")

    myResource = NeuroDataResource(host,
                                  token,
                                  col,
                                  exp,
                                  [{'name': channel, 'dtype': dtype}])
    print("Successfully Loaded Boss Resource!\n")

    return myResource, channel

def user_get_cutout(resource, channel):
    print("\n Specify cutout, User input REQUIRED \n")

    z_str = get_validated_user_input("Z Range, Format: <ZSTART> <ZEND>: ", "str")
    z_range = [int(z) for z in z_str.split(" ")]

    y_str = get_validated_user_input("Y Range, Format: <YSTART> <YEND>: ", "str")
    y_range = [int(y) for y in y_str.split(" ")]

    x_str = get_validated_user_input("X Range, Format: <XSTART> <XEND>: ", "str")
    x_range = [int(x) for x in x_str.split(" ")]

    print("\n Getting Cutout... \n")
    data = resource.get_cutout(channel,
                               z_range,
                               y_range,
                               x_range)
    return data

def user_save_data(data):
    print("\n Save Data \n")

    data_path = get_validated_user_input("Data Dir, Format: path/to/data/: ", "str")
    filename = get_validated_user_input("Filename (.tif recommended): ", "str")
    save_image(data_path, filename, data)


if __name__ == '__main__':
    host, token = get_host_token()
    myResource, channel = user_get_neurodata_resource(host, token) ## TODO: Make this less jank, figure out channel resource
    data = user_get_cutout(myResource, channel) ##TODO: Make this less jank
    user_save_data(data)
