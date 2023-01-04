import cv2 # OpenCV
import numpy as np
import matplotlib.pyplot as plt
import os
from create_xml import create
from utils import *


'''
生成多裂缝图像样本
'''

root_path = '../data'
save_img_dir = '../crack/img/'
save_lable_dir = '../crack/label/'

files_list = os.listdir(root_path)

result_name = 'img'

# 背景大小默认1024*1024
w, h = 1024, 1024
bg_size = (w, h)

k = 1 # 以当前裂缝为基础生成图像的个数
cnt = 0 # 生成的图像个数计数

n = len(files_list)
for img_name in files_list:
    #  get current crack
    img = cv2.imread(os.path.join(root_path, img_name), 0)

    # generate background
    bg = np.zeros((h, w))
    bg = bg.astype(np.uint8)

    for i in range(k):
        background = bg.copy()
        img1 = img.copy()
        
        # 翻转变换
        fz = np.random.randint(0, 5)

        if i <= 4:
            fz = i
        
        if fz == 1:
            img1 = cv2.transpose(img1)
        if fz == 2:
            img1 = cv2.flip(img1, 0)
        if fz == 3:
            img1 = cv2.flip(img1, 1)
        if fz == 4:
            img1 = cv2.flip(img1, -1)
        

        h1, w1 = img1.shape[0], img1.shape[1]
            
        # resize crack
        w2, h2 = get_newsize(w1, h1, w, h)
        new_size = (w2, h2)
        img1 = cv2.resize(img1, new_size)

        # generate the adding center
        center = random_center(bg_size, new_size)

        # add crack to background
        result = add_obj(background, img1, center[0], center[1])
        
        dectors = []
        if result is not None:
            merge_img = result[0]
            tg_loca = (result[1], result[2], result[3], result[4])
            dectors.append(tg_loca)
            k1 = np.random.randint(1, 5)
            if i <= 4:
                k1 = 0
            for _ in range(k1):
                j = np.random.randint(0, n)
                img2 = cv2.imread(os.path.join(root_path, files_list[j]), 0)
                h3, w3 = img2.shape[0], img2.shape[1]
                # resize crack
                w4, h4 = w2, h2 = get_newsize(w3, h3, w, h)
                new_size1 = (w4, h4)
                img2 = cv2.resize(img2, new_size1)

                # generate the adding center
                center = random_center(bg_size, new_size)

                # add crack to background
                result = add_obj(merge_img, img2, center[0], center[1])

                if result is None:
                    continue
                
                merge_img = result[0]
                tg_loca = (result[1], result[2], result[3], result[4])
                dectors.append(tg_loca)
        
        # if result is not None:
        
        cnt += 1
        img_name = result_name + str(cnt) + '.jpg'
        merge_img = add_noise(merge_img)
        merge_img[merge_img < 50] = 0
        merge_img[merge_img >= 50] = 255
        cv2.imwrite(save_img_dir + img_name, merge_img)
        decs = merge_all(dectors)
        create(save_lable_dir, img_name, bg_size, len(decs), decs)
        # print(i, end=',')
    
    # a = 0
    # assert a == 1