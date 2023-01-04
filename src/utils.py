import cv2 # OpenCV
import numpy as np
import matplotlib.pyplot as plt
import os
import numpy as np

'''
生成大坝的黑白背景并随机生成噪声
'''

def add_small(w, h):
          root_path = '../noise/small'
          files_list = os.listdir(root_path)
          n = len(files_list)
          k = np.random.randint(0, n)
          img = cv2.imread(os.path.join(root_path, files_list[k]), 0)
          img = cv2.resize(img, (h, w))
          return img

def add_big(w, h):
          root_path = '../noise/big'
          files_list = os.listdir(root_path)
          n = len(files_list)
          k = np.random.randint(0, n)
          img = cv2.imread(os.path.join(root_path, files_list[k]), 0)
          img = cv2.resize(img, (h, w))
          return img

def get_xy(w, h, w1, h1):
          a = w - w1 - 1
          b = h - h1 - 1
          x = np.random.randint(0, a)
          y = np.random.randint(0, b)
          return x, y

def add_noise(img):
          '''
          函数功能: 为img添加噪声
          img: 输入图像
          '''
          w = img.shape[1]
          h = img.shape[0]
          # 小噪点添加
          count = np.random.randint(10, 200)
          for _ in range(0, count):
                    w1 = np.random.randint(5, 10)
                    h1 = np.random.randint(5, 10)
                    x, y = get_xy(w, h, w1, h1)
                    img[x:x+w1, y:y+h1] = add_small(w1, h1)
          # 方形噪声添加
          count = np.random.randint(1, 5)
          for _ in range(0, count):
                    w1 = np.random.randint(20, 40)
                    h1 = np.random.randint(20, 40)
                    x, y = get_xy(w, h, w1, h1)
                    img[x:x+w1, y:y+h1] = add_small(w1, h1)
          # 长形噪声添加
          count = np.random.randint(1, 5)
          for _ in range(0, count):
                    w1 = np.random.randint(5, 10)
                    h1 = np.random.randint(20, 40)
                    x, y = get_xy(w, h, w1, h1)
                    img[x:x+w1, y:y+h1] = add_small(w1, h1)
          # 扁形噪声添加
          count = np.random.randint(1, 5)
          for _ in range(0, count):
                    w1 = np.random.randint(20, 40)
                    h1 = np.random.randint(5, 10)
                    x, y = get_xy(w, h, w1, h1)
                    img[x:x+w1, y:y+h1] = add_small(w1, h1)
          return img

def add_obj(background, img, x, y):
    ''''
    函数功能:将裂缝img融合到background上去
    background: 背景图像
    img: 要融合的裂缝图像
    x,y: 要融合到的位置
    '''
    bg = background.copy()
    h_bg, w_bg = bg.shape[0], bg.shape[1]
    h, w = img.shape[0], img.shape[1]
    # Calculating coordinates of the top left corner of the object image to the background
    x_tl = x - int(w/2)
    y_tl = y - int(h/2)    
    # Calculating coordinates of the bottom right corner of the object image to the background
    x_br = x + int(w/2)
    y_br = y + int(h/2)

    w1 = x_br - x_tl
    h1 = y_br - y_tl
    
    if (x_tl >= 0 and y_tl >= 0) and (x_br < w_bg and y_br < h_bg):
        # bg[y_tl:y_br, x_tl:x_br] = img[0:h1, 0:w1]
        a = bg[y_tl:y_br, x_tl:x_br]
        b = img[0:h1, 0:w1]
        c = np.where(b>50, b, a)
        bg[y_tl:y_br, x_tl:x_br] = c
        bg[bg>50] = 255
        bg[bg<=50] = 0
        return bg, x_tl, y_tl, x_br, y_br
    else:
        return None

def random_xy(a, b, c, d):
    '''
    随机产生一个坐标(x, y): a <= x <= b, c <= y <= d
    '''
    return (np.random.randint(a, b), np.random.randint(c, d))

def max_min(bg_size, tg_size):
    '''
    生成可以随机粘贴的位置范围(a, b, c, d)
    bg_size : 大的(x, y)
    tg_size : 小的(x, y)
    '''
    a = int((tg_size[0])/2) + 1
    b = int(bg_size[0] - (tg_size[0])/2) - 1
    c = int((tg_size[1])/2) + 1
    d = int(bg_size[1] - (tg_size[1])/2) - 1
    return a, b, c, d

def random_center(bg_size, tg_size):
    a, b, c, d = max_min(bg_size, tg_size)
    return random_xy(a, b, c, d)


def get_newsize(w1, h1, w, h):
    '''
    不使用随机resize,加以限制
    防止裂缝过宽
    '''
    ratio = h1/w1
    w2 = w1
    h2 = h1
    if ratio < 3/4:
        w2 = np.random.randint(150, w-10)
        h2 = np.random.randint(h1, min(h1+50, h-10))
        return w2, h2
    
    if ratio > 4/3:
        h2 = np.random.randint(150, h-10)
        w2 = np.random.randint(w1, min(w1+50, w-10))
        return w2, h2
    
    if np.random.random()>0.5:
        w2 = np.random.randint(150, w-10)
    else:
        h2 = np.random.randint(150, h-10)

    if np.random.random()<0.1:
        w2 = w1
        h2 = h1
    return w2, h2

def merge_two(dec1, dec2):
    '''
    判断两box是否重叠, 返回融合之后的box坐标
    '''
    x01, y01, x02, y02 = dec1
    x11, y11, x12, y12 = dec2
 
    lx = abs((x01 + x02) / 2 - (x11 + x12) / 2)
    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
    sax = abs(x01 - x02)
    sbx = abs(x11 - x12)
    say = abs(y01 - y02)
    sby = abs(y11 - y12)
    if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:
        return (min(x01, x11), min(y01, y11), max(x02, x12), max(y02, y12))
    else:
        return None
    
def merge_all(dectors):
    decs = dectors.copy()
    flag = 1
    while flag==1:
        flag = 0
        n = len(decs)
        for i in range(n-1):
            dec_new = merge_two(decs[i], decs[i+1])
            if dec_new is not None:
                flag = 1
                a = decs[i]
                b = decs[i+1]
                decs.remove(a)
                decs.remove(b)
                decs.append(dec_new)
                break
    return decs
