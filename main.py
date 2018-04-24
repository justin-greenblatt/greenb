

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import motor
import pygame
import sys
import ctypes
import signal
import os
import subprocess
import random
import time
import math
import cv2
import re
import logging

#BASIC PYGAME

pygame.init()
pygame.font.init() 
clock = pygame.time.Clock()
screen_width = 1300
screen_height = 1000
screen = pygame.display.set_mode([screen_width, screen_height])

block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
button_list = pygame.sprite.Group()
label_list = pygame.sprite.Group()

#CLASSES

class Block(pygame.sprite.Sprite):

 
    def __init__(self, color, width, height,x_pos = None, y_pos = None, text = None,value = None, font_type = 'ubuntumono', font_size = 20, text_color = [0,0,0], text_x = 5, text_y = 5, direction = 0, index_x = None, index_y = None):

        super().__init__()
 

        self.size = [width,height]
        self.image = pygame.Surface(self.size)
        self.image.fill(color)
        self.color = color
        self.x = x_pos
        self.y = y_pos
        self.text_x = text_x
        self.text_y = text_y
        self.text = text
        self.font_type = font_type
        self.font_size = font_size
        self.text_color = text_color
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.textsurface = self.font.render(self.text, False, self.text_color)
        self.image.blit(self.textsurface,(self.text_x, self.text_y))
        self.direction = direction
        self.index_x = index_x
        self.index_y = index_y
        self.value = value
    def update(self, txt):
        self.text = txt
        self.image.fill(self.color)
        self.textsurface = self.font.render(self.text, False, self.text_color)
        self.image.blit(self.textsurface,(self.text_x, self.text_y))
    
    def change_text(self, data_pos):
        data_pos = data_pos + self.diection
        
        return data_pos


# CAMERA PARAMETERS FOR LIVEVIEW
gp = ctypes.CDLL('/usr/local/lib/libgphoto2.so.6.0.0')
GP_OK = fileNbr = 0
GP_VERSION_VERBOSE = 1
cam = ctypes.c_void_p()
gp.gp_camera_new(ctypes.byref(cam))
ctx = gp.gp_context_new()
fil = ctypes.c_void_p()
gp.gp_file_new(ctypes.byref(fil))
old_tick = round(time.time())
#POSITIONING PARAMETERS

barrier = 724
b1 = 510
b2 = 545
b3 = 580
b4 = 615
b5 = 650
b6 = 685
b7 = 720
b8 = 755
b9 = 790
done = False

grid_x = 0
grid_y = 0
exposures = []

z_low = None
z_high = None

column = 200

# CREATING SURFACES
nav = pygame.surface.Surface((400, 400))
nav.fill((255,255,255))

camera_width = 70
camera_height = 50
camera = pygame.surface.Surface((camera_width,camera_height))

camera.fill((0,0,255))
camera.set_alpha(80)


nav_border = pygame.surface.Surface((505, 450))
nav_border.fill((155,155,155))

h_scale =  pygame.surface.Surface((30, 400))
h_scale.fill((255,255,255))

camera_level = pygame.surface.Surface((30, 5))
camera_level.fill((30,30,255))

camera_low = pygame.surface.Surface((30, 20))
camera_low.fill([255,150,150])

camera_high = pygame.surface.Surface((30, 20))
camera_high.fill([255,255,140])



btx = 7
bty = 2
color1 = [255,255,255]
color2 = [100,100,100]
#navigator coordinates
nav_x_count = Block((155,155,155),125,25, text = 'X',text_color = [255,255,255])
nav_y_count = Block((155,155,155),125,25, text = 'Y',text_color = [255,255,255])
nav_z_count = Block((155,155,155),125,25, text = 'Z',text_color = [255,255,255])


#STARTING SCREEN

button_start = Block((0,0,0),1000,50, text = ' PLEASE PRESS ALL CALIBRATION BUTTONS AS A SECURITY CHECK ',text_color = [255,255,255],font_size = 40)
                     
x_button_start = Block((255,255,0),250,100, text = 'X BUTTON', text_color = [0,0,0],text_x = 30,text_y = 30,font_size = 50)

y_button_start = Block((255,255,0),250,100, text = 'Y BUTTON', text_color = [0,0,0],text_x = 30,text_y = 30,font_size = 50)

#cols button
grid_cols_list = range(1,15)
grid_cols_index = 3
grid_cols_disp_text = "Cols:    " + str(grid_cols_list[grid_cols_index])
grid_cols_disp = Block(color1,175,25, text = grid_cols_disp_text,text_color = color2,text_x = btx, text_y = bty)
grid_cols_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty, direction = 1)
grid_cols_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty, direction = -1)
grid_cols_up.rect.x =  barrier + 220
grid_cols_up.rect.y = b1
grid_cols_down.rect.x =  barrier + 185
grid_cols_down.rect.y = b1
button_list.add(grid_cols_down)
button_list.add(grid_cols_up)


#rows button
grid_rows_list = range(1,15)
grid_rows_index = 3
grid_rows_disp_text = "Rows:    " +str(grid_rows_list[grid_rows_index])
grid_rows_disp = Block(color1,175,25, text = grid_rows_disp_text,text_color = color2,text_x = btx, text_y = bty)
grid_rows_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
grid_rows_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
grid_rows_up.rect.x =  barrier + 220
grid_rows_up.rect.y = b2
grid_rows_down.rect.x =  barrier + 185
grid_rows_down.rect.y = b2
button_list.add(grid_rows_down)
button_list.add(grid_rows_up)

#shutter button
shutter_list = ["0.0002s","0.0003s","0.0004s","0.0005s","0.0006s","0.0008s","0.0010s",
           "0.0012s","0.0015s","0.0020s","0.0025s","0.0031s","0.0040s","0.0050s",
           "0.0062s","0.0080s","0.0100s","0.0125s","0.0166s","0.0200s","0.0250s",
           "0.0333s","0.0400s","0.0500s","0.0666s","0.0769s","0.1000s","0.1250s",
           "0.1666s","0.2000s","0.2500s","0.3333s","0.4000s","0.5000s","0.6250s",
           "0.7692s","1.0000s","1.3000s","1.6000s","2.0000s","2.5000s","3.0000s",
           "4.0000s","5.0000s","6.0000s","8.0000s","10.0000s","13.0000s","15.0000s",
           "20.0000s","25.0000s","30.0000s"]
shutter_index = 15
shutter_disp_text = "Shutter: " + str(shutter_list[shutter_index])
shutter_disp = Block((200,255,255),175,25, text = shutter_disp_text,text_color = color2,text_x = btx, text_y = bty)
shutter_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
shutter_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
shutter_up.rect.x =  barrier + 220 + 260
shutter_up.rect.y = b2
shutter_down.rect.x =  barrier + 185 + 260
shutter_down.rect.y = b2
button_list.add(shutter_down)
button_list.add(shutter_up)

