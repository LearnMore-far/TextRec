from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


class PptxParser:

    def __init__(self, ocr=None, lang="ch"):
        if ocr is None:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)
        else:
            self.ocr = ocr

    def __extract(self, shape):
        if shape.shape_type == 19:
            # tb = shape.table
            # rows = []
            # for i in range(1, len(tb.rows)):
            #     rows.append("; ".join([tb.cell(
            #         0, j).text + ": " + tb.cell(i, j).text for j in range(len(tb.columns)) if tb.cell(i, j)]))
            # return "\n".join(rows)

            table = shape.table
            rows = []
            for row in table.rows:
                row_text = []
                for cell in row.cells:
                    row_text.append(cell.text_frame.text)
                rows.append(" | ".join(row_text))
            return "\n".join(rows)

        if shape.has_text_frame:
            return shape.text_frame.text

        if shape.shape_type == 6:
            texts = []
            for p in sorted(shape.shapes, key=lambda x: (x.top // 10, x.left)):
                t = self.__extract(p)
                if t:
                    texts.append(t)
            return "\n".join(texts)

        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            res = self.ocr.ocr(shape.image.blob)
            if res[0]:
                return " ".join([line[1][0] for line in res[0]])

    def __call__(self, pptx_path):
        prs = Presentation(pptx_path)
        re = []
        for slide in prs.slides:
            texts = []
            for shape in sorted(slide.shapes, key=lambda x: (x.top // 10, x.left)):
                # if shape.shape_type == MSO_SHAPE_TYPE.TEXT_BOX:
                #     text_frame = shape.text_frame
                #     re.append(text_frame.text)
                #
                # elif shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                #     res = self.ocr.ocr(shape.image.blob)
                #     if res[0]:
                #         re.append(" ".join([line[1][0] for line in res[0]]))
                #
                # elif shape.shape_type == MSO_SHAPE_TYPE.TABLE:
                #     table = shape.table
                #     for row in table.rows:
                #         row_text = []
                #         for cell in row.cells:
                #             row_text.append(cell.text_frame.text)
                #         re.append(" | ".join(row_text))
                # else:
                #     print(f"Ppt Unknown type: {shape}")
                txt = self.__extract(shape)
                if txt:
                    texts.append(txt)
            re.append("\n".join(texts))
        return re


if __name__ == '__main__':
    re = PptxParser()('../data/LargePpt.pptx')
    for i in re:
        print(i)
