from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


class PptxParser:

    def __init__(self, ocr=None, lang="ch"):
        if ocr is None:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)
        else:
            self.ocr = ocr

    def __call__(self, pptx_path):
        prs = Presentation(pptx_path)
        re = []
        for slide in prs.slides:
            for shape in slide.shapes:
                # if shape.has_text_frame:
                #     text_frame = shape.text_frame
                #     print(text_frame.text)

                # 也可以通过下面这种方式，更好判断每个shape的类型
                if shape.shape_type == MSO_SHAPE_TYPE.TEXT_BOX:
                    text_frame = shape.text_frame
                    re.append(text_frame.text)

                if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                    res = self.ocr.ocr(shape.image.blob)
                    if res[0]:
                        re.append(" ".join([line[1][0] for line in res[0]]))
        return re


if __name__ == '__main__':
    print(PptxParser()('../data/ex.pptx'))
