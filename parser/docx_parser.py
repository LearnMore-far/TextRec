import docx
from docx.document import Document
from docx.text.paragraph import Paragraph
from docx.parts.image import ImagePart
from docx.table import _Cell, Table
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P


class DocxParser:

    def __init__(self, ocr=None, lang="ch"):
        if ocr is None:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)
        else:
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
        return "\n".join(["|".join([cell.text for cell in row.cells]) for row in table.rows])

    def __is_formula(self, paragraph):
        return bool(paragraph._element.xpath('.//m:oMath'))

    def __extract_formula_text(self, omml_element):
        return "".join([node.text for node in omml_element.iter() if node.text])

    def __extract_formula(self, paragraph):
        omml_elements = paragraph._element.xpath('.//m:oMath')
        for omml in omml_elements:
            return self.__extract_formula_text(omml)
        # formula_texts = [self.__extract_formula_text(omml) for omml in omml_elements]
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

    def __call__(self, word_path):
        doc = docx.Document(word_path)
        re = []
        for block in self.__iter_block_items(doc):
            if isinstance(block, Paragraph):
                re.append(block.text)
            elif isinstance(block, Table):
                re.append(self.__read_table(block))
            elif isinstance(block, ImagePart):
                res = self.ocr.ocr(block.blob, cls=True)
                if res[0]:
                    re.append("\n".join([line[1][0] for line in res[0]]))
            elif isinstance(block, str):
                re.append(block)
            else:
                print(f"Doc Unknown type: {block}")
        return re


if __name__ == '__main__':
    re = DocxParser()('../data/word.docx')
    for i in re:
        print(i)
