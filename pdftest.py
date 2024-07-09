import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QLabel, QWidget, QAction, QMenuBar,QDialog,QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage  # 注意这里，添加了QImage
import fitz  # PyMuPDF的fitz模块用于处理PDF文件


class TextEditorWindow(QDialog):
    def __init__(self, text_pages, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PDF Text Editor")
        layout = QVBoxLayout(self)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(False)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.set_text('\n'.join(text_pages))  # 添加一个设置文本的方法

        layout.addWidget(self.text_edit)

    def set_text(self, text):
        self.text_edit.setPlainText(text)


class PDFReader(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化变量
        self.pdf_path = None
        self.doc = None
        self.page_current = 0
        self.page_total = 0

        # 设置窗口标题和大小
        self.setWindowTitle("PDF阅读器")
        self.setGeometry(100, 100, 800, 600)

        # 创建主布局
        self.layout = QVBoxLayout()

        # 创建标签，用于显示PDF页面
        self.label = QLabel()
        self.layout.addWidget(self.label)

        # 创建按钮和功能
        self.prev_button = QPushButton("上一页")
        self.prev_button.clicked.connect(self.prev_page)
        self.layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一页")
        self.next_button.clicked.connect(self.next_page)
        self.layout.addWidget(self.next_button)

        self.custom_button1 = QPushButton("1")
        self.custom_button1.clicked.connect(self.custom_process1)
        self.layout.addWidget(self.custom_button1)

        self.custom_button2 = QPushButton("2")
        self.custom_button2.clicked.connect(self.custom_process2)
        self.layout.addWidget(self.custom_button2)

        # 创建中心窗口并设置布局
        self.center_widget = QWidget()
        self.center_widget.setLayout(self.layout)
        self.setCentralWidget(self.center_widget)

        # 创建菜单栏
        self.create_menu()

    def create_menu(self):
        # 创建菜单栏
        self.menu_bar = self.menuBar()

        # 创建文件菜单
        self.file_menu = self.menu_bar.addMenu("文件")

        # 创建上传PDF的动作
        self.upload_action = QAction("上传PDF", self)
        self.upload_action.triggered.connect(self.upload_pdf)
        self.file_menu.addAction(self.upload_action)

    def upload_pdf(self):
        # 打开文件对话框，让用户选择PDF文件
        self.pdf_path, _ = QFileDialog.getOpenFileName(self, "选择PDF文件", "", "PDF Files (*.pdf)")
        if self.pdf_path:
            # 加载PDF文件
            self.doc = fitz.open(self.pdf_path)
            self.page_total = self.doc.page_count
            # 提取PDF文本并显示
            pdf_text = self.extract_pdf_text()
            # 打开文本编辑窗口
            self.text_editor = TextEditorWindow(pdf_text)
            self.text_editor.show()
            # 显示第一页
            self.show_page(0)

    def extract_pdf_text(self):
        text_pages = []
        for page_number in range(self.page_total):
            page = self.doc.load_page(page_number)
            page_text = page.get_text()
            # 移除多余的换行符，并在页码前添加换行符
            cleaned_text = ' '.join(page_text.split())  # 移除原始文本中的换行符，并用空格连接
            text_pages.append(f"\n#{page_number + 1} {cleaned_text}")  # 在页码前添加换行符
        return text_pages

    def show_page(self, page_number):
        # 显示指定页面的内容
        self.page_current = page_number
        page = self.doc.load_page(page_number)
        pix = page.get_pixmap()
        qimage = QImage(pix.samples, pix.width, pix.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap)
        self.label.setFixedSize(pixmap.size())
        self.setWindowTitle(f"PDF阅读器 - 第{self.page_current + 1}页/共{self.page_total}页")

    def prev_page(self):
        # 显示上一页
        if self.page_current > 0:
            self.show_page(self.page_current - 1)

    def next_page(self):
        # 显示下一页
        if self.page_current < self.page_total - 1:
            self.show_page(self.page_current + 1)

    def custom_process1(self):
        # 在这里添加你的自定义处理逻辑
        # 示例：获取当前文本，进行处理，然后更新TextEditorWindow
        current_text = self.text_editor.text_edit.toPlainText()
        processed_text = current_text + "\n这是自定义处理1的结果！"
        self.text_editor.set_text(processed_text)  # 修改为正确的方法调用

    def custom_process2(self):
        # 在这里添加你的自定义处理逻辑
        # 示例：获取当前文本，进行处理，然后更新TextEditorWindow
        current_text = self.text_editor.text_edit.toPlainText()
        processed_text = current_text + "\n这是自定义处理2的结果！"
        self.text_editor.set_text(processed_text)  # 修改为正确的方法调用

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pdf_reader = PDFReader()
    pdf_reader.show()
    sys.exit(app.exec_())