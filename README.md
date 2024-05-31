# TextRec 快速开始

**说明：**  用于提取pdf，docx，pptx，excel以及图片中的文字，能够提取文档图片、表格以及公式的文字

## 1. 环境设置
mac环境 python3.8
```
conda env create -f environment.yml -n your_env
命令行安装libreoffice
注意：目前paddleOCR使用的是cpu版本，非常非常非常慢！
要使用gpu版本需要安装gpu版本paddleOCR
pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple
然后设置use_gpu=True，paser文件夹的pdf_parser中
self.pdf_ocr = PPStructure(lang="ch", use_gpu=True)
```
## 2.使用指南

--source_dir 指定输入目录，可为单个文件或者文件夹

--output_dir 指定输出目录，输出为txt文本；默认参数为None，结果输出到控制台

--fast 此参数开启unstructured库的识别方法，有两个选项
* "fast": 当为fast时，使用非OCR方式提取，此时仅提取文本内容，不提取图像等内容，比较快
* "hi_res": 当为hi_res时，使用OCR方式识别，在没有GPU时会很慢
* 默认参数为None，表示不开启

--doc2pdf & --ppt2pdf 这两个参数将docx或者ppt转为pdf然后套用pdf识别的pipeline，默认为False

默认情况下docx和ppt采用混合的方式提取文本，也就是使用python-docx和python-pptx提取文本，然后图表公式等利用OCR方式识别

```commandline
python3 main.py --source_dir your_source_dir --output_dir your_output_dir
```