#iso button
iso_list = ["100","200","300","400","800","1600","3200","6400","12800"]
iso_index = 0
iso_disp_text = "Iso:     " + str(iso_list[iso_index])
iso_disp = Block((200,255,255),175,25, text = iso_disp_text,text_color = color2,text_x = btx, text_y = bty)
iso_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
iso_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
iso_up.rect.x =  barrier + 220 + 260
iso_up.rect.y = b1
iso_down.rect.x =  barrier + 185 + 260
iso_down.rect.y = b1
button_list.add(iso_down)
button_list.add(iso_up)


#zstep button
z_step_list = range(1,30)
z_step_index = 2
z_step_text = "Z Step:  " + str(z_step_list[z_step_index])
z_step_disp = Block(color1,175,25, text = z_step_text,text_color = color2,text_x = btx, text_y = bty)
z_step_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
z_step_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
z_step_up.rect.x =  barrier + 220
z_step_up.rect.y = b5
z_step_down.rect.x =  barrier + 185
z_step_down.rect.y = b5    
button_list.add(z_step_down)
button_list.add(z_step_up)

layers = math.ceil(column/z_step_list[z_step_index])
#x_step button
x_step_list = range(70,95,2)
x_step_index = 8
x_step_text = "Overlap: " + str(x_step_list[x_step_index])
x_step_disp = Block(color1,175,25, text = x_step_text,text_color = color2,text_x = btx, text_y = bty)
x_step_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
x_step_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
x_step_up.rect.x =  barrier + 220
x_step_up.rect.y = b3
x_step_down.rect.x =  barrier + 185
x_step_down.rect.y = b3   
button_list.add(x_step_down)
button_list.add(x_step_up)

#y_step button ----- CHANGED TO CAMERA SIZE
y_step_list = range(12,180,2)
y_step_index = 9
y_step_text = "CAM:  " + str(y_step_list[y_step_index])
y_step_disp = Block(color1,175,25, text = y_step_text,text_color = color2,text_x = btx, text_y = bty)
y_step_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
y_step_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
y_step_up.rect.x =  barrier + 220
y_step_up.rect.y = b4
y_step_down.rect.x =  barrier + 185
y_step_down.rect.y = b4
button_list.add(y_step_down)
button_list.add(y_step_up)

#Image quality button
img_list = [["JPEG Basic","3008x2000",0.2],["JPEG Basic","4512x3000",0.4],["JPEG Basic","6016x4000",0.6],\
            ["JPEG Normal","3008x2000",0.6],["JPEG Normal","4512x3000",0.8],["JPEG Normal","6016x4000",1],\
            ["JPEG Fine","3008x2000",1.2],["JPEG Fine","4512x3000",1.4],["JPEG Fine","6016x4000",1.6],\
            ["NEF (Raw)","6016x4000",2]]
img_index = 9
img_text = "Image Q:    " + str(img_list[img_index][0] + img_list[img_index][1])
img_disp = Block(color1,175,25, text = img_text,text_color = color2,text_x = btx, text_y = bty,font_size = 14)
img_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
img_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
img_up.rect.x =  barrier + 220
img_up.rect.y = b6
img_down.rect.x =  barrier + 185
img_down.rect.y = b6
button_list.add(img_down)
button_list.add(img_up)


#canny parameter 1
canny1_list = range(5,200,5)
canny1_index = 10
canny1_text = "Canny1:  " + str(canny1_list[canny1_index])
canny1_disp = Block(color1,175,25, text = canny1_text,text_color = color2,text_x = btx, text_y = bty)
canny1_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
canny1_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
canny1_up.rect.x =  barrier + 220
canny1_up.rect.y = b7
canny1_down.rect.x =  barrier + 185
canny1_down.rect.y = b7
button_list.add(canny1_down)
button_list.add(canny1_up)

#canny parameter 2
canny2_list = range(5,200,5)
canny2_index = 20
canny2_text = "Canny2:  " + str(canny2_list[canny2_index])
canny2_disp = Block(color1,175,25, text = canny2_text,text_color = color2,text_x = btx, text_y = bty)
canny2_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
canny2_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
canny2_up.rect.x =  barrier + 220
canny2_up.rect.y = b8
canny2_down.rect.x =  barrier + 185
canny2_down.rect.y = b8
button_list.add(canny2_down)
button_list.add(canny2_up)

#threshold button
threshold_list = range(10)
threshold_index = 0
threshold_text = "Treshold: " + str(canny2_list[canny2_index])
threshold_disp = Block(color1,175,25, text = canny2_text,text_color = color2,text_x = btx, text_y = bty)
threshold_up = Block(color1,25,25, text = ">",text_color = color2,text_x = btx, text_y = bty,direction = 1)
threshold_down = Block(color1,25,25, text = "<",text_color = color2,text_x = btx, text_y = bty,direction = -1)
threshold_up.rect.x =  barrier + 220
threshold_up.rect.y = b9
threshold_down.rect.x =  barrier + 185
threshold_down.rect.y = b9
button_list.add(threshold_down)
button_list.add(threshold_up)


#set Grid button
grid_set = Block([200,200,200],245,25, text = "        SET GRID",text_color = color2,text_x = btx, text_y = bty)
grid_set.rect.x =  barrier + 260
grid_set.rect.y = b6
button_list.add(grid_set)
#add button
add_button = Block([130,255,255],245,25, text = "    ADD CAMERA FRAME",text_color = color2,text_x = btx, text_y = bty)
add_button.rect.x =  barrier + 260
add_button.rect.y = b3
button_list.add(add_button) 
#add set bottom
lowest_focus = Block([255,150,150],245,25, text = "    SET LOWEST FOCUS",text_color = color2,text_x = btx, text_y = bty)
lowest_focus.rect.x =  barrier + 260
lowest_focus.rect.y = b8
button_list.add(lowest_focus)
#add highest
highest_focus = Block([255,255,140],245,25, text = "    SET HIGHEST FOCUS",text_color = color2,text_x = btx, text_y = bty)
highest_focus.rect.x =  barrier + 260
highest_focus.rect.y = b7
button_list.add(highest_focus) 

#EXPOSURE CLEAR
exposure_clear = Block([255,255,255],245,25, text = "    CLEAR EXPOSURES",text_color = color2,text_x = btx, text_y = bty)
exposure_clear.rect.x =  barrier + 260
exposure_clear.rect.y = b5
button_list.add(exposure_clear) 


#PREVIEW ALL
preview_all = Block([130,255,255],245,25, text = "  PREVIEW ALL FRAMES",text_color = color2,text_x = btx, text_y = bty)
preview_all.rect.x =  barrier + 260
preview_all.rect.y = b4
button_list.add(preview_all) 

