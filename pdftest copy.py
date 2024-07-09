import fitz  # PyMuPDF
import os

def extract_text_and_images(pdf_path, font_size_threshold):
    # 打开PDF文件
    pdf_document = fitz.open(pdf_path)
    chapter_images = {}

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        blocks = page.get_text("dict")['blocks']

        for block in blocks:  # 遍历每个文本块
            if 'lines' in block:  # 确定这是文本块
                for line in block['lines']:
                    for span in line['spans']:
                        # 检查字号大小
                        if span['size'] > font_size_threshold:
                            chapter_title = span['text'].strip()
                            chapter_images.setdefault(chapter_title, [])
            elif 'img' in block:  # 确定这是图片块
                # 获取图片数据
                img_data = block['img']
                xref = img_data[0]
                pix = fitz.Pixmap(pdf_document, xref)
                # 保存图片到对应章节的文件夹
                for chapter_title in chapter_images:
                    chapter_folder = f"{chapter_title}_images"
                    if not os.path.exists(chapter_folder):
                        os.makedirs(chapter_folder)
                    img_path = f"{chapter_folder}/{chapter_title}_img{page_number}.png"
                    pix.save(img_path)
                    chapter_images[chapter_title].append(img_path)

    pdf_document.close()
    return chapter_images

# 使用函数
pdf_path = "C:/Users/Ecust/Desktop/实验室/项目/大模型/双栏标题图片.pdf"
font_size_threshold = 18  # 字号大小阈值
chapter_images = extract_text_and_images(pdf_path, font_size_threshold)
print(chapter_images)
