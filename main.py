import csv 
import os
import glob
from shutil import copyfile

gas_count = 0 
elec_count = 0

config_files=[]
with open('config/appliance_config.csv', newline='') as csvfile : 
	fr = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in fr : 
		if "Total Number of Houses" in row[0] : 
			total_count = int(int(row[1])/3) #count per phase
		elif 'Run Name' in row[0] : 
			continue 
		else :
			elec_count = total_count*float(row[1])
			gas_count = total_count-elec_count
			config_file_name = 'elec_config_'+str(row[0]).replace(" ", "_")+'.glm'
			config_files.append(config_file_name)
			fw = open("elec_config/"+config_file_name, 'w')
			fw.write('#define HOUSESPERPHASE=' + str(int(total_count)))
			fw.write('\n#define GAS_COUNT=' + str(int(gas_count))) 
			fw.write('\n#define ELEC_COUNT=' + str(int(elec_count))) 

for i,file_name in enumerate(config_files) : 
	if i==0 : # resetting the folder by removing all the model files 
		files = glob.glob('model_files/*')
		for f in files : 
			os.remove(f)
	copyfile('model.glm', 'model_files/model.glm')
	new_file = "model_files/model_"+file_name
	os.rename("model_files/model.glm",new_file)

	with open(new_file, 'r+') as fm:
			content = fm.read()
			fm.seek(0, 0)
			line="#include \"elec_config/" + file_name + "\"" 
			fm.write(line+"\n"+"#define RUN_NAME="+file_name[12:-4]+"\n")











