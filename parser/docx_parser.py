# docx
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
        return [[cell.text for cell in row.cells] for row in table.rows]

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
                if self.__is_image(paragraph, parent):
                    # print('[Image] ')
                    yield self.__get_ImagePart(paragraph, parent)
                # print('[Text] ')
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                # print('[Table] ')
                yield Table(child, parent)

    def __call__(self, word_path):
        doc = docx.Document(word_path)
        re = []
        for block in self.__iter_block_items(doc):
            if isinstance(block, Paragraph):
                re.append(block.text)
                # print("text", [block.text])
            elif isinstance(block, Table):
                re.append(self.__read_table(block))
                # print("table", self.__read_table(block))
            elif isinstance(block, ImagePart):
                res = self.ocr.ocr(block.blob, cls=True)
                if res[0]:
                    # print("Image", " ".join([line[1][0] for line in res[0]]))
                    re.append("\n".join([line[1][0] for line in res[0]]))
            else:
                print('Unknown Type')
        return re


if __name__ == '__main__':
    print(DocxParser()('../data/word.docx'))