#canny button
preview_button = Block([255,255,255],120,100, text = "CANNY",text_color = color2,text_x = 25, text_y = 40)
preview_button.rect.x =  20
preview_button.rect.y = b1   
button_list.add(preview_button)

#run button
run_button = Block([100,255,100],120,100, text = "RUN",text_color = color2,text_x = 45, text_y = 40)
run_button.rect.x =  20
run_button.rect.y = b4
button_list.add(run_button)

#orientation button
orientation_button = Block([255,255,255],120,100, text = "ORIENTATION",text_color = color2,text_x = 5, text_y = 40)
orientation_button.rect.x =  150
orientation_button.rect.y = b1   
button_list.add(orientation_button)
orientation_list = ["Horizontal","Vertical"]
orientation_index = 1
#reset button
reset_button = Block([255,255,255],120,100, text = "RESET",text_color = color2,text_x = 37, text_y = 40)
reset_button.rect.x =  150
reset_button.rect.y = b4
button_list.add(reset_button)

# run labels
project_name_disp = Block([250,250,250],425,25, text = "PROJECT NAME:             ",text_color = color2,text_x = 130, text_y = 3)
text = ""
project_name_disp.rect.x = 280
project_name_disp.rect.y = b1
button_list.add(project_name_disp)
run_label = Block([230,230,230],425,25, text = "RUN SPECIFICATIONS",text_color = color2,text_x = 130, text_y = 3)
label_font = 18
run_label1_text = "COLS:"+str(grid_cols_list[grid_cols_index]) + " ROWS:"+ str(grid_rows_list[grid_rows_index])+" ORIENTATION:" + orientation_list[orientation_index]+ " Expo:" + str(len(exposures)) + " ImageQ:" + str(img_list[img_index])
run_label2_text = "Xstep:" + str(x_step_list[x_step_index]) + "   Ystep:" + str(y_step_list[y_step_index]) + "  Zstep:" + str(z_step_list[z_step_index]) + "   Grid:" + str(grid_x) + "," + str(grid_y)  + "  Zdepth:" + str(layers)
run_label1 = Block([230,230,230],425,25, text = run_label1_text,text_color = color2,text_x = 3, text_y = 3,font_size = label_font)
run_label2 = Block([230,230,230],425,25, text = run_label2_text,text_color = color2,text_x = 3, text_y = 3,font_size = label_font)

#----------------     CAMERA FUNCTIONS     -------------------
def dslr(command, cycle=0):
    camera_process = subprocess.call(command)
    cycles = cycle
    if camera_process != 0:
        if cycles < 10:
            cycles +=1
            
            time.sleep(1)
            dslr(command,cycles)
        else:
            try:
                logging.warning("Error after 10 cycles trying to execute Dslr command: ",command)

            except:  
                print("Error after 10 cycles trying to execute Dslr command: ",command)
def cam_shutter(value):
    
    return ["gphoto2","--set-config", "/main/capturesettings/shutterspeed=" + value] 


def cam_iso(value):
    return ["gphoto2","--set-config", "/main/imgsettings/iso=" + value] 

def cam_img_size(value):
    
        return ["gphoto2","--set-config","/main/other/5003=" + value] 

def cam_img_quality(string):

        return ["gphoto2","--set-config","/main/capturesettings/imagequality=" + string] 


def camera_match(expression):
    
    camera_files  = subprocess.check_output(['gphoto2','--list-files'])
    m = re.findall(expression,camera_files)
    return m
    
def newfolder(name):
    os.makedirs(name)
    os.chdir(name)

def killstart():
    p= subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate ()

    for line in out.splitlines() :
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None,1) [0])
            os.kill(pid, signal.SIGKILL)
def find_delete_folder():
    folder = camera_match(r"/store_00010001/DCIM/1.......")
    return ["gphoto2","--folder",folder, "-R", "--delete-all-files"]


clear = ["gphoto2","--folder", "/store_00010001/DCIM/100D3200", "-R", "--delete-all-files"]
trigger = ["gphoto2","--trigger-capture"]
download = ["gphoto2","--get-all-files"]
memorycard = ["gphoto2","--set-config", "capturetarget=1"]

def files_num(i):
    order = ["gphoto2","--folder"]
    directory = "/store_00010001/DCIM/10{}D3200".format(i)
    ext = ["-R", "--num-files"]
    order.append(directory)
    order.extend(ext)
    pros = subprocess.check_output(order)


    numberr = int(pros[59:])
    return numberr


def check(rtn):
    if rtn != GP_OK:
        gp.gp_result_as_string.restype = ctypes.c_char_p
        print('!! ERROR(%s) %s' % (rtn,gp.gp_result_as_string(rtn)))
        sys.exit(0)



#  CREATING GRAPHICAL REPRESENTATION OF A GRID
def grid_create(p_x, p_y,x_motor,y_motor,frame_width,frame_height,cols,rows):
    
    grid_color=[225,225,255]
    overlap_color = [210,210,255]
    
    overlap_x = frame_width - x_motor
    overlap_y = frame_height - y_motor
    pos_y = p_y
    for i in range(rows):
        pos_x = p_x
        for l in range(cols):
            
                 
            if l == 0 or l == (cols-1):
                draw_width = frame_width - overlap_x
            else:
                draw_width = frame_width - (2*overlap_x)
            if i == 0 or i == (rows - 1):
                draw_height = frame_height - overlap_y
            else:
                draw_height = frame_height - (2*overlap_y)
            
            if l != 0 and i != 0:
                block = Block(grid_color,draw_width,draw_height,(pos_x - overlap_x),(pos_y - overlap_y),index_x = l,index_y = i)
            elif l != 0:
                block = Block(grid_color,draw_width,draw_height,(pos_x - overlap_x),pos_y,index_x = l,index_y = i)
            elif i != 0:
                block = Block(grid_color,draw_width,draw_height,pos_x,(pos_y - overlap_y),index_x = l,index_y = i)
            else:
                block = Block(grid_color,draw_width,draw_height,pos_x,pos_y,index_x = l,index_y = i)
            block.rect.x = pos_x
            block.rect.y = pos_y
            block_list.add(block)
            all_sprites_list.add(block)
           
            if i != (rows-1):
                over  =  Block(overlap_color,draw_width,overlap_y) 
                over.rect.x = pos_x 
                over.rect.y = pos_y + draw_height
                
                all_sprites_list.add(over) 

         
            pos_x = pos_x + draw_width
            if l != (cols-1):
                if i != (rows-1):
                    over  =  Block(overlap_color,overlap_x,(draw_height + overlap_y)) 
                    over.rect.x = pos_x 
                    over.rect.y = pos_y
                    all_sprites_list.add(over) 
                    pos_x = pos_x + overlap_x
                else:
                    over  =  Block(overlap_color,overlap_x,draw_height) 
                    over.rect.x = pos_x 
                    over.rect.y = pos_y
                    all_sprites_list.add(over) 
                    pos_x = pos_x + overlap_x

        pos_y = pos_y + draw_height + overlap_y
             
