import pickle
import numpy as np
from skimage import io
from intern.remote.boss import BossRemote
from intern.resource.boss.resource import ChannelResource

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
                raise

    def assert_channel_exists(self, channel):
            return channel in self._chanList.keys()


    def get_cutout(self, chan, zRange=None, yRange=None, xRange=None):
        if not chan in self._chanList.keys():
            print('Error: Channel Not Found in this Resource')
            return
        if zRange is None or yRange is None or xRange is None:
            print('Error: You must supply zRange, yRange, xRange kwargs in list format')
        data = self._bossRemote.get_cutout(self._chanList[chan],
                                           0,
                                           xRange,
                                           yRange,
                                           zRange)
        return data


def test_function():
    #load ground truth file
    #gt = io.imread('./data/gt.tiff')

    #api token is stored internally for security
    token = 'edef359a8de270163c911dcef5d467a72348d68d'
    host = 'api.boss.neurodata.io'
    myResource = NeuroDataResource(host,
                                  token,
                                  'collman',
                                  'collman15v2',
                                  [{'name':'annotation', 'dtype':'uint64'},
                                   {'name':'DAPI1st', 'dtype':'uint8'},
                                   {'name':'GABA488', 'dtype':'uint8'}])

    cutout = myResource.get_cutout('annotation', [2,4], [2300,2500], [3400,3700])
    pickle.dump(cutout,open('gt.pickle', 'wb'))

if __name__ == '__main__':
    test_function()
