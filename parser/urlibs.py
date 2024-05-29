import os
import shutil
from pathlib import Path
from subprocess import run
from ppstructure.utility import draw_structure_result


def sorted_layout_boxes(res, w):
    """
    Sort text boxes in order from top to bottom, left to right
    args:
        res(list):ppstructure results
    return:
        sorted results(list)
    """
    num_boxes = len(res)
    if num_boxes == 1:
        res[0]["layout"] = "single"
        return res

    sorted_boxes = sorted(res, key=lambda x: (x["bbox"][1], x["bbox"][0]))
    _boxes = list(sorted_boxes)

    new_res = []
    res_left = []
    res_right = []

    for _box in _boxes:
        bbox = _box['bbox']
        m_x = (bbox[0] + bbox[2]) / 2
        if m_x + 10 > w / 2 - 10 and m_x - 10 < w / 2:
            new_res += res_left
            new_res += res_right
            _box["layout"] = "single"
            new_res.append(_box)
            res_left = []
            res_right = []
        elif m_x < w / 2:
            _box["layout"] = "double"
            res_left.append(_box)
        else:
            _box["layout"] = "double"
            res_right.append(_box)

    if res_left:
        new_res += res_left
    if res_right:
        new_res += res_right
    return new_res


def file_to_pdf(doc_path, basedir, file_type=0):
    """
    Converts a Word document to a PDF file using LibreOffice.
    """
    output_folder = os.path.join(basedir, "output/tmp")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if file_type == 0:
        pdf_path = doc_path.replace(".docx", ".pdf")
    elif file_type == 1:
        pdf_path = doc_path.replace(".pptx", ".pdf").replace(".ppt", ".pdf")
    stem = os.path.basename(pdf_path)
    pdf_path = os.path.join(output_folder, stem)
    command = ['soffice', '--headless', '--convert-to', 'pdf', '--outdir', output_folder, doc_path]
    run(command, check=True)
    return pdf_path


def clear(file_path):
    if os.path.isdir(file_path):
        files = traverse_directory(file_path)
    else:
        files = [file_path]
    for file in files:
        os.remove(file)


def traverse_directory(directory):
    files = []
    path = Path(directory)
    for file_path in path.rglob('*'):
        if file_path.is_file():
            files.append(str(file_path))
    return files


def draw(result, image):
    from PIL import Image

    font_path = '/Users/zhoutao/code/PaddleOCR/doc/fonts/simfang.ttf'  # PaddleOCR下提供字体包
    im_show = draw_structure_result(image, result, font_path=font_path)
    im_show = Image.fromarray(im_show)
    im_show.save('/Users/zhoutao/code/TextRec/output/tmp/result.jpg')


if __name__ == '__main__':
    file_to_pdf("../data/docx/word3.docx", "../")
