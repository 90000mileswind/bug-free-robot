#用于读取kfb格式数据转化为普通jpg图片,并能把坐标转化回来
import kfbreader.kfbReader as kfbReader
import cv2
import json
import os
import random

#参数设置,这个scale是kfbReader的缩放倍数，影响清晰度
scale = 20
num_line = 0


#使roi和pos区域一一对应
def roi_pos(roi_box1,pos_box):
    list = []
    [list.append(i) for i in roi_box1 if not i in list]
    roi_box = list
    pos_box_3d = [0] * len(roi_box)
    for i, roi in enumerate(roi_box):
        for j in pos_box:
            if 0 <= j[0] - roi[0] <= roi[2] - j[2] and 0 <= j[1] - roi[1] <= roi[3] - j[3]:
                if pos_box_3d[i] == 0:
                    pos_box_3d[i] = [[j[0], j[1], j[2], j[3]]]
                else:
                    pos_box_3d[i].append([j[0], j[1], j[2], j[3]])
    k = len(pos_box_3d) - 1
    while k >= 0:
        if pos_box_3d[k] == 0:
            del pos_box_3d[k]
            del roi_box[k]
        k -= 1
    return roi_box, pos_box_3d

#函数接收load_list，返回roi_box,pos_box两个列表
def roi_for_pos(load_list):
    roi_box = []
    pos_box = []
    for box in load_list:
        if box['class'] == 'roi':
            roi_box.append([box['x'], box['y'], box['w'], box['h']])
        if box['class'] == 'pos':
            pos_box.append([box['x'], box['y'], box['w'], box['h']])
    return roi_box,pos_box

#函数返回4个随机数r_w,r_h,r_x,r_y
def _random_4(a,b):
    r_w = random.randint(500, 1000)  # 取一个随机数作宽random.randint(500, 1000)
    r_h = random.randint(500, 1000)  # 取一个随机数作高random.randint(500, 1000)
    while a>=r_w:
        r_w += 200
    while b>=r_h:
        r_h += 200
    r_x = random.randint(a, r_w)
    r_y = random.randint(b, r_h)
    return r_w,r_h,r_x,r_y

#函数划分属于这个区域的pos_s(还是原来的pos重分一下) roi[x,y,w,h]
#pos_s变成[xmin,ymin,xmax,ymax]
def pos2_6c(roi_box,pos_box,pos_boxold):
    roi_s = []
    for i in range(len(pos_box)):
        for k in range(len(pos_box[i])):
            w,h,a,b = _random_4(pos_box[i][k][2],pos_box[i][k][3])
            x = pos_box[i][k][0]-a
            y = pos_box[i][k][1]-b
            if x<roi_box[i][0]:
                x=roi_box[i][0]
            if y<roi_box[i][1]:
                y=roi_box[i][1]
            if x+w>roi_box[i][0]+roi_box[i][2]:
                x=roi_box[i][0]+roi_box[i][2]-w
            if y+h>roi_box[i][1]+roi_box[i][3]:
                y=roi_box[i][1]+roi_box[i][3]-h
            roi_s.append([x,y,w,h])
    roi_s,pos_s = roi_pos(roi_s,pos_boxold)
    for m in range(len(pos_s)):
        for j in range(len(pos_s[m])):
            pos_s[m][j][0] -= roi_s[m][0]
            pos_s[m][j][1] -= roi_s[m][1]
            pos_s[m][j][2] += pos_s[m][j][0]
            pos_s[m][j][3] += pos_s[m][j][1]
    return roi_s,pos_s

#切割大图片为小jpg图片同时写入txt。接收的img_name是'T2019_53.kfb'这样的
def write_img(img_name, path_file,distribution):
    global num_line#引用全局变量
    # 实例化reader类
    read = kfbReader.reader()
    path = path_file +'\\'+ img_name
    kfbReader.reader.ReadInfo(read, path, scale, True)
    #先读取json文件内容
    with open(r"E:\AI_project\yolov3_tianchi\data\labels\\"+img_name[:-3]+"json", 'r') as load_f:
        load_list = json.load(load_f)                #获取json文件内容
        roi_box, pos_box = roi_for_pos(load_list) #生成roi和pos
        roi_box, pos_box_3d = roi_pos(roi_box, pos_box)#生成roi和pos对应的两个列表
        roi_box, pos_box = pos2_6c(roi_box, pos_box_3d, pos_box)       #pos的四个坐标变为（xmin,ymin,xmax,ymax,1,0）
        for i, roi in enumerate(roi_box):
            # 读取ROI区域
            roi_m = read.ReadRoi(roi[0], roi[1], roi[2], roi[3], scale)
            str_num_line = str(num_line)+' '
            num_line += 1
            img = '.\\data\\images\\' + distribution + '\\' + img_name[:-4] + '_' + str(roi[0]) + '_' + str(roi[1]) + '_' + str(num_line) + '.jpg'
            cv2.imwrite(img, roi_m)  # 按地址写入图片
            img_widthandhight = ' {} {}'.format(roi[2], roi[3])
            box_info = ''
            for k in pos_box[i]:
                box_info += ' {} {} {} {} {}'.format(int(0), int(k[0]), int(k[1]), int(k[2]), int(k[3]))
            with open('./data/my_data/' + distribution + '.txt', 'a') as f:
                f.write('\n')#换行
                f.write(str_num_line)#行序号
                f.write(img)  # 图片地址
                f.write(img_widthandhight)#这里写入宽和高
                f.write(box_info)#类别，xmin,ymin,xmax,ymax


#读取所有pos_i文件夹内所有kfb文件
path_all = r'E:\img_data\pos_'
for n in range(10):#数字1先遍历50张图片
    path_file = path_all+str(n)
    if n<=7:
        distribution = 'train'
    elif n==8:
        num_line = 0
        distribution = 'val'
    else:
        num_line = 0
        distribution = 'test'
    for file in os.listdir(path_file):
        write_img(file,path_file,distribution)#file是一个个'T2019_53.kfb'这样的文件，把第一个for中的数字改成10就可以遍历500张图


