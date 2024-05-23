from paddleocr import PaddleOCR
from parser.pdf_parser import PdfParser
from parser.pptx_parser import PptxParser
from parser.docx_parser import DocxParser
from parser.excel_parser import ExcelParser
import os
from tqdm import tqdm

class Parser:

    def __init__(self):
        self.pdf = PdfParser()
        self.ppt = PptxParser()
        self.doc = DocxParser()
        self.excel = ExcelParser()

    def __call__(self, file_name, output_dir=r"output/"):
        paths = []
        root = ""
        if os.path.isfile(file_name):
            paths.append(file_name)
        elif os.path.isdir(file_name):
            paths.extend(os.listdir(file_name))
        else:
            raise Exception('Illegal FileName!')
        for name in tqdm(paths):
            if name.endwith('pdf'):



if __name__ == '__main__':
    par = Parser()

