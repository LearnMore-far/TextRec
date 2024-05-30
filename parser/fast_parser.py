import os

import cv2
from tqdm import tqdm
import base64
from paddleocr import img_decode
from upload import upload_file
from urlibs import clear

from unstructured.partition.auto import partition


class FastParser:
    def __init__(self):
        self.save_folder = os.path.abspath(__file__).replace("parser/fast_parser.py", "output/tmp")
        os.makedirs(self.save_folder, exist_ok=True)

    def __save_image__(self, element):
        img_path = os.path.join(
            self.save_folder, "{}.jpg".format(element.id)
        )
        cv2.imwrite(img_path, img_decode(base64.b64decode(element.metadata.image_base64)))
        return img_path

    def __table__(self, table):
        return table.metadata.text_as_html

    def __image__(self, image):
        img_path = self.__save_image__(image)
        link = upload_file(img_path, "{}.jpg".format(image.id))
        return link

    def __formula__(self, formula):
        return formula.text

    def __call__(self, file_name, strategy="fast"):
        elements = partition(file_name,
                             strategy=strategy,
                             pdf_extract_element_types=["Image", "Formula", "Table"],
                             pdf_infer_table_structure=True,
                             pdf_extract_to_payload=True,
                             skip_infer_table_types=[],
                             pdf_image_output_dir_path=self.save_folder)
        if strategy == "fast":
            return [element.text for element in elements]
        re = []
        for element in tqdm(elements, desc=f"process {file_name}"):
            if element.category == "Image":
                re.append(element.text)
                re.append(self.__image__(element))
            elif element.category == "Table":
                re.append(self.__table__(element))
            elif element.category == "Formula":
                re.append(self.__formula__(element))
            else:
                re.append(element.text)
        clear(self.save_folder)
        return re


if __name__ == '__main__':
    re = FastParser()("../data/pdf/LargePdf.pdf", strategy="hi_res")
    with open('../output/LargePdf.txt', 'w') as w:
        w.write("\n".join(re))
