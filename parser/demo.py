# import os
# import cv2
# from paddleocr import PPStructure, draw_structure_result, PaddleOCR
# from ppocr.utils.utility import check_and_read
# table_engine = PPStructure(show_log=True, lang="en", recovery=True)
#
# save_folder = '../output/tmp'
# img_path = '../data/pdf/weekly_market_recap.pdf'
# # img = cv2.imread(img_path)
# img, flag_gif, flag_pdf = check_and_read(img_path)
# result = table_engine(img[0])
# # save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])
#
# from PIL import Image
#
# font_path = '/Users/zhoutao/code/PaddleOCR/doc/fonts/simfang.ttf'  # PaddleOCR下提供字体包
# # image = Image.open(img_path).convert('RGB')
# image = Image.fromarray(img[0])
# im_show = draw_structure_result(image, result, font_path=font_path)
# im_show = Image.fromarray(im_show)
# im_show.save('../output/tmp/result.jpg')
# from unstructured.partition.auto import partition
# from unstructured.partition.pdf import partition_pdf
# from tempfile import TemporaryDirectory
#
# elements = partition("../data/docx/word2.docx",
#                      strategy="hi_res",
#                      pdf_extract_element_types=["Image", "Formula", "Table"],
#                      pdf_infer_table_structure=True,
#                      pdf_extract_to_payload=True,
#                      skip_infer_table_types=[],
#                      # extract_element_types=['Image', "Formula", "Table"],
#                      # extract_to_payload=True,
#                      # infer_table_structure=True,
#                      image_output_dir_path="../output/tmp"
#                      )
# print()

from pix2tex.cli import LatexOCR
from PIL import Image

img1 = Image.open("../data/picture/fmla2.png")
model = LatexOCR()
re = model(img1)
print(re)
