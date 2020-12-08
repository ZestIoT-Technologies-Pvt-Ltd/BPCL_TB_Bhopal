#   Copyright (C) 2020 by ZestIOT. All rights reserved. The information in this 
#   document is the property of ZestIOT. Except as specifically authorized in 
#   writing by ZestIOT, the receiver of this document shall keep the information
#   contained herein confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and disseminations to 
#   the receiver's employees shall only be made on a strict need to know basis.
"""
Input: Configuration file path, Weight file path and meta file path of the cylinder model
Output: Image object, network and Class names, all of them are Darknet objects

User Requirement:
1) Loads Cylinder detection model

Requirements:
1) This function loads the cylinder detection model with the given configuration file,
   Weight file and meta file
2 Returns the Darknet image, network and Class name objects which are inturn to make 
  cylinder detection."""


import darknet
import json
config="/home/smartcow/BPCL/BPCL_final/BPCL_config.json"
with open(config) as json_data:
	info= json.load(json_data)
	configPath,weightPath,metaPath= info["xy_tracker"]["configPath"],info["xy_tracker"]["weightPath"],info["xy_tracker"]["metaPath"]

def load_model():
	network, class_names, class_colors = darknet.load_network(configPath,metaPath,weightPath,batch_size=1)
	darknet_image = darknet.make_image(darknet.network_width(network),darknet.network_height(network),3)
	return(darknet_image,network,class_names)
