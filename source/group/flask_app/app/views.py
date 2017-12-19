from intern.remote.boss import BossRemote
from intern.resource.boss.resource import ChannelResource
from flask import render_template, request
from app import app
from NDR import get_host_token, NeuroDataResource
from skimage import io
import os
import numpy as np
import configparser

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route("/pull_tif", methods=["GET", "POST"])
def pull_tif():
	## TODO:should do some form validation here but w/e for now
	col = request.form["collection"]
	exp = request.form["experiment"]
	channel = request.form["channel"]
	dtype = request.form["datatype"]
	host,token = get_host_token()
	x_range = [int(request.form["xstart"]),int(request.form["xstop"])]
	y_range = [int(request.form["ystart"]),int(request.form["ystop"])]
	z_range = [int(request.form["zstart"]),int(request.form["zstop"])]
	x = '-'.join([str(x1) for x1 in x_range])
	y = '-'.join([str(y1) for y1 in y_range])
	z = '-'.join([str(z1) for z1 in z_range])
	filename = str(col)+'_'+str(exp)+'_'+str(channel)+'_'+str(x)+'_'+str(y)+'_'+str(z)

	resource = NeuroDataResource(host,
                                  token,
                                  col,
                                  exp,
                                  [{'name': channel, 'dtype': dtype}])

	data = resource.get_cutout(channel,
                               z_range,
                               y_range,
                               x_range)

	directory = os.path.dirname('DATA/')
	if not os.path.exists(directory):
		os.makedirs(directory)
	io.imsave('DATA/'+filename+'.tif', data)
	return "Data Saved in DATA folder"

@app.route("/push_tif", methods=["GET", "POST"])
def push_tif():
	#	message1 = request.form['channel']
	#if message1:
	#	print(message1)
	col = request.form["collection"]
	exp = request.form["experiment"]
	channel = request.form["channel"]
	dtype = request.form["datatype"]
	host,token = get_host_token()
	x_range = [int(request.form["xstart"]),int(request.form["xstop"])]
	y_range = [int(request.form["ystart"]),int(request.form["ystop"])]
	z_range = [int(request.form["zstart"]),int(request.form["zstop"])]
	
	remote = BossRemote('./neurodata.cfg')
	voxel_size = '1 1 1'
	voxel_unit = 'micrometers'
	
	channel_resource = ChannelResource(channel, col, exp, 'image', '', 0, dtype, 0)
	project = remote.get_project(channel_resource)
	my_file = request.form["file"]	
	my_array = np.array(io.imread('./DATA/'+my_file)).astype(np.uint8)
	
	for z in range(z_range[0],z_range[1]):
		remote.create_cutout(channel_resource, 0, (x_range[0],x_range[1]), (y_range[0],y_range[1]), (z,z+1), my_array[z].reshape(-1,my_array.shape[1],my_array.shape[2]))
	return 'Successfully pushed'
