class PicParser:

    def __init__(self, ocr):
        self.ocr = ocr

    def __call__(self, img_path):
        return self.ocr(img_path)


if __name__ == '__main__':
    from pdf_parser import PdfParser
    print(PicParser(PdfParser())("../data/captcha_demo.png"))
