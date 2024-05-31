import os

import cv2
from tqdm import tqdm
import base64
from paddleocr import img_decode
from .upload import upload_file
from tempfile import TemporaryDirectory
from unstructured.partition.auto import partition


class FastParser:
    def __init__(self):
        pass

    def __save_image__(self, element, save_folder):
        img_path = os.path.join(
            save_folder, "{}.jpg".format(element.id)
        )
        cv2.imwrite(img_path, img_decode(base64.b64decode(element.metadata.image_base64)))
        return img_path

    def __table__(self, table):
        s = "以下是一张表格，包含对应的格式以及数据，以<end_table>结尾: \n"
        s += table.metadata.text_as_html
        s += "\n<end_table>"
        return s

    def __image__(self, image, save_folder):
        img_path = self.__save_image__(image, save_folder)
        link = upload_file(img_path, "{}.jpg".format(image.id))
        return link

    def __formula__(self, formula):
        s = "以下是一个公式，包含对应的格式，以<end_formula>结尾: \n"
        s += formula.text
        s += "\n<end_formula>"
        return s

    def __call__(self, file_name, strategy="fast"):
        with TemporaryDirectory() as tmpdir:
            elements = partition(file_name,
                                 strategy=strategy,
                                 pdf_extract_element_types=["Image", "Formula", "Table"],
                                 pdf_infer_table_structure=True,
                                 pdf_extract_to_payload=True,
                                 skip_infer_table_types=[],
                                 pdf_image_output_dir_path=tmpdir)
            if strategy == "fast":
                return [element.text for element in elements]
            re = []
            for element in tqdm(elements, desc=f"process {file_name}"):
                if element.category == "Image":
                    s = "以下是一张图片，包含对应的<图片文本内容>以及<图片链接>，以<end_figure>结尾: \n"
                    s += "<图片文本内容>\n"
                    s += element.text
                    s += "\n</图片文本内容>"
                    link = self.__image__(element, tmpdir)
                    s += f"\n<图片链接>\n {link} \n</图片链接>"
                    s += "\n<end_figure>"
                    re.append(s)
                elif element.category == "Table":
                    re.append(self.__table__(element))
                elif element.category == "Formula":
                    re.append(self.__formula__(element))
                else:
                    re.append(element.text)
        return re


if __name__ == '__main__':
    re = FastParser()("../data/pptx/LargePpt.pptx", strategy="hi_res")
    with open('../output/pdf6.txt', 'w') as w:
        w.write("\n".join(re))
