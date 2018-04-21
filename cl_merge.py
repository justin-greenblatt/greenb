import os
import math
start = os.getcwd()
project = raw_input("Project file in root directory: ")
root_files = os.listdir(".")
while project not in root_files:
	project = input("Project not found in root folder, please reenter a valid project folder name.")
os.chdir(project)

alfabet = "abcdefghijklmnopqrstuvwxyz"
alfa_size = len(alfabet)

Y = input("number of Y")
X = input("number of X")
Z = input("hdr frames")
print(start)
for i in range(Y):
	for j in range(X):
		h = "X" + str(j) + "Y" + str(i)
				
		print(start + "/" + project + "/" + h )
		os.chdir(start + "/" + project + "/" + h )
		sfile = os.listdir(os.getcwd())
                sfile.sort()
                print(sfile)
                alfa = 0
		for x in range(len(sfile)):
                        print(x)
                        
			if x%Z == 0:
                            alfa_first = int(math.floor(alfa/alfa_size))
                            alfa_second = int(alfa%alfa_size)
                            alfa += 1
                            
                            hdr_list = ""
                            for t in range(Z):
                                try:
                                    hdr_list = hdr_list + " " + sfile[x+t]
                                except:
                                    pass
			    os.system( "enfuse -o " + alfabet[alfa_first] + alfabet[alfa_second] + ".tif" + hdr_list)
	                    remove_list = hdr_list.split(" ")[1::]
                            print('remove list',remove_list)
	                    for used_file in remove_list:
                                print('removing',used_file)
                                os.remove(used_file)
		
                os.system("align_image_stack -m -a OUT *.tif")
                for b_filename in os.listdir(os.getcwd()):
                    if not b_filename.startswith("OUT"):
                        os.remove(b_filename)
                os.system("enfuse --exposure-weight=0 --saturation-weight=0 --contrast-weight=1 --hard-mask --contrast-window-size=5 --output=new.tif OUT*.tif")
                for a_filename in os.listdir(os.getcwd()):
                    if not a_filename.startswith("new"):
                        os.remove(a_filename)


		
                '''
                os.system("align_image_stack -m -a OUT *.tif")
		os.system("enfuse --exposure-weight=0 --saturation-weight=0 --contrast-weight=1 --hard-mask --contrast-window-size=5 --output="  + h +".tif OUT*.tif")
                os.chdir('/home/justin/'+project)
		
		
		print("Iteration="+ "X" + str(j) + "Y" + str(i))
		print("Current directory: " + os.getcwd())
		os.chdir(start)		
		print("Moving stacked image to focus file")
		mov1 = 	project + "/"+ h +"/"+ h +".tif"
		mov2 = 	project  + "/focus/" + h + ".tif"
		print(mov1)
		print(mov2)
		os.rename(mov1,mov2)
		os.chdir(project)
		print("Current directory: " + os.getcwd())



os.chdir("focus")
os.system(" pto_gen -o project.pto *.tif")
os.system(" cpfind -o project.pto --multirow --celeste project.pto")
os.system(" cpclean -o project.pto project.pto")
os.system(" linefind -o project.pto project.pto")
os.system(" autooptimiser -a -m -l -s -o project.pto project.pto")
os.

system(" pano_modify --canvas=AUTO --crop=AUTO -o project.pto project.pto")
os.system(" nona -m TIFF_m -o project project.pto")
os.system(" enblend -o project.tif project*.tif")
'''