def calibrate_xy():
    x = motor.button_x()
    y = motor.button_y()
    calibration_count_x = 0
    calibration_count_y = 0
    print("Starting Calibration")
    while not x or not y and calibration_count_x < 8500 and calibration_count_y < 8500:
        x = motor.button_y()
        y = motor.button_x()

        if not x and not y:
            motor.small_bottom_left(5) 
            calibration_count_x = calibration_count_x + 5
            calibration_count_y = calibration_count_y + 5
        elif not x:
            
            motor.small_left(5)
            calibration_count_x = calibration_count_x + 5
        elif not y:
            
            motor.small_down(5)
            calibration_count_y = calibration_count_y + 5
    print("Calibration Ended")
    calibration = (calibration_count_x,calibration_count_y)
    return calibration

    
done = False
click_pos = [None,None]
go_to = False
  
killstart()
time.sleep(0.5)

check(gp.gp_camera_init(cam, ctx))
print('** camera connected')
camera_width = (y_step_list[y_step_index])
camera_height = round((camera_width*2)/3)
pygame.display.set_caption('Macro Viewer')

#---------BUTTON SECURITY CHECK ------------
screen.blit(button_start.image,(160,300))
screen.blit(x_button_start.image,(700,500))
screen.blit(y_button_start.image,(300,500))
pygame.display.update()

check_x = False
check_y = False
while not check_x or not check_y:
    x = motor.button_y()
    y = motor.button_x()
    if x:
        check_x = True
        x_button_start.image.fill([0,255,0])
        
        screen.blit(x_button_start.image,(700,500))

    if y:
        check_y = True
        y_button_start.image.fill([0,255,0])
        
        screen.blit(y_button_start.image,(300,500))
    pygame.display.update()
button_start.update("CALIBRATING...")
screen.fill([0,0,0])
screen.blit(button_start.image,(500,300))
screen.blit(y_button_start.image,(300,500))
screen.blit(x_button_start.image,(700,500))
pygame.display.update()
# -------------------------PARAMETERS----------------------------
buffer_wait = 0.5
download_time = 2
max_cycles = 8
cycles_sleep = 1
pos = [0,0]
nef_mode = True
smotor = 15
cali = calibrate_xy()
print(cali)
count_x = 0
count_y = 0
count_z = None
camera_x = 0
camera_y = 400 - camera_height
z_high = None
z_low = None
z_level = None
change = True
motor_mode = False
run_mode = False
canny_on = False
current_frame = None
grid_x = 50
grid_y = 50
b = [b5,b6,b7,b8,b9]
ce = 0
screen.fill([230,230,230])
lens = "4X"
project_name = ""
cam_bug_index = 0
shot_fail = False
############################### Positioning Gui Loop ###########################
while not done:

#------------------------ CAMERA COMMUNICATION ----------------
    clock.tick(60) #60fps
    
    try:
        check(gp.gp_camera_capture_preview(cam, fil, ctx))
        cData = ctypes.c_void_p()
        cLen = ctypes.c_ulong()
        check(gp.gp_file_get_data_and_size(fil, ctypes.byref(cData), ctypes.byref(cLen)))
        img = ctypes.string_at(cData.value, cLen.value)
        open('img1.jpg','wb').write(img)
        feed = pygame.image.load("img1.jpg")

    except:
        
        time.sleep(2)
        check(gp.gp_camera_exit(cam, ctx))
        time.sleep(2)
        check(gp.gp_camera_init(cam, ctx))
        time.sleep(2)
        check(gp.gp_camera_capture_preview(cam, fil, ctx))
        cData = ctypes.c_void_p()
        cLen = ctypes.c_ulong()
        check(gp.gp_file_get_data_and_size(fil, ctypes.byref(cData), ctypes.byref(cLen)))
        img = ctypes.string_at(cData.value, cLen.value)
        open('img1.jpg','wb').write(img)
        feed = pygame.image.load("img1.jpg")


    if  canny_on:
        frame = cv2.imread('img1.jpg',0)
        canny = cv2.Canny(frame,canny1_list[canny1_index],canny2_list[canny2_index])
        hist = cv2.calcHist(canny,[0],None,[2],[0,256])
        
        cv2.imwrite('canny.jpg',canny)
        feed = pygame.image.load("canny.jpg")
        preview_button.update("CANNY: "+str(int(hist[1])))
