#from xml.etree import ElementTree as  etree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree
from xml.dom import minidom

'''
生成对应的label，也就是xml文件
'''


# elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
def prettyXml(element, indent, newline, level = 0):
    # 判断element是否有子元素
    if element:
        # 如果element的text没有内容      
        if element.text == None or element.text.isspace():     
            element.text = newline + indent * (level + 1)      
        else:    
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)    
    # 此处两行如果把注释去掉，Element的text也会另起一行 
    #else:     
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level    
    temp = list(element) # 将elemnt转成list    
    for subelement in temp:    
        # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
        if temp.index(subelement) < (len(temp) - 1):     
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个    
            subelement.tail = newline + indent * level   
        # 对子元素进行递归操作 
        prettyXml(subelement, indent, newline, level = level + 1)


def create(root_dir, img_name, bg_size, count, tg_loca):
          '''
          root_dir: 要写到得文件夹下
          img_name: 对应样本的文件名
          bg_size: 图片的大小 (w, h)
          count: 目标的个数
          tg_loca: 裂缝目标的位置 list[(x_tl, y_tl, x_br, y_br)]
          '''
          # 1 annotation
          annotation = Element('annotation')
          
          # 1-1 filename
          filename = SubElement(annotation, 'filename')
          filename.text = img_name

          # 1-2 object_count
          object_count = SubElement(annotation, 'object_count')
          object_count.text = str(count)

          # 1-3 size
          # -------------------size start--------------------------
          size = SubElement(annotation, 'size')

          # 1-3-1 width
          width = SubElement(size, 'width')
          width.text = str(bg_size[0])

          # 1-3-2 height
          height = SubElement(size, 'height')
          height.text = str(bg_size[1])

          # 1-3-3 depth
          depth = SubElement(size, 'depth')
          depth.text = '1'
          # -------------------size end--------------------------

          # 1-4 segmented
          segmented = SubElement(annotation, 'segmented')
          segmented.text = '0'

          # 1-(5 : 5 + count) object
          for i in range(0, count):
                object = SubElement(annotation, 'object')
                # 1-(:)-1 name
                name = SubElement(object, 'name')
                name.text = 'Crack'

                # 1-(:)-2 pose
                pose = SubElement(object, 'pose')
                pose.text = 'Unspecified'

                # 1-(:)-3 truncated
                truncated = SubElement(object, 'truncated')
                truncated.text = str(i)

                # 1-(:)-4 difficult
                difficult = SubElement(object, 'difficult')
                difficult.text = '0'

                # 1-(:)-5 bndbox
                # ---------------------bndbox start------------------------------
                bndbox = SubElement(object, 'bndbox')
                # xmin
                xmin = SubElement(bndbox, 'xmin')
                xmin.text = str(tg_loca[i][0])
                # ymin
                ymin = SubElement(bndbox, 'ymin')
                ymin.text = str(tg_loca[i][1])
                # xmax
                xmax = SubElement(bndbox, 'xmax')
                xmax.text = str(tg_loca[i][2])
                # ymax
                ymax = SubElement(bndbox, 'ymax')
                ymax.text = str(tg_loca[i][3])
                # ---------------------bndbox end------------------------------
          
          tree = ElementTree(annotation)
          root = tree.getroot()  
          prettyXml(root, '\t', '\n')
          
          # write out xml data
          tree.write(root_dir + img_name + '.xml', encoding = 'utf-8')


# img_name = '1.jpg'
# bg_size = (512, 512)
# count = 2
# tg_loca = [(12, 15, 128, 139), (12, 25, 89, 98)]

# create(img_name, bg_size, count, tg_loca)