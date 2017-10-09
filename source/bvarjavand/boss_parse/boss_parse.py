from NDR import NeuroDataResource
#import json
import pickle
import os
#id: XX_YY_ZZ <- XX = cube id, YY = slice id, ZZ = view id
def get_collman_em_cube(token,z_range,x_range,y_range):
    boss_data = NeuroDataResource(
        'api.boss.neurodata.io',
        token,
        'collman',
        'collman15v2',
        [{'name':'EM25k', 'dtype':'uint8'}])
    cube = boss_data.get_cutout('EM25k', z_range, x_range, y_range)
    #jsoncube = cube.tolist() #to load, use np.array(json.loads(cube)['data'])
    #with open('cube.pickle', 'wb') as f:
    #    pickled = pickle.dump(cube, f)
    metadata = {'id':'01_00_00','dim':[z_range,x_range,y_range],'annotaters':[]} #TODO: id not helpful?
    metacube = {'metadata':metadata, 'data':cube} #TODO: make a class
    with open(metadata['id'] + '.pickle', 'wb') as f:
        metapickled = pickle.dump(metacube, f)

def get_cube_example():
    get_collman_em_cube('edef359a8de270163c911dcef5d467a72348d68d',
        [0,5],
        [0,1000],
        [0,1000])

if __name__ == '__main__':
    get_cube_example()



#note : gt.pickle = [0,25], [1000,3500], [1000,3500]
