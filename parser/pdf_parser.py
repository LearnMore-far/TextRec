class PdfParser:

    def __init__(self, ocr=None, lang="ch", page_num=0):
        if ocr is None:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(use_angle_cls=True, lang=lang, page_num=page_num, show_log=False)
        else:
            self.ocr = ocr

    def __call__(self, pdf_path):
        result = self.ocr.ocr(pdf_path, cls=True)
        re = []
        for idx in range(len(result)):
            res = result[idx]
            if res == None:
                continue
            texts = [line[1][0] for line in res]
            re.append(texts)
        return re


if __name__ == '__main__':
    print(PdfParser(page_num=5)("../data/UnrealText.pdf"))
