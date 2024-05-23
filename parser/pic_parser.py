class PicParser:

    def __init__(self, ocr=None, lang="ch"):
        if ocr is None:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)
        else:
            self.ocr = ocr

    def __call__(self, img_path):
        result = self.ocr.ocr(img_path, cls=True)
        re = []
        for idx in range(len(result)):
            res = result[idx]
            if res == None:
                continue
            texts = [line[1][0] for line in res]
            re.append("\n".join(texts))
        return re


if __name__ == '__main__':
    print(PicParser()("../data/captcha_demo.png"))
