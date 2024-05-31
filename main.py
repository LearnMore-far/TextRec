from parser.pdf_parser import PdfParser
from parser.pptx_parser import PptxParser
from parser.docx_parser import DocxParser
from parser.excel_parser import ExcelParser
from parser.pic_parser import PicParser
from parser.fast_parser import FastParser
from parser.urlibs import file_to_pdf, traverse_directory, init_args
import os
from tqdm import tqdm
from tempfile import TemporaryDirectory


def write_helper(data, path):
    with open(path, "w", encoding="utf-8") as fw:
        fw.write(data)


class Parser:

    def __init__(self):
        self.basedir = os.path.abspath(__file__).replace("main.py", "")
        # 利用paddleOCR进行版面分析，文字检测，文字识别
        self.pdf = PdfParser()
        # 利用python-pptx进行顺序处理，遇到图片用paddleOCR处理
        self.ppt = PptxParser(self.pdf)
        # 利用python-docx进行顺序处理，遇到图片用paddleOCR处理
        self.doc = DocxParser(self.pdf)
        # 利用openpyxl处理excel表单
        self.excel = ExcelParser()
        # 利用paddleOCR处理
        self.pic = PicParser(self.pdf)
        # 利用unstructured库处理
        self.fast = FastParser()

    def __pdf__(self, args, file_name):
        if args.fast:
            re = self.fast(file_name, strategy=args.fast)
        else:
            re = self.pdf(file_name)
        return re

    def __docx__(self, args, file_name, tmpdir):
        if args.doc2pdf:
            file_name = file_to_pdf(file_name, tmpdir)
        if args.fast:
            re = self.fast(file_name, strategy=args.fast)
        elif args.doc2pdf:
            re = self.pdf(file_name)
        else:
            re = self.doc(file_name)
        return re

    def __pptx__(self, args, file_name, tmpdir):
        if args.ppt2pdf:
            file_name = file_to_pdf(file_name, tmpdir, file_type=1)
        if args.fast:
            re = self.fast(file_name, strategy=args.fast)
        elif args.ppt2pdf:
            re = self.pdf(file_name)
        else:
            re = self.ppt(file_name)
        return re

    def __call__(self, args):
        """
        :param args: 指定参数
        :return: list, 其中每一项为一个文件解析
        """
        paths = []
        file_name = args.source_dir.replace('\\', '/')
        if os.path.isfile(file_name):
            paths.append(os.path.abspath(file_name))
        elif os.path.isdir(file_name):
            paths = traverse_directory(os.path.abspath(file_name))
        else:
            raise Exception('Illegal FileName!')
        result = []
        with TemporaryDirectory() as tmpdir:
            for name in tqdm(paths):
                try:
                    basename = os.path.basename(name).split('.')[0] + '.txt'
                    if name.endswith('pdf'):
                        re = self.__pdf__(args, name)
                    elif name.endswith('docx'):
                        re = self.__docx__(args, name, tmpdir)
                    elif name.endswith("pptx"):
                        re = self.__pptx__(args, name, tmpdir)
                    elif name.endswith("xlsx"):
                        re = self.excel.html(name)
                    else:
                        re = self.pic(name)
                    if args.output_dir:
                        write_helper("\n".join(re), os.path.join(args.output_dir, basename))
                    else:
                        result.append("\n".join(re))
                except Exception as e:
                    print("异常产生：", e)
        return result, paths


if __name__ == '__main__':
    parser = init_args()
    args = parser.parse_args()
    par = Parser()
    print(args)
    re = par(args)
    if not args.output_dir:
        for file, name in zip(re[0], re[1]):
            print(name)
            print(file)
