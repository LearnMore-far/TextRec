import os
import cv2
from paddleocr import PPStructure, draw_structure_result, PaddleOCR

table_engine = PaddleOCR(show_log=True)

save_folder = '../output/tmp'
img_path = '../data/picture/pdf6.png'
img = cv2.imread(img_path)
result = table_engine(img)
# save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])

from PIL import Image

font_path = '/Users/zhoutao/code/PaddleOCR/doc/fonts/simfang.ttf' # PaddleOCR下提供字体包
image = Image.open(img_path).convert('RGB')
im_show = draw_structure_result(image, result,font_path=font_path)
im_show = Image.fromarray(im_show)
im_show.save('../output/tmp/result.jpg')