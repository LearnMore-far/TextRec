from parser.pdf_parser import PdfParser
from parser.pptx_parser import PptxParser
from parser.docx_parser import DocxParser
from parser.excel_parser import ExcelParser
from parser.pic_parser import PicParser
from parser.urlibs import file_to_pdf, traverse_directory, clear
import os
from tqdm import tqdm
import argparse


def write_helper(data, path):
    with open(path, "w", encoding="utf-8") as fw:
        fw.write(data)


class Parser:

    def __init__(self):
        self.basedir = os.path.abspath(__file__).replace("main.py", "")
        self.pdf = PdfParser()
        self.ppt = PptxParser(self.pdf)
        self.doc = DocxParser(self.pdf)
        self.excel = ExcelParser()
        self.pic = PicParser(self.pdf)

    def __call__(self, args):
        paths = []
        file_name = args.source_dir.replace('\\', '/')
        if os.path.isfile(file_name):
            paths.append(os.path.abspath(file_name))
        elif os.path.isdir(file_name):
            paths = traverse_directory(os.path.abspath(file_name))
        else:
            raise Exception('Illegal FileName!')
        for name in tqdm(paths):
            try:
                basename = os.path.basename(name).split('.')[0] + '.txt'
                if name.endswith('pdf'):
                    re = self.pdf(name)
                elif name.endswith('docx'):
                    if args.doc2pdf:
                        name = file_to_pdf(name, self.basedir)
                        re = self.pdf(name)
                    else:
                        re = self.doc(name)
                elif name.endswith("pptx"):
                    if args.ppt2pdf:
                        name = file_to_pdf(name, self.basedir, file_type=1)
                        re = self.pdf(name)
                    else:
                        re = self.ppt(name)
                elif name.endswith("xlsx"):
                    re = self.excel.html(name)
                else:
                    re = self.pic(name)
                write_helper("\n".join(re), os.path.join(args.output_dir, basename))
            except:
                clear(self.pdf.save_folder)
                print(f"{name} is error!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_dir", type=str, default="./data/pdf/LargePdf.pdf")
    parser.add_argument("--output_dir", type=str, default="./output/")
    parser.add_argument("--doc2pdf", type=bool, default=True)
    parser.add_argument("--ppt2pdf", type=bool, default=False)
    args = parser.parse_args()
    par = Parser()
    print(args.source_dir, args.output_dir)
    par(args)
