import os

import docx
from docx.document import Document
from docx.text.paragraph import Paragraph
from docx.parts.image import ImagePart
from docx.table import _Cell, Table
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from paddle.dataset.image import cv2
from paddleocr import img_decode
from tempfile import TemporaryDirectory


class DocxParser:

    def __init__(self, ocr):
        self.ocr = ocr

    def __is_image(self, graph: Paragraph, doc: Document):
        images = graph._element.xpath('.//pic:pic')  # 获取所有图片
        for image in images:
            for img_id in image.xpath('.//a:blip/@r:embed'):  # 获取图片id
                part = doc.part.related_parts[img_id]  # 根据图片id获取对应的图片
                if isinstance(part, ImagePart):
                    return True
        return False

    def __get_ImagePart(self, graph: Paragraph, doc: Document):
        images = graph._element.xpath('.//pic:pic')  # 获取所有图片
        for image in images:
            for img_id in image.xpath('.//a:blip/@r:embed'):  # 获取图片id
                part = doc.part.related_parts[img_id]  # 根据图片id获取对应的图片
                if isinstance(part, ImagePart):
                    return part
        return None

    def __read_table(self, table):
        rows = ["<table><thead>"]
        row_text = ["<tr>"]
        for cell in table.rows[0].cells:
            row_text.append(f"<td>{cell.text}</td>")
        row_text.append("</tr>")
        rows.append("".join(row_text))
        rows.append("</thead><tbody>")
        for idx, row in enumerate(table.rows):
            if idx == 0:
                continue
            row_text = ["<tr>"]
            for cell in row.cells:
                row_text.append(f"<td>{cell.text}</td>")
            row_text.append("</tr>")
            rows.append("".join(row_text))
        rows.append("</tbody></table>")
        s = "以下是一张表格，包含对应的格式以及数据，以<end_table>结尾: \n"
        table = "".join(rows)
        s += table
        s += "\n<end_table>"
        return s

    def __is_formula(self, paragraph):
        return bool(paragraph._element.xpath('.//m:oMath'))

    def __extract_formula_text(self, omml_element):
        s = "以下是一个公式，包含对应的格式，以<end_formula>结尾: \n"
        formula = "".join([node.text for node in omml_element.iter() if node.text])
        s += formula
        s += "\n<end_formula>"
        return

    def __extract_formula(self, paragraph):
        omml_elements = paragraph._element.xpath('.//m:oMath')
        for omml in omml_elements:
            return self.__extract_formula_text(omml)
        return None

    def __iter_block_items(self, parent):
        """
        Yield each paragraph and table child within *parent*, in document order.
        Each returned value is an instance of either Table or Paragraph. *parent*
        would most commonly be a reference to a main Document object, but
        also works for a _Cell object, which itself can contain paragraphs and tables.
        """
        if isinstance(parent, Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        else:
            raise ValueError("something's not right")

        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                paragraph = Paragraph(child, parent)
                yield Paragraph(child, parent)
                if self.__is_image(paragraph, parent):
                    yield self.__get_ImagePart(paragraph, parent)
                if self.__is_formula(paragraph):
                    yield self.__extract_formula(paragraph)
            elif isinstance(child, CT_Tbl):
                yield Table(child, parent)
            else:
                continue

    def __save_image__(self, block, save_folder):
        img_path = os.path.join(
            save_folder, "{}.jpg".format(block.sha1)
        )
        cv2.imwrite(img_path, img_decode(block.blob))
        return img_path

    def __call__(self, word_path):
        doc = docx.Document(word_path)
        re = []
        with TemporaryDirectory() as tmpdir:
            for block in self.__iter_block_items(doc):
                if isinstance(block, Paragraph):
                    re.append(block.text)
                elif isinstance(block, Table):
                    re.append(self.__read_table(block))
                elif isinstance(block, ImagePart):
                    res = self.ocr(block.blob)
                    if len(res):
                        re.append("\n".join(res))
                elif isinstance(block, str):
                    re.append(block)
                else:
                    continue
        return re


if __name__ == '__main__':
    from pdf_parser import PdfParser
    re = DocxParser(PdfParser())('../data/docx/word.docx')
    with open('../output/word.txt', 'w') as w:
        w.write("\n".join(re))
