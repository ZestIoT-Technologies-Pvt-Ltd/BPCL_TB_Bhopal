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
