from paddleocr import PaddleOCR
from parser.pdf_parser import PdfParser
from parser.pptx_parser import PptxParser
from parser.docx_parser import DocxParser
from parser.excel_parser import ExcelParser
from parser.pic_parser import PicParser
import os
from tqdm import tqdm
import argparse


def write_helper(data, path):
    with open(path, "w", encoding="utf-8") as fw:
        fw.write(data)


class Parser:

    def __init__(self):
        self.pdf = PdfParser()
        self.ppt = PptxParser()
        self.doc = DocxParser()
        self.excel = ExcelParser()
        self.pic = PicParser()

    def __call__(self, file_name, output_dir=r"output/"):
        paths = []
        file_name.replace('//', '/')
        file_name.replace('\\', '/')
        if os.path.isfile(file_name):
            paths.append(file_name)
        elif os.path.isdir(file_name):
            tmp = os.listdir(file_name)
            for file in tmp:
                paths.append(os.path.join(file_name, file))
        else:
            raise Exception('Illegal FileName!')
        for name in tqdm(paths):
            try:
                basename = os.path.basename(name).split('.')[0] + '.txt'
                if name.endswith('pdf'):
                    re = self.pdf(name)
                elif name.endswith('docx'):
                    re = self.doc(name)
                elif name.endswith("pptx"):
                    re = self.ppt(name)
                elif name.endswith("xlsx"):
                    re = self.excel(name)
                else:
                    re = self.pic(name)
                write_helper("\n".join(re), os.path.join(output_dir, basename))
            except:
                print(f"{name} is error!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_dir", type=str, default="data/")
    parser.add_argument("--output_dir", type=str, default="output/")
    args = parser.parse_args()
    par = Parser()
    print(args.source_dir, args.output_dir)
    par(args.source_dir, args.output_dir)
