#from watson_machine_learning_client import WatsonMachineLearningAPIClient
import math
import PIL
import numpy as np
from flask import Flask, request, json, jsonify, render_template
import os


import pvlib as pv
import netCDF4
import siphon
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP

latitude, longitude, tz = 32.2, -110.9, 'US/Arizona'
start = pd.Timestamp(datetime.date.today(), tz=tz)
end = start + pd.Timedelta(days=1)
irrad_vars = ['ghi', 'dni', 'dhi']


model = HRRR()
my_data = model.get_processed_data(latitude, longitude, start, end)

data0 = ''
k=0
for i in my_data['ghi']:
	if k == 0:
		data0 = data0 + '{"y":' + str(i) + '}'
		k=k+1
	if k > 0:
		data0 = data0 + ',{"y":' + str(i) + '}'
		k=k+1
data1 = ''
k=0
for i in my_data['dni']:
	if k == 0:
		data1 = data1 + '{"y":' + str(i) + '}'
		k=k+1
	if k > 0:
		data1 = data1 + ',{"y":' + str(i) + '}'
		k=k+1

#
# 1.  Fill in wml_credentials.
#
#wml_credentials = {
#  "instance_id": "942e2897-3e27-4a57-b120-faa12ec49aaf",
#  "password": "feb82aa8-fdd9-4233-b544-2fa43598650a",
#  "url": "https://us-south.ml.cloud.ibm.com",
#  "username": "1ee6e69c-747b-4c74-a257-f89be1b21e1a"
#}

#client = WatsonMachineLearningAPIClient( wml_credentials )

#
# 2.  Fill in one or both of these:
#     - model_deployment_endpoint_url
#     - function_deployment_endpoint_url
#
#model_deployment_endpoint_url    = "https://us-south.ml.cloud.ibm.com/v3/wml_instances/942e2897-3e27-4a57-b120-faa12ec49aaf/deployments/7e58c8e6-7412-4281-8776-0686072e7c84/online";
#function_deployment_endpoint_url = "https://us-south.ml.cloud.ibm.com/v3/wml_instances/942e2897-3e27-4a57-b120-faa12ec49aaf/deployments/7e58c8e6-7412-4281-8776-0686072e7c84/online";

#def createPayload( canvas_data ):
#    dimension      = canvas_data["height"]
#    img            = Image.fromarray( np.asarray( canvas_data["data"] ).astype('uint8').reshape( dimension, dimension, 4 ), 'RGBA' )
#    sm_img         = img.resize( ( 28, 28 ), Image.LANCZOS )
#    alpha_arr      = np.array( sm_img.split()[-1] )
#    norm_alpha_arr = alpha_arr / 255
#    payload_arr    = norm_alpha_arr.reshape( 1, 784 )
#    payload_list   = payload_arr.tolist()
#    return { "values" : payload_list }


app = Flask( __name__, static_url_path='',template_folder='templates' )

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int( os.getenv( 'PORT', 8000 ) )


#data = '{ "y": 0.40},{ "y": 0.10},{ "y": 0.20},{ "y": 0.30},{ "y": 0.40},{ "y": 0.30},{ "y": 0.40}'


@app.route('/')
#def root():
#    return app.send_static_file( 'index.html' )


def index():

		return render_template('index.html')
	

@app.route('/update')
#def root():
#    return app.send_static_file( 'index.html' )

def index1():
	
	longitude = float(request.args.get('longitude'))
	latitude = float(request.args.get('latitude'))
	if longitude < -130.12:
		longitude = -130.12
	if longitude > -60.86:
		longitude = -60.86
	if latitude < 20.17:
		latitude = 20.17
	if latitude < 50.11:
		latitude = 50.11
	tz = 'US/Arizona'
	start = pd.Timestamp(datetime.date.today(), tz=tz)
	end = start + pd.Timedelta(days=1)
	irrad_vars = ['ghi', 'dni', 'dhi']
	
	
	model = HRRR()
	my_data = model.get_processed_data(latitude, longitude, start, end)
	
	data0 = ''
	k=0
	for i in my_data['ghi']:
		if k == 0:
			data0 = data0 + '{"y":' + str(i) + '}'
			k=k+1
		if k > 0:
			data0 = data0 + ',{"y":' + str(i) + '}'
			k=k+1
	data1 = ''
	k=0
	for i in my_data['dni']:
		if k == 0:
			data1 = data1 + '{"y":' + str(i) + '}'
			k=k+1
		if k > 0:
			data1 = data1 + ',{"y":' + str(i) + '}'
			k=k+1
	
	return render_template('index.html', data0=data0,data1=data1)
	

	

#@app.route( '/sendtomodel', methods=['POST'] )
#def sendtomodel():
#    try:
#        print( "sendtomodel..." )
#        if model_deployment_endpoint_url:
#            canvas_data = request.get_json()
#            payload = canvas_data
#            result = client.deployments.score( model_deployment_endpoint_url, payload )
#            print( "result: " + json.dumps( result, indent=3 ) )
#            return jsonify( result )
#        else:
#            err = "Model endpoint URL not set in 'server.py'"
#            print( "\n\nError:\n" + err )
#            return jsonify( { "error" : err } )
#    except Exception as e:
#        print( "\n\nError:\n" + str( e ) )
#        return jsonify( { "error" : str( e ) } )
    
#@app.route( '/sendtofunction', methods=['POST'] )
#def sendtofunction():
#    try:
#        print( "sendtofunction..." )
#        if function_deployment_endpoint_url:
#            canvas_data = request.get_json()
#            payload = canvas_data
#            result = client.deployments.score( function_deployment_endpoint_url, payload )
#            print( "result: " + json.dumps( result, indent=3 ) )
#            return jsonify( result )
#        else:
#            err = "Function endpoint URL not set in 'server.py'"
#            print( "\n\nError:\n" + err )
#            return jsonify( { "error" : err } )
#    except Exception as e:
#        print( "\n\nError:\n" + str( e ) )
#        return jsonify( { "error" : str( e ) } )

#@app.route( '/sendtowebserver', methods=['POST'] )
#def sendtowebserver():
#    try:
#        print( "sendtowebserver..." )
#        if model_deployment_endpoint_url:
#            canvas_data = request.get_json()
#            payload = createPayload( canvas_data )
#            result = client.deployments.score( model_deployment_endpoint_url, payload )
#            print( "result: " + json.dumps( result, indent=3 ) )
#            return jsonify( result )
#        else:
#            err = "Model endpoint URL not set in 'server.py'"
#            print( "\n\nError:\n" + err )
#            return jsonify( { "error" : err } )
#    except Exception as e:
#        print( "\n\nError:\n" + str( e ) )
#        return jsonify( { "error" : str( e ) } )

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=port, debug=True)
