import os
import math
import numpy as np
import pandas as pd
import sys
import subprocess
import logging

start = os.getcwd()
root_files = os.listdir(os.getcwd())
#Get directory of input files
project = input("Project file in root directory: ")
# Validate Directory		
while project not in root_files:
	project = input("Project not found in root folder, please reenter a valid project folder name.")
os.chdir(project)

# get csv file from project directory. Exit if nothing there
root_files = os.listdir(os.getcwd())
for file in root_files:
    if file.endswith(".csv"):
        csv_file = file
        data = pd.read_csv(csv_file)
       
logging.basicConfig(filename=(project+'_merge.log'), level=logging.INFO)
# Just using this for naming outputs
alfabet = "abcdefghijklmnopqrstuvwxyz"
upper_alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alfa_size = len(alfabet)
# get information about collumns and rows of project to define iterations
y = 0
x = 0
Z = data["z_pos"][0]
hdr_template = ["enfuse","-o"]
a_template = ["align_image_stack", "-m", "--use-given-order", "-a", "OUT" ]
f_template = ["enfuse", "--exposure-weight=0", "--saturation-weight=0", "--contrast-weight=1", "--hard-mask", \
 "--contrast-window-size=5"]
hdr_list = []
aligne_list = []
hdr_fail = False
#iterator
i = 0
limit = data.shape[0]
if True:
    while i < limit:
        logging.info("starting hdr of column {}/{}".format(x,y))
		##############################  HDRing all photos of specific column ##########################
        
        #using indexes again
        name_index_1 = 0
        name_index_2 = 0
        logging.info("Currently processing column  {}/{}".format(x,y)) 
        #print("Limits the Hdring to photos of the same column")
        while data["grid_x"][i] == x and data["grid_y"][i] == y and i < limit:
            #print("finding all elements in specific z position")
            #print(data["z_pos"][i])
            hdr_list = []
            hdr_command = []
            while data["z_pos"][i] == Z and i < limit :
                #print("this is the combination",Z,data["z_pos"][i])
                hdr_list.append(data["name"][i])
                #print("updating photo iterator")
                i += 1
                #print(hdr_list)
                #print(i)
            #Test if hdr is necessary
            
            #print("construct command to be used by Popen")
            hdr_out = "{}{}{}{}.tif".format(upper_alfabet[x],upper_alfabet[y],alfabet[name_index_2],alfabet[name_index_1])    
            hdr_command = hdr_template
            hdr_command.append(hdr_out)
            hdr_command.extend(hdr_list)
            #submit command line process
            #print(hdr_template)
            #print(hdr_command)
            hdr = subprocess.Popen(hdr_command)

		# Observe if process has fineshed sucssesfuly
            hdr.wait()

            for item in hdr_list:
                
                os.remove(item)
                logging.critical("removing {}".format(item))

            del hdr_list
            del hdr_command
            del hdr_template
            hdr_template = ["enfuse","-o"]
            #print("Updating z_pos for next alignement")
            Z = data["z_pos"][i]
            #print("Cleaning list for next HDR")


            if name_index_1 == (len(alfabet)-1):
                name_index_1 = 0
                name_index_2 += 1
            else:
                name_index_1 += 1
                
        a_files = [a for a in os.listdir(os.getcwd()) if a.startswith("{}{}".format(upper_alfabet[x],upper_alfabet[y]))]
        a_files.sort()
        a_old = a_files[0]
        while len(a_files) > 1:
            a_list = a_files[0:10]
            a_command = a_template
            a_command.append(a_old)
            a_command.extend(a_list)
            print("aligne command", a_command)
            aligne = subprocess.Popen(a_command)
            a_template = ["align_image_stack", "-m", "--use-given-order","-a", "OUT" ]
            if aligne.wait() < 0:
            	logging.critical("alignement failed")
            else:
                logging.info("alignement sucssesfull")
            for f in a_files[1:10]:
                os.remove(f)
            del a_files[1:10]
            f_command = f_template
            f_command.append(("--output="+a_old))
            f_files = [a for a in os.listdir(os.getcwd()) if a.startswith("OUT")]
            f_command.extend(f_files)
            print("focus command", f_command)
            f_merge = subprocess.Popen(f_command)
            f_template = ["enfuse", "--exposure-weight=0", "--saturation-weight=0", "--contrast-weight=1", "--hard-mask", \
 "--contrast-window-size=5"]
            if f_merge.wait() < 0:
            	logging.critical("merging failed")
            else:
                for f_out in os.listdir(os.getcwd()):
                    if f_out.startswith("OUT"):
                        os.remove(f_out)
        x = data["grid_x"][i]
        y = data["grid_y"][i]

os.system(" pto_gen -o project.pto *.tif")
os.system(" cpfind -o project.pto --multirow --celeste project.pto")
os.system(" cpclean -o project.pto project.pto")
os.system(" linefind -o project.pto project.pto")
os.system(" autooptimiser -a -m -l -s -o project.pto project.pto")
os.system(" pano_modify --canvas=AUTO --crop=AUTO -o project.pto project.pto")
os.system(" nona -m TIFF_m -o project project.pto")
os.system(" enblend -o project.tif project*.tif")


