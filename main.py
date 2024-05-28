from parser.pdf_parser import PdfParser
from parser.pptx_parser import PptxParser
from parser.docx_parser import DocxParser
from parser.excel_parser import ExcelParser
from parser.pic_parser import PicParser
from parser.urlibs import file_to_pdf, clear, traverse_directory
import os
from tqdm import tqdm
import argparse


def write_helper(data, path):
    with open(path, "w", encoding="utf-8") as fw:
        fw.write(data)


class Parser:

    def __init__(self):
        self.pdf = PdfParser()
        self.ppt = PptxParser(self.pdf)
        self.doc = DocxParser(self.pdf)
        self.excel = ExcelParser()
        self.pic = PicParser(self.pdf)

    def __call__(self, args):
        paths = []
        file_name = args.source_dir.replace('\\', '/')
        if os.path.isfile(file_name):
            paths.append(file_name)
        elif os.path.isdir(file_name):
            paths = traverse_directory(file_name)
        else:
            raise Exception('Illegal FileName!')
        for name in tqdm(paths[::-1][:5]):
            try:
                basename = os.path.basename(name).split('.')[0] + '.txt'
                if name.endswith('pdf'):
                    re = self.pdf(name)
                elif name.endswith('docx'):
                    if args.convert2pdf:
                        name = file_to_pdf(name)
                        re = self.pdf(name)
                        clear(name)
                    else:
                        re = self.doc(name)
                elif name.endswith("pptx"):
                    if args.convert2pdf:
                        name = file_to_pdf(name, 1)
                        re = self.pdf(name)
                        clear(name)
                    else:
                        re = self.ppt(name)
                elif name.endswith("xlsx"):
                    re = self.excel(name)
                else:
                    re = self.pic(name)
                write_helper("\n".join(re), os.path.join(args.output_dir, basename))
            except:
                print(f"{name} is error!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_dir", type=str, default="data/")
    parser.add_argument("--output_dir", type=str, default="output/")
    parser.add_argument("--convert2pdf", type=bool, default=True)
    args = parser.parse_args()
    par = Parser()
    print(args.source_dir, args.output_dir)
    par(args)
