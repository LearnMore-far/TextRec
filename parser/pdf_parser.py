from .urlibs import sorted_layout_boxes
from paddleocr import check_img
import os
import cv2


class PdfParser:

    def __init__(self, ocr=None, lang="ch"):
        if ocr is None:
            from paddleocr import PPStructure
            self.pdf_ocr = PPStructure(show_log=False, lang=lang)
        else:
            self.pdf_ocr = ocr

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
        save_folder = f"../output/tmp"
        os.makedirs(save_folder, exist_ok=True)
        for page_idx, img in enumerate(imgs):
            rec_res = self.pdf_ocr(img)
            h, w, _ = img.shape
            rec_res = sorted_layout_boxes(rec_res, w)
            for res in rec_res:
                if len(res['res']) == 0:
                    continue
                if res['type'] == 'figure':
                    # Todo upload figure to web, and add it`s text and link to original pos
                    img_path = os.path.join(
                        save_folder, "{}_{}.jpg".format(res["bbox"], res['img_idx'])
                    )
                    cv2.imwrite(img_path, res['img'])
                    t = [s['text'] for s in res['res']]
                    s = " ".join(t)
                    s += f" <link {res['bbox']}_{res['img_idx']}.jpg >"
                    pdf_re.append(s)
                elif res['type'] == 'table':
                    table = res['res']['html'].replace('<html><body>', '').replace('</body></html>', '')
                    pdf_re.append(table)
                elif res['type'] == 'equation':
                    # Todo convert equation to markdown type
                    # eq_path = os.path.join(
                    #     save_folder, "{}_{}.jpg".format(res["bbox"], res['img_idx'])
                    # )
                    # cv2.imwrite(eq_path, res['img'])
                    t = [s['text'] for s in res['res']]
                    s = " ".join(t)
                    pdf_re.append(s)
                else:
                    t = [s['text'] for s in res['res']]
                    s = " ".join(t)
                    pdf_re.append(s)

        return pdf_re


if __name__ == '__main__':
    re = PdfParser()("../data/picture/table1.png", page_num=6)
    with open('../output/table1.txt', 'w') as w:
        w.write("\n".join(re))
