#!/usr/bin/env python

import shlex
import configparser
import numpy as np
from  skimage import io
import os

""" Script to generate ingest commands for ingest program """
""" Once generated, copy commands to terminal and run them """

""" Recommend copy this to a new location for editing """

def get_validated_user_input(prompt, type_):
    while True:
        ui = input(prompt)
        if (type(ui) == type(type_)):
            break
        else:
            print("Invalid input, please try again\n")
            continue
    return ui

script = "ingest_large_vol.py"

source_type = 'local'  # either 'local' or 's3'
s3_bucket_name = "BUCKET_NAME"  # not used for 'local' source_type
aws_profile = "default"  # not used for 'local' source_type

boss_config_file = "neurodata.cfg"  # location on local system for boss API key

# Slack messages (optional)
# sends a slack message when ingest is finished with a link to the see the data
# set to a blank string (e.g. '') to exclude from command output
slack_token = ""  # Slack token for sending Slack messages
slack_username = ""  # your slack username

# boss metadata

def cast_type(data, dtype):
    #print('Initial Type: ' + str(data.dtype))
    #data = data.astype(dtype)
    data[data>0] = 254
    #print('Fixed Type: ' + str(data.dtype))
    return data

config = configparser.ConfigParser()
config.read('config.cfg')

collection=config['ANN_METADATA']['collection']
experiment=config['ANN_METADATA']['experiment']
channel=config['ANN_METADATA']['channel']
data_directory=config['ANN_METADATA']['path']
file_name=config['FILENAME']['ann_name'].split('.')[0]
file_format=config['FILENAME']['ann_name'].split('.')[1]
####################################
data_type = 'uint8'

data = io.imread(data_directory+file_name+'.'+file_format)
cast_data = cast_type(data, data_type)
io.imsave(data_directory+file_name+'_0.'+file_format, cast_data)

####################################
'''data_dimensions'''
x,y,z = config['FILENAME']['ann_name'].split('.')[0].split('_')[:]#1x3 vector, x = '0-1280', y = '0-720', z = '0-2'
x1 = str(int(x.split('-')[1])-int(x.split('-')[0]))
y1 = str(int(y.split('-')[1])-int(y.split('-')[0]))
z1 = str(int(z.split('-')[1])-int(z.split('-')[0]))
data_dimensions = x1+' '+y1+' '+z1
####################################
zrange = [int(z.split('-')[0]),int(z.split('-')[1])]
####################################

'''DONT TOUCH BELOW HERE PLEASE'''
z_step = '1'
voxel_size = '1 1 1'
voxel_unit = 'micrometers'

workers = 1

""" Code to generate the commands """

def gen_comm(zstart, zend):
    cmd = "python3 " + script + " "
    cmd += ' --base_path ' + shlex.quote(data_directory)
    cmd += ' --base_filename ' + shlex.quote(file_name)
    cmd += ' --extension ' + file_format
    cmd += ' --datasource ' + source_type
    cmd += ' --collection ' + collection
    cmd += ' --experiment ' + experiment
    cmd += ' --channel ' + channel
    cmd += ' --voxel_size ' + voxel_size
    cmd += ' --voxel_unit ' + voxel_unit
    cmd += ' --datatype ' + data_type
    cmd += ' --img_size ' + data_dimensions
    cmd += ' --z_range %d %d ' % (zstart, zend)
    cmd += ' --z_step ' + z_step
    cmd += ' --warn_missing_files'
    cmd += ' --boss_config_file ' + boss_config_file

    if slack_token != '' and slack_username != '':
        cmd += ' --slack_token_file ' + slack_token
        cmd += " --slack_usr " + slack_username

    if source_type == 's3':
        cmd += " --s3_bucket_name " + s3_bucket_name
        cmd += ' --aws_profile ' + aws_profile
    cmd += " &"

    return cmd


range_per_worker = (zrange[1] - zrange[0]) // workers

print("# Range per worker: ", range_per_worker)

if range_per_worker % 16:  # supercuboids are 16 z slices
    range_per_worker = ((range_per_worker // 16) + 1) * 16

print("# Range per worker (rounded up): ", range_per_worker)

# amount of memory per worker
ddim_xy = list(map(int, data_dimensions.split(' ')[0:2]))
if data_type == 'uint8':
    mult = 1
elif data_type == 'uint16':
    mult = 2
elif data_type == 'uint64':
    mult = 8
mem_per_w = ddim_xy[0] * ddim_xy[1] * mult * 16 / 1024 / 1024 / 1024
print('# Expected memory usage per worker {:.1f} GB'.format(mem_per_w))

# amount of memory total
mem_tot = mem_per_w * workers
print('# Expected total memory usage: {:.1f} GB'.format(mem_tot))





#cmd = gen_comm(zrange[0], zrange[1])
#cmd += ' --create_resources '
#print('\n' + cmd + '\n')

for worker in range(workers):
    start_z = max((worker * range_per_worker +
                   zrange[0]) // 16 * 16, zrange[0])
    if start_z < zrange[0]:
        start_z = zrange[0]
    if start_z > zrange[1]:
        # No point start a useless thread
        continue

    next_z = ((worker + 1) * range_per_worker + zrange[0]) // 16 * 16
    end_z = min(zrange[1], next_z)

    cmd = gen_comm(start_z, end_z)
    cmd += ' --create_resources '
    print(cmd)
    print('\n')
    os.system(cmd)
