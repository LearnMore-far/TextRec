# TextRec 快速开始

**说明：**  用于提取pdf，docx，pptx，excel以及图片中的文字，能够提取文档图片、表格以及公式的文字

## 1. 环境设置
mac环境
```
shapely
scikit-image
imgaug
pyclipper
lmdb
tqdm
numpy
rapidfuzz
opencv-python<=4.6.0.66
opencv-contrib-python<=4.6.0.66
cython
Pillow>=10.0.0
pyyaml
python-docx
python-pptx
openpyxl
paddlepaddle==2.3.2
```
## 2.使用指南
```commandline
python main.py --source_dir your_dir --output_dir your_output_dir
```