#------------------------------ RUN MODE -------------------------------
    if run_mode:
        if go_to:
            pass
        else:
            
            eadge = []
            os.chdir("/home/pi/green/")
            while (count_z - z_step) > 0:
               
                try:
                    check(gp.gp_camera_capture_preview(cam, fil, ctx))
                    cData = ctypes.c_void_p()
                    cLen = ctypes.c_ulong()
                    check(gp.gp_file_get_data_and_size(fil, ctypes.byref(cData), ctypes.byref(cLen)))
                    img = ctypes.string_at(cData.value, cLen.value)
                    open('img1.jpg','wb').write(img)
                    feed1 = pygame.image.load("img1.jpg")

                except:
        
                    time.sleep(2)
                    check(gp.gp_camera_exit(cam, ctx))
                    time.sleep(2)
                    check(gp.gp_camera_init(cam, ctx))
                    time.sleep(2)
                    check(gp.gp_camera_capture_preview(cam, fil, ctx))
                    cData = ctypes.c_void_p()
                    cLen = ctypes.c_ulong()
                    check(gp.gp_file_get_data_and_size(fil, ctypes.byref(cData), ctypes.byref(cLen)))
                    img = ctypes.string_at(cData.value, cLen.value)
                    open('img1.jpg','wb').write(img)
                    feed1 = pygame.image.load("img1.jpg")
                frame = cv2.imread('img1.jpg',0)
                screen.blit(feed1, (20,40))
                canny = cv2.Canny(frame,canny1_list[canny1_index],canny2_list[canny2_index])
                hist = cv2.calcHist(canny,[0],None,[2],[0,256])
                cv2.imwrite('canny.jpg',canny)
                feed = pygame.image.load("canny.jpg")
                screen.blit(feed, (20,b1))
                hist = cv2.calcHist(canny,[0],None,[2],[0,256])
                eadge.append(int(hist[1]))
                motor.focus_down(z_step)
                count_z -= z_step
                pygame.display.update()

            check(gp.gp_camera_exit(cam, ctx))
            logging.info(("Starting run x {} | y {}!".format(str(grid_index_x),str(grid_index_y))))
            s_count = 0
            time.sleep(1)
            for i,e in enumerate(eadge[::-1]):

                if e > threshold:
                    s_count +=1
                    logging.info("SHOT! Position:{}|Canny{}".format(i,e))
                    

                    for button in label_list:
                        #Configure this boolean for control flow later
                        shot_fail = False
                        #this is the basic photo process
                        dslr(cam_iso(button.value[1]))
                        time.sleep(0.3)
                        dslr(cam_shutter(button.value[0]))
                        time.sleep(0.3)
                        dslr(trigger)
                        time.sleep(float(button.value[0].replace("s",""))*2)
                        d1 = time.time()
                        shot_time.append(d1)
                        time.sleep(img_list[img_index][2])
                        #Now we validate if the shot is in the camera memory
                        #We compare the count of shots in the program to the amount found un the folder that stores the images on the camera
                        shot_n = len(shot_canny)
                        #every 999 photos the nikon D3200 creates a new directory, this needs a quick fix
                        cam_bug_index = math.floor(shot_n/999)
                        #look refers to images found in camera file
                        look = files_num(cam_bug_index)
                        #look2 refers to count in the program
                        look2 = (shot_n%999)
                        #these lines are just so there is no problem on file 999.
                        if look2 == 0:
                            look2 = 999
                        else:
                            cam_bug_index = math.floor(shot_n/999)

                        logging.info("CAM/REG -- {}/{}".format(look,look2))
                        # A cicles count for validating the photo in the camera
                        check_cycles = 0
                        #validation loop if the file has not been found on the camera yet, if more than max_cycles ocure an error is raised
                        while look != look2:
                            time.sleep(img_list[img_index][2])
                            look = files_num()
                            look2 = len(shot_canny)
                            
                            logging.info("CHECK CICLE {} -- {}/{}".format(check_cycles,look,look2))
                            check_cycles += 1
                            t2 = time.time()
                            dt = d2-d1
                            
                            if check_cycles > max_cycles:
                            
                                logging.warning("Faliure in shot x{}|y{}|z{}|s{}|i{}, removing from csv, total = {}".format(grid_index_x,grid_index_y,i,button.value[0],button.value[1],total_err))
                                total_err +=1
                                shot_fail = True
                                break
                        #If nothing happened update the data of the run.
                        if not shot_fail:
          
                            shot_canny.append(e)
                            shot_z_pos.append(i)
                            shot_iso.append(button.value[1])
                            shot_shutter.append(button.value[0])
                            shot_grid_x.append(grid_index_x)
                            shot_grid_y.append(grid_index_y)
                            shot_dt.append(dt)
                            shot_time.append(d1)
                            camera_files  = subprocess.check_output(['gphoto2','--list-files'], universal_newlines = True)
                            expression = r"DSC_........"
                            run_files = re.findall(expression,camera_files)
                            d = {"name":run_files,"grid_x":shot_grid_x,"grid_y":shot_grid_y, "z_pos":shot_z_pos, "canny":shot_canny,\
                                 "iso":shot_iso, "shutter":shot_shutter,"dt":shot_dt,"time":shot_time}
                            df = pd.DataFrame(data=d)
                            df.to_csv(project_name+".csv")
                            
                            
                    motor.focus_up(z_step)
                    count_z += z_step

                else:
                    motor.focus_up(z_step)
                    count_z += z_step

            logging.info("{} Shots in x {}| y {} total camera frames = {}".format(grid_index_x,grid_index_y,s_count,(s_count * len(label_list))))
            
            if ((grid_index_y + 2)%2) == 0:

                if grid_index_x == (grid_cols - 1):
                
                    if grid_index_y == (grid_rows - 1):
                        run_mode = False

                        logging.info("TOTAL FILES IN CAMERA MEMORY={}".format(len(run_files)))
                        logging.info("FILES REGISTERED IN CSV ={}".format(len(shot_grid_x)))
                        logging.info('ENDING')
                        check(gp.gp_camera_exit(cam, ctx))
                        sys.exit()
                    else:

                        grid_index_y += 1
                        
                        

                else:
                    grid_index_x += 1
                    
            else:
                if grid_index_x == 0:
                
                    if grid_index_y == (grid_rows - 1):
                        run_mode = False

                        logging.info("TOTAL FILES IN CAMERA MEMORY={}".format(len(run_files)))
                        logging.info("FILES REGISTERED IN CSV ={}".format(len(shot_grid_x)))
                        logging.info('ENDING')
                        check(gp.gp_camera_exit(cam, ctx))
                        sys.exit()
                    else:

                        grid_index_y += 1
                        
                        

                else:
                    grid_index_x -= 1

            # updating go_to x and y       
            for block in block_list:
                
                if block.index_y == grid_index_y:
                    if block.index_x == grid_index_x:
                        go_to = True
                        block.image.fill((50,255,50))
                        go_to_x = block.x
                        go_to_y = block.y
                        
  



#-------------------------- EVENT HANDLING -------------------------

    keys=pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check(gp.gp_camera_exit(cam, ctx))
            sys.exit()
    x_step = x_step_list[x_step_index]
    y_step = y_step_list[y_step_index]
    z_step = z_step_list[z_step_index]
    x = motor.button_x()
    y = motor.button_y()
    if count_x != 0:
        camera_x = round(count_x/25)
    if count_y != 0: 
        camera_y = 400 - camera_height - round(count_y/25)
    if z_level != None:
        if z_high != None:
            z_level = 20 + round(350*((z_high - count_z)/z_high))


    if x or y:
        go_to = False
        if keys[pygame.K_RIGHT]:
            motor.small_up(smotor)
            count_x = count_x + smotor
            motor_mode = True

        elif keys[pygame.K_UP]:
            motor.small_right(smotor)
            count_y = count_y + smotor
            motor_mode = True

    elif count_x > 8400 or count_y > 8400:
        print("YOU HIT AND EADGE")
        go_to = False
        if keys[pygame.K_LEFT]:
            motor.small_down(smotor)
            count_x = count_x - smotor
            motor_mode = True

        elif keys[pygame.K_DOWN]:
            motor.small_left(smotor)
            count_y = count_y - smotor
            motor_mode = True

            
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            motor.small_bottom_left(smotor)
            count_x = count_x - smotor
            count_y = count_y - smotor
            motor_mode = True
#--------------------------- GO TO MODE ----------------------
    elif go_to :
        motor_mode = True
        if go_to_x > camera_x:
            motor.small_up(5)
            count_x = count_x + 5
        if go_to_x < camera_x:
            motor.small_down(5)
            count_x = count_x - 5
        if go_to_y < camera_y:
            motor.small_right(5)
            count_y = count_y + 5
        if go_to_y > camera_y:
            motor.small_left(5)
            count_y = count_y - 5
        if go_to_x == camera_x and go_to_y == camera_y:
            go_to = False
