from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit,QWidget, QLayout, QSpacerItem, QSizePolicy,QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import numpy as np
import pandas as pd

class MainWindow (QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.tin_hieu_main = False
        self.tin_hieu_table = False
        self.gui_main()
        
        
    def gui_main(self):
        self.setWindowTitle("Numpy PMNMN")
        self.setGeometry(100, 100, 600, 400)

        self.label_toan = QLabel("Điểm toán")
        self.label_toan.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_toan.setMaximumSize(180, 40)
        self.edt_toan = QLineEdit()
        self.edt_toan.setMaximumSize(180, 40)
        
        self.label_van = QLabel("Điểm văn")
        self.label_van.setMaximumSize(180, 40)
        self.label_van.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edt_van = QLineEdit()
        self.edt_van.setMaximumSize(180, 40)
        
        self.btn_xn = QPushButton("Xác nhận")
        self.btn_xn.setMaximumSize(100, 50)
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setMaximumSize(100, 50)
        self.btn_import = QPushButton("Import")
        
        
        if self.tin_hieu_main == False:
            self.btn_xn.clicked.connect(self.xac_nhan_thong_tin)
            self.btn_clear.clicked.connect(self.clear_data)
            self.btn_import.clicked.connect(self.open_dialog_file)
            
            self.tin_hieu_main = True
        
        self.layoutBTN = QHBoxLayout()
        self.layoutBTN.addWidget(self.btn_xn)
        self.layoutBTN.addWidget(self.btn_clear)
        
        
        self.vLayoutInput = QVBoxLayout()
        
        self.vLayoutInput.setSpacing(1)
        self.vLayoutInput.addWidget(self.label_toan)
        self.vLayoutInput.addWidget(self.edt_toan)
        self.vLayoutInput.addWidget(self.label_van)
        self.vLayoutInput.addWidget(self.edt_van)
        self.vLayoutInput.addLayout(self.layoutBTN)
        self.vLayoutInput.addWidget(self.btn_import)
        
        # HSpace và VSpace dùng addItem
        
        self.Hspace = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.Vspace = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        
        self.hLayout = QHBoxLayout()
        self.hLayout.addItem(self.Hspace)
        #Layout dùng addlayout
        self.hLayout.addLayout(self.vLayoutInput)
        self.hLayout.addItem(self.Hspace)
        
        self.vLayoutFinal = QVBoxLayout()
        self.vLayoutFinal.setSpacing(1)
        self.vLayoutFinal.addItem(self.Vspace)
        self.vLayoutFinal.addLayout(self.hLayout)
        self.vLayoutFinal.addItem(self.Vspace)
        
        # Tạp một QWidget trung tâm
        self.central_widget = QWidget()
        
        self.central_widget.setLayout(self.vLayoutFinal)
        self.setCentralWidget(self.central_widget)
    
    def xac_nhan_thong_tin(self):
        diemToan = self.edt_toan.text()
        diemVan = self.edt_van.text()
        contentMess = f"Toán {diemToan} - Văn {diemVan}"
        self.show_message(contentMess)
        
        # if self.tin_hieu_table == True:
            
    
    def clear_data(self):
        self.edt_toan.clear()
        self.edt_van.clear()
        
    def show_message(self, content):
        # Tạo QMessageBox
        msg_box = QMessageBox()

        # Thiết lập tiêu đề và nội dung
        msg_box.setWindowTitle("Thông báo")
        msg_box.setText(str(content))
        msg_box.setIcon(QMessageBox.Icon.Question)  
        msg_box.exec()
    
    def show_table_widget(self, dataFrame):
        label = dataFrame.columns
        numberRow = len(dataFrame)
        numberColumn = len(label)
        self.HLayoutTable = QHBoxLayout()
        
        # Xóa bảng cũ nếu đã có
        if self.tin_hieu_table:
            self.HLayoutTable.removeWidget(self.qTable)
            self.tin_hieu_table = False
            
        self.qTable = QTableWidget(numberRow, numberColumn)
        self.qTable.setHorizontalHeaderLabels(label)
        
        for row in range (numberRow):
            for col in range (numberColumn):
                data_index = dataFrame.iloc[row][col]
                item = QTableWidgetItem(str(data_index))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa
                self.qTable.setItem(row, col, item)
                self.qTable.setColumnWidth(col, 100)
                
        total_width = numberColumn*100
        self.qTable.setFixedWidth(total_width)
        
        self.HLayoutTable.addItem(self.Hspace)
        self.HLayoutTable.addWidget(self.qTable)
        self.HLayoutTable.addItem(self.Hspace)
        self.vLayoutFinal.addLayout(self.HLayoutTable)
        self.vLayoutFinal.addItem(self.Vspace)
        self.tin_hieu_table = True
            
        
        
        
    def open_dialog_file(self):
        # Mở dialog chế độ chọn tệp
        filePath, _ = QFileDialog.getOpenFileName(self, "Chọn tệp")
        print('File đã chọn: ', filePath)
        filePath = filePath.replace("/", "//")
        
        lastPath = filePath.split(".")[-1]
        
        if lastPath == 'csv':
            data = pd.read_csv(filePath)
            if check_data_import(data) == True:
                self.show_table_widget(data)
            else:
                self.show_message("Chỉ có điểm Toán, Văn, TB")
        elif lastPath == "xlsx":
            data = pd.read_excel(filePath)
            if check_data_import(data) == True:
                self.show_table_widget(data)
            else:
                self.show_message("Chỉ có điểm Toán, Văn, TB")
            
            
        else:
            self.show_message("Không đúng file (xlsx, csv)")
            
def check_data_import(dataFrame):
    label = dataFrame.columns
    
    if len(label) != 3 or "Toán" not in label or "Văn" not in label or "TB" not in label:
        return False
    else:
        return True
    
        
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()