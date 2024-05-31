# from .urlibs import sorted_layout_boxes
from ppstructure.recovery.recovery_to_doc import sorted_layout_boxes
from paddleocr import check_img
import os
import cv2
from .upload import upload_file
from tqdm import tqdm
from PIL import Image
from pix2tex.cli import LatexOCR
from tempfile import TemporaryDirectory

class PdfParser:

    def __init__(self, ocr=None, lang="ch"):
        if ocr is None:
            from paddleocr import PPStructure
            self.pdf_ocr = PPStructure(show_log=False, lang=lang)
        else:
            self.pdf_ocr = ocr
        self.formula = LatexOCR()

    def __save_image__(self, res, save_folder):
        img_path = os.path.join(
            save_folder, "{}_{}.jpg".format(res["bbox"], res['img_idx'])
        )
        cv2.imwrite(img_path, res['img'])
        return img_path

    def __call__(self, pdf_path, page_num=0, alpha_color=(255, 255, 255)):

        img, flag_gif, flag_pdf = check_img(pdf_path, alpha_color)
        if isinstance(img, list) and flag_pdf:
            if page_num > len(img) or page_num == 0:
                imgs = img
            else:
                imgs = img[: page_num]
        else:
            imgs = [img]

        pdf_re = []
        if len(pdf_path) > 100:
            process_name = "picture"
        else:
            process_name = pdf_path
        with TemporaryDirectory() as tmpdir:
            for page_idx, img in enumerate(tqdm(imgs, desc=f"process {process_name}")):
                rec_res = self.pdf_ocr(img)
                h, w, _ = img.shape
                rec_res = sorted_layout_boxes(rec_res, w)
                page_info = []
                header = []
                footer = []
                for res in tqdm(rec_res, desc=f"page {page_idx}"):
                    if len(res['res']) == 0 and res['type'] != "figure":
                        continue
                    if res['type'] == 'figure':
                        s = "以下是一张图片，包含对应的<图片文本内容>以及<图片链接>，以<end_figure>结尾: \n"
                        s += "<图片文本内容>\n"
                        t = [s['text'] for s in res['res']]
                        s += "\n".join(t)
                        s += "\n</图片文本内容>"
                        img_path = self.__save_image__(res, tmpdir)
                        link = upload_file(img_path, "{}_{}.jpg".format(res["bbox"], res['img_idx']))
                        s += f"\n<图片链接>\n {link} \n</图片链接>"
                        s += "\n<end_figure>"
                        page_info.append(s)
                    elif res['type'] == 'table':
                        s = "以下是一张表格，包含对应的格式以及数据，以<end_table>结尾: \n"
                        table = res['res']['html'].replace('<html><body>', '').replace('</body></html>', '')
                        s += table
                        s += "\n<end_table>"
                        page_info.append(s)
                    elif res['type'] == 'equation':
                        s = "以下是一个公式，包含对应的格式，以<end_formula>结尾: \n"
                        eq_path = self.__save_image__(res, tmpdir)
                        img = Image.open(eq_path)
                        eq = self.formula(img)
                        s += eq
                        s += "\n<end_formula>"
                        page_info.append(s)
                    else:
                        t = [s['text'] for s in res['res']]
                        s = "\n".join(t)
                        if res['type'] == 'header':
                            header.append(s)
                        elif res['type'] == 'footer':
                            footer.append(s)
                        else:
                            page_info.append(s)
                pdf_re.extend(header)
                pdf_re.extend(page_info)
                pdf_re.extend(footer)
        return pdf_re


if __name__ == '__main__':
    re = PdfParser()("../data/pdf/word2.pdf", page_num=7)
    with open('../output/word2.txt', 'w') as w:
        w.write("\n".join(re))