#-------------------- MOTOR EVENTS WITH BUTTON SECURITY ---------------

# -------------------------------MOTOR EVENTS -------------------------------------
    else:
        if keys[pygame.K_w] and z_low != None:
            motor.focus_up(z_step)
            motor_mode = True
            count_z += z_step


        elif keys[pygame.K_w]:
            motor.focus_up(z_step)
            motor_mode = True


        elif keys[pygame.K_s] and z_low != None:
            if (count_z - z_step) > 0:
                motor.focus_down(z_step)
                motor_mode = True
                count_z -= z_step
             
        elif keys[pygame.K_s]:
                motor.focus_down(z_step)
                motor_mode = True
                


        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            motor.small_bottom_left(smotor)
            count_x = count_x - smotor
            count_y = count_y - smotor
            motor_mode = True

   
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            motor.small_bottom_right(smotor)
            count_x = count_x - smotor
            count_y = count_y + smotor
            motor_mode = True

   
  
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            motor.small_top_right(smotor)
            count_x = count_x + smotor
            count_y = count_y + smotor
            motor_mode = True

            

        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            motor.small_top_left(15)
            count_x = count_x + smotor
            count_y = count_y - smotor
            motor_mode = True

   
        elif keys[pygame.K_UP]:
            motor.small_right(smotor)
            count_y = count_y + smotor
            motor_mode = True

          
        elif keys[pygame.K_DOWN]:
            motor.small_left(smotor)
            count_y = count_y - smotor
            motor_mode = True


        elif keys[pygame.K_LEFT]:
            motor.small_down(smotor)
            count_x = count_x - smotor
            motor_mode = True

        elif keys[pygame.K_RIGHT]:
            
            
            motor.small_up(smotor)
            count_x = count_x + smotor
            motor_mode = True


#---------------------BUTTON EVENTS --------------

# --------- GO TO MODULE------------
    if not motor_mode and not run_mode:
        x,y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for box in block_list:
            box.image.fill(box.color)   
            if box.rect.collidepoint((x - 749),(y - 65)): 
                box.image.fill((200,255,200))
                if click[0] == True and box.x < 400 and box.y < 400 and box.y > 0:
                    box.image.fill((50,255,50))
                    go_to_x = box.x
                    go_to_y = box.y
                    go_to = True
