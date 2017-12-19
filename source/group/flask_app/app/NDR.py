import pickle
import numpy as np
from skimage import io
from intern.remote.boss import BossRemote
from intern.resource.boss.resource import ChannelResource
import cmd
import sys
import os, errno
import datetime
#import configparser

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

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

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
    timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
    ensure_dir("./DATA/"+str(col)+'/'+str(exp)+'/'+str(channel)+'/'+timestamp+'/')
    data_path = "./DATA/"+str(col)+'/'+str(exp)+'/'+str(channel)+'/'+timestamp+'/'

    print("\n Specify Annotation Resource, User input REQUIRED \n")
    ann_col = get_validated_user_input("Annotation Collection: ", "str")
    ann_exp = get_validated_user_input("Annotation Experiment: ", "str")
    ann_channel = get_validated_user_input("Annotation Channel: ", "str")
    ann_dtype = 'uint64'
    ensure_dir("./DATA/"+str(ann_col)+'/'+str(ann_exp)+'/'+str(ann_channel)+'/')
    ann_path = "./DATA/"+str(ann_col)+'/'+str(ann_exp)+'/'+str(ann_channel)+'/'

    config = configparser.ConfigParser()
    config['METADATA'] = {
                        'collection':col,
                        'experiment':exp,
                        'channel':channel,
                        'data_type':dtype,
                        'path':data_path,
                        'time_stamp':timestamp
                        }
    config['ANN_METADATA'] = {
                        'collection':ann_col,
                        'experiment':ann_exp,
                        'channel':ann_channel,
                        'path':ann_path,
                        }
    with open('config.cfg', 'w') as configfile:
        config.write(configfile)

    return myResource, channel, dtype, data_path

def user_get_cutout(resource, channel, dtype):
    print("\n Specify cutout, User input REQUIRED \n")

    x_str = get_validated_user_input("X Range, Format: <XSTART> <XEND>: ", "str")
    x_range = [int(x) for x in x_str.split(" ")]

    y_str = get_validated_user_input("Y Range, Format: <YSTART> <YEND>: ", "str")
    y_range = [int(y) for y in y_str.split(" ")]

    z_str = get_validated_user_input("Z Range, Format: <ZSTART> <ZEND>: ", "str")
    z_range = [int(z) for z in z_str.split(" ")]

    xyz = x_str.replace(' ','-')+'_'+y_str.replace(' ','-')+'_'+z_str.replace(' ','-')

    print("\n Getting Cutout... \n")
    data = resource.get_cutout(channel,
                               z_range,
                               y_range,
                               x_range)

    return data, dtype, xyz

def user_save_data(data_path, data, xyz):
    print("\n Save Data \n")

    config = configparser.ConfigParser()
    config['FILENAME'] = {
                        'name':xyz+'.tif',
                        'ann_name':xyz+'.tif'
                        }
    with open('config.cfg', 'a') as configfile:
        config.write(configfile)

    save_image(data_path, xyz+'.tif', data)

def cast_type(data, dtype):
    print('Initial Type: ' + str(data.dtype))
    data = data.astype(dtype)
    print('Fixed Type: ' + str(data.dtype))
    return data


if __name__ == '__main__':
    host, token = get_host_token()
    myResource, channel, dtype, data_path = user_get_neurodata_resource(host, token) ## TODO: Make this less jank, figure out channel resource
    data, dtype, xyz = user_get_cutout(myResource, channel, dtype) ##TODO: Make this less jank
    data = cast_type(data, dtype) #TODO
    user_save_data(data_path,data, xyz)