#--------------------PARAMETER BUTTONS ----------------------
        for button in button_list:
            button.image.fill(button.color)
            button.image.blit(button.textsurface,(button.text_x, button.text_y))   
            if button.rect.collidepoint(x,y): 
                button.image.fill(((button.color[0] - 50),(button.color[1] - 50),(button.color[2] - 50)))
                button.image.blit(button.textsurface,(button.text_x, button.text_y))  
                if click[0] == True:
                    button.image.fill(((button.color[0] - 50),(button.color[1]),(button.color[2] - 50)))
                    button.image.blit(button.textsurface,(button.text_x, button.text_y))

                    if button in label_list:
                        check(gp.gp_camera_exit(cam, ctx))
                        time.sleep(0.5)
                        dslr(clear)
                        time.sleep(0.5)
                        dslr(cam_img_size("3008x2000"))
                        time.sleep(0.5)
                        dslr(cam_iso(button.value[1]))
                        time.sleep(0.1)
                        dslr(cam_shutter(button.value[0]))
                        time.sleep(0.1)
                        dslr(trigger)
                        time.sleep(3)


                        dslr(download)
                        time.sleep(1)
                        


                        for filename in os.listdir("."):
                            if filename.endswith(".JPG"):
                                os.rename(filename,"preview.jpg")
                        preview_image = cv2.imread("preview.jpg")
                        hist_preview = cv2.cvtColor(preview_image,cv2.COLOR_RGB2GRAY)

                        fig, ax = plt.subplots( nrows=1, ncols=1 )
                        fig.set_size_inches(5,5)  
                        ax.hist(hist_preview.ravel(),256,[0,256])
                        ax.set_xlim([0,256])
                        
                        for tick in ax.yaxis.get_major_ticks():
                            tick.draw = lambda *args:None


                        fig.set_size_inches(5,5)    
                        fig.savefig('hist.png')
                        plt.close(fig)  
                        
                        s_preview = cv2.resize(preview_image,None,fx=0.20, fy=0.20, interpolation = cv2.INTER_CUBIC)

                        cv2.imwrite('preview.jpg',s_preview)
                        preview_1 = pygame.image.load("preview.jpg")
                        preview_1_hist = pygame.image.load('hist.png')
                        screen.fill((255,255,255))
                        
                        screen.blit(preview_1_hist,(700,100))
                        screen.blit(preview_1,(25,150))


                        
                        pygame.display.update()
                        wait = True
                        time.sleep(2)
                        while wait:
                            
                            if len(pygame.key.get_pressed()) > 0:
                                wait = False
                            
                        os.remove("preview.jpg")
                        os.remove('hist.png')
                   
                        
                    
                    if button == grid_cols_up and grid_cols_index != (len(grid_cols_list)-1):
                        grid_cols_index +=1
                        change = True
                    if button == grid_cols_down and grid_cols_index !=0:
                        grid_cols_index -=1
                        change = True
   
                    if button == grid_rows_up and grid_rows_index != (len(grid_rows_list)-1):
                        grid_rows_index +=1
                        change = True
                    if button == grid_rows_down and grid_rows_index != 0:
                        grid_rows_index -=1
                        change = True
        
                    if button == shutter_up and shutter_index != (len(shutter_list)-1):
                        shutter_index +=1
                        change = True
                    if button == shutter_down and shutter_index != 0:
                        shutter_index -=1
                        change = True
                
                    if button == iso_up and iso_index != (len(iso_list)-1):
                        iso_index +=1
                        change = True
                    if button == iso_down and iso_index != 0:
                        iso_index -=1
                        change = True
               
                    if button == img_up and img_index != (len(img_list)-1):
                        img_index +=1
                        change = True
                    if button == img_down and img_index != 0:
                        img_index -=1
                        change = True

                    if button == x_step_up and x_step_index != (len(x_step_list)-1):
                        x_step_index +=1
                        change = True
                    if button == x_step_down and x_step_index != 0:
                        x_step_index -=1
                        change = True

                    if button == y_step_up and y_step_index != (len(y_step_list)-1):
                        y_step_index +=1
                        change = True
                    if button == y_step_down and y_step_index != 0:
                        y_step_index -=1
                        change = True

                    if button == z_step_up and z_step_index != (len(z_step_list)-1):
                        z_step_index +=1
                        change = True
                    if button == z_step_down and z_step_index != 0:
                        z_step_index -=1
                        change = True

                    if button == canny1_up and canny1_index != (len(canny1_list)-1):
                        canny1_index +=1
                        change = True
                    if button == canny1_down and canny1_index != 0:
                        canny1_index -=1
                        change = True

                    if button == canny2_up and canny2_index != (len(canny2_list)-1):
                        canny2_index +=1
                        change = True
                    if button == canny2_down and canny2_index != 0:
                        canny2_index -=1
                        change = True
                        
                    if button == threshold_up and threshold_index != (len(threshold_list)-1):
                        threshold_index +=1
                        change = True
                    if button == threshold_down and threshold_index != 0:
                        threshold_index -=1
                        change = True
                        
                    if button == lowest_focus:
                        count_z = 0
                        z_low = 0
                        z_high = None
                        change = True

                    if button == highest_focus:
                        z_high = count_z
                        z_level = 30
                        change = True
                
                    if button == add_button:
                        
                        if ce < 5:
                            exposures.append([shutter_list[shutter_index],iso_list[iso_index]])
                            expo_label = Block((200,255,255),425,25, value = [shutter_list[shutter_index],iso_list[iso_index]],text = (" Exposure " + str(ce + 1) + "      Shutter: " + shutter_list[shutter_index] + "      Iso: " + iso_list[iso_index]),text_color = color2,text_x = 3, text_y = 3,font_size = label_font)
                            expo_label.rect.x = 280
                            expo_label.rect.y = b[ce]
                            button_list.add(expo_label)
                            label_list.add(expo_label)
                            ce +=1
                            change = True


                    if button == exposure_clear:
 
                        del exposures
                        exposures = []
                        for sprite in label_list:
                            sprite.kill()
                            del sprite
                        ce = 0
                        change = True

                    if button == grid_set:
                        grid_x = camera_x
                        grid_y = camera_y
                        change = True

                    if button == orientation_button:
                        
                        camera_height,camera_width = camera_width, camera_height
                        camera = pygame.surface.Surface((camera_width,camera_height))
                        camera.fill((0,0,255))
                        camera.set_alpha(80)
                        change = True

                    if button == preview_button:
                        canny_on = True
                   
                    if button == project_name_disp:
                        text_finished = False

                        while not text_finished:
                            keys=pygame.key.get_pressed()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        text_finished = True
                                    elif event.key == pygame.K_BACKSPACE:
                                        text = text[:-1]
                                        project_name_disp.update("PROJECT NAME:  " + text)
                                        project_name = text
                                    else:
                                        text += event.unicode      
                                        project_name_disp.update("PROJECT NAME:  " + text)
                                        project_name = text            
                            screen.blit(project_name_disp.image,(280,b1))
                            pygame.display.update()
                    if button == preview_all and len(label_list) != 0:

                        

                        relative_height = math.floor((screen_height - 200)/len(label_list))
                        relative_width = math.floor(relative_height*1.5)
                        pc = 0
                        col = ["r", "g", "b","black","grey","orange","purple"]
                        col_rgb = [(255,0,0),(0,255,0),(0,0,255),(0,0,0),(100,100,100),(255,200,120),(255,100,255)]

                        check(gp.gp_camera_exit(cam, ctx))
                        time.sleep(0.5)
                        dslr(clear)
                        time.sleep(0.5)
                        dslr(cam_img_quality("JPEG Basic"))
                        time.sleep(0.3)
                    
                        dslr(cam_img_size("3008x2000"))
                        dslr(cam_img_quality("JPEG Basic"))       

                        time.sleep(2)
                        
                        for button in label_list:
                            
                            
                            time.sleep(0.3)
                            dslr(cam_img_size("3008x2000"))
                            time.sleep(0.5)
                            dslr(cam_iso(button.value[1]))
                            time.sleep(0.3)
                            dslr(cam_shutter(button.value[0]))
                            time.sleep(0.3)
                            dslr(trigger)
                            time.sleep(2)
                            
                        time.sleep(5)
                        dslr(download)
                        
                        fig, ax = plt.subplots( nrows=1, ncols=1 )
                        fig.set_size_inches(5,5) 
                        ax.set_xlim([0,256])
                        screen.fill((255,255,255))
                        
                        for filename in os.listdir("."):
                            if filename.endswith(".JPG"):
                                os.rename(filename,("preview.jpg"))
                                preview_image = cv2.imread("preview.jpg")
                                hist_preview = cv2.cvtColor(preview_image,cv2.COLOR_RGB2GRAY)
                                ax.plot(cv2.calcHist([hist_preview],[0],None,[256],[0,256]),color = col[pc])
                                s_preview = cv2.resize(preview_image,(relative_width,relative_height), interpolation = cv2.INTER_CUBIC)
                                cv2.imwrite('preview.jpg',s_preview)
                                time.sleep(0.5)
                                preview_feed = pygame.image.load("preview.jpg")
                             
                                id_label = Block(col_rgb[pc],relative_width,25, text = (" Exposure " + str(pc + 1) ),text_color = color2,text_x = 3, text_y = 3,font_size = label_font)
                                
                                screen.blit(preview_feed,(25,(50 + pc*relative_height)))
                                screen.blit(id_label.image,(25,(50 + pc*relative_height)))
                                os.remove("preview.jpg")
                                pc += 1
                        
                        
                        for tick in ax.yaxis.get_major_ticks():
                            tick.draw = lambda *args:None


                        fig.set_size_inches(5,5)    
                        fig.savefig('hist.png')
                        plt.close(fig)  
                        
                        preview_hist = pygame.image.load('hist.png')
                        
                        
                        screen.blit(preview_hist,(700,100))
                        


                        os.remove('hist.png')
                        pygame.display.update()

                        time.sleep(15)

                        


#-----------------------------------------------------------------------------------------------------                  
                    if button == run_button:
                        if len(exposures) > 0 and z_high !=None and project_name != "":
                            logging.basicConfig(filename=(project_name +'.log'),level=logging.DEBUG)
                            check(gp.gp_camera_exit(cam, ctx))
                            time.sleep(0.5)
                            dslr(clear)
                            time.sleep(2)
                            dslr(cam_img_quality(img_quality))
                            time.sleep(0.3)
                            if img_quality != "NEF (Raw)":
                                dslr(cam_img_size(img_size))
                                
                            project_start = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
                            total_err = 0
                            debug_list = []
                            shot_time = []
                            shot_canny = []
                            shot_z_pos = []
                            shot_iso = []
                            shot_shutter = []
                            shot_lens = []
                            shot_grid_x = []
                            shot_grid_y = []
                            shot_x = []
                            shot_y = []
                            shot_id = []
                            shot_z_step = []
                            shot_dt = []
                            go_to = True
                            while count_z < z_high:
                                motor.focus_up(1)
                                count_z += 1

                            grid_index_x = 0
                            grid_index_y = 0
                            grid_end = (grid_rows + 2)%2
                            run_mode = True
                            

                            for block in block_list:
                
                                if block.index_y == grid_index_y:
                                    if block.index_x == grid_index_x:
                                        go_to = True
                                        block.image.fill((50,255,50))
                                        go_to_x = block.x
                                        go_to_y = block.y
             
                    if button == reset_button:
                        canny_on = False
                        preview_button.update("Canny")
                        

    if change:
        grid_cols_disp.update("Cols:    " +str(grid_cols_list[grid_cols_index]))
        grid_rows_disp.update("Rows:    " +str(grid_rows_list[grid_rows_index]))
        shutter_disp.update("Shutter: " +shutter_list[shutter_index])
        iso_disp.update("Iso:     " +iso_list[iso_index])
        img_disp.update("Image Q:    " +(str(img_list[img_index][0] + img_list[img_index][1])))
        x_step_disp.update("Overlap: " +str(x_step_list[x_step_index]))
        y_step_disp.update("CAM:  " +str(y_step_list[y_step_index]))
        z_step_disp.update("Z Step:  " +str(z_step_list[z_step_index]))
        canny1_disp.update("Canny1:  " +str(canny1_list[canny1_index]))
        canny2_disp.update("Canny2:  " +str(canny2_list[canny2_index]))
        threshold_disp.update("Treshold: " +str(threshold_list[threshold_index]))

#------------------------------------------------------------------------



        


        for sprite in all_sprites_list:
            sprite.kill()
            del sprite

        
#------------------------------------------------------------------------
        camera_width = (y_step_list[y_step_index])
        camera_height = round((camera_width*2)/3)
        stride_x = round(camera_width * ((x_step_list[x_step_index])/100))
        stride_y = round(camera_height - (camera_width - stride_x))      
        camera = pygame.surface.Surface((camera_width,camera_height))
        camera.fill((0,0,255))
        img_quality = img_list[img_index][0]
        img_size = img_list[img_index][1]
        camera.set_alpha(80)
        threshold = threshold_list[threshold_index]
        grid_cols = (grid_cols_list[grid_cols_index])
        grid_rows =  (grid_rows_list[grid_rows_index])
#def criachuva(pos_x, pos_y,x_motor,y_motor,frame_width,frame_height,cols,rows):
        grid_create(grid_x,grid_y,stride_x,stride_y,camera_width,camera_height,grid_cols,grid_rows)
        

#----------------------- BLITING --------------------
          
    
    if z_level != None:
        h_scale.fill([255,255,255])
        h_scale.blit(camera_high,(0,0))
        h_scale.blit(camera_low,(0,380))
        h_scale.blit(camera_level,(0,z_level))
    screen.fill((230,230,230))
    nav.blit(camera,(camera_x,camera_y))   
    nav_border.blit(h_scale,(450,25))

    nav_x_count.update("X:"+str(count_x))
    nav_y_count.update("Y:"+str(count_y))
    nav_z_count.update("Z:"+str(count_z))
    nav_border.blit(nav_x_count.image,(125,425))
    nav_border.blit(nav_y_count.image,(250,425))
    nav_border.blit(nav_z_count.image,(375,425))

    for label in label_list:
        screen.blit(label.image,(label.rect.x,label.rect.y))

    nav.fill((255,255,255))
    all_sprites_list.draw(nav)
    nav.blit(camera,(camera_x,camera_y))
    nav_border.blit(h_scale,(450,25))
    nav_border.blit(nav,(25,25))
    screen.blit(feed, (20,40))
    screen.blit(nav_border,(barrier,40))
    
    
 
    if not run_mode:

        screen.blit(grid_cols_disp.image, (barrier,b1))
        screen.blit(grid_cols_down.image, ((barrier + 185),b1))
        screen.blit(grid_cols_up.image, ((barrier + 220),b1))
    

    
        screen.blit(grid_rows_disp.image, (barrier,b2))
        screen.blit(grid_rows_down.image, ((barrier + 185),b2))
        screen.blit(grid_rows_up.image, ((barrier +220),b2))


    
        screen.blit(shutter_disp.image, ((barrier+260),b2))  
        screen.blit(shutter_down.image, ((barrier + 185 + 260),b2))
        screen.blit(shutter_up.image, ((barrier +220 + 260) ,b2))


        screen.blit(iso_disp.image, (barrier + 260,b1))
        screen.blit(iso_down.image, ((barrier + 185 + 260),b1))
        screen.blit(iso_up.image, ((barrier + 220 + 260 ),b1))


        screen.blit(img_disp.image, (barrier,b6))
        screen.blit(img_down.image, ((barrier + 185),b6))
        screen.blit(img_up.image, ((barrier + 220),b6))
 

        screen.blit(x_step_disp.image, (barrier,b3))
        screen.blit(x_step_down.image, ((barrier +185),b3))
        screen.blit(x_step_up.image, ((barrier + 220),b3))
    

        screen.blit(y_step_disp.image, (barrier,b4))
        screen.blit(y_step_down.image, ((barrier+185),b4))
        screen.blit(y_step_up.image, ((barrier + 220),b4))


        screen.blit(z_step_disp.image, (barrier ,b5))
        screen.blit(z_step_down.image, ((barrier + 185),b5))
        screen.blit(z_step_up.image, ((barrier + 220),b5))
    

        screen.blit(canny1_disp.image, (barrier ,b7))
        screen.blit(canny1_down.image, ((barrier + 185),b7))
        screen.blit(canny1_up.image, ((barrier + 220),b7))

        screen.blit(canny2_disp.image, (barrier ,b8))
        screen.blit(canny2_down.image, ((barrier + 185),b8))
        screen.blit(canny2_up.image, ((barrier + 220),b8))

        screen.blit(threshold_disp.image, (barrier ,b9))
        screen.blit(threshold_down.image, ((barrier + 185),b9))
        screen.blit(threshold_up.image, ((barrier + 220),b9))

        
        screen.blit(add_button.image, (barrier + 260,b3))


        screen.blit(grid_set.image, ((barrier + 260),b6))

    
        screen.blit(lowest_focus.image, ((barrier + 260 ),b8))
   
    
        screen.blit(highest_focus.image, ((barrier + 260 ),b7))

        screen.blit(exposure_clear.image, ((barrier + 260 ),b5))

        screen.blit(preview_all.image, ((barrier + 260 ),b4)) 
    
        screen.blit(run_button.image, (20,b4))

    
        screen.blit(preview_button.image, (20,b1))


        screen.blit(reset_button.image, (150,b4))

    
        screen.blit(orientation_button.image, (150,b1))
        screen.blit(project_name_disp.image,(280,b1))
        screen.blit(run_label.image, (280,b2))
   
        screen.blit(run_label1.image, (280,b3))

        screen.blit(run_label2.image, (280,b4))
   
    change = False
    motor_mode = False
    pygame.display.update()

        
