from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import glob, os
import sys
import json 
import operator

os.chdir("./save")

def getData():
    headers = ["Değer"]
    f = open('gorunen/gorunenData.txt','r')
    text = f.read()
    data = json.loads(text)
    return headers, data

class Dialog(QDialog):
    sig_complete = Signal(dict)
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent=parent)
        self.data = []
        self.setGeometry(100,100,600,400)
        vLayout = QVBoxLayout(self)
        hLayout = QHBoxLayout()
        self.list = QListView(self)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.list)
        self.model = QStandardItemModel(self.list)
        self.list.setModel(self.model)
        for file in glob.glob("*.txt"):
            item = QStandardItem(file)
            item.setFont(QFont("Sanserif",50))
            print(item.text())
            self.model.appendRow(item)
            self.list.setIndexWidget(item.index(), self.buttonScreen(item))
        timer = QTimer(self)
        timer.timeout.connect(self.show_data)
        timer.start(1000)

    def show_data(self):
        self.model = QStandardItemModel(self.list)
        self.list.setModel(self.model)
        for file in glob.glob("*.txt"):
            item = QStandardItem(file)
            item.setFont(QFont("Sanserif",50))
            print(item.text())
            self.model.appendRow(item)
            self.list.setIndexWidget(item.index(), self.buttonScreen(item))
        
    def buttonScreen(self,item):
        self.button1 = QPushButton("SİL")
        self.button1.setMinimumHeight(60)
        self.button1.clicked.connect(self.kaldir(item))
        self.button = QPushButton("SEÇ")
        self.button.setMinimumHeight(60)
        self.button.clicked.connect(self.yazdir(item))
        lay = QHBoxLayout(self)
        lay.addStretch(0)
        lay.addWidget(self.button1)
        lay.addWidget(self.button, alignment=Qt.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)
        b=QGroupBox()
        b.setLayout(lay)
        return b
    
    def yazdir(self,item):
        def yazdirr():
            f = open(item.text(),"r")
            text= f.read()
            data = json.loads(text)
            f = open('gorunen/gorunenData.txt','w')
            f.write(str(data))
            self.accept()
        return yazdirr
    def kaldir(self,item):
        def kaldirr():
            userInfo = QMessageBox.question(self,"Bilgilendirme","Bu dosyayı silme istediğinizden emin misiniz?",QMessageBox.Yes | QMessageBox.No)
            if userInfo == QMessageBox.Yes:
                os.remove(item.text())
            elif userInfo == QMessageBox.No:
                pass
        return kaldirr
            
class Keyboard(QDialog):
    sig_complete = Signal(dict)
    def __init__(self, parent=None):
        super(Keyboard, self).__init__(parent=parent)
        self.setGeometry(100,100,600,400)
        vLayout = QVBoxLayout(self)
        hLayout = QHBoxLayout()
        self.girilenText = QLabel("")
        self.girilenText.setFont(QFont("Sanserif",25))
        self.girilenText.setMaximumHeight(60)
        groupBox = QGroupBox("Dosya adını giriniz:")
        groupBox.setFont(QFont("Sanserif",13))
        hLayout.addWidget(self.girilenText)
        groupBox.setLayout(hLayout)
        vLayout.addWidget(groupBox)
        vLayout.addLayout(self.keyboardGrid())
        

    def keyboardGrid(self):
        groupBox2 = QGroupBox()
        groupBox2.setFont(QFont("Sanserif",25))
        
        names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
                 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'bck',
                 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', 'ENTER']
        grid = QGridLayout()
        j = 0
        pos = [(0, 0), (0, 1), (0, 2), (0, 3),(0, 4), (0, 5), (0, 6), (0, 7),(0, 8), (0, 9),
               (1, 0), (1, 1), (1, 2), (1, 3),(1, 4), (1, 5), (1, 6), (1, 7),(1, 8), (1, 9),
               (2, 0), (2, 1), (2, 2), (2, 3),(2, 4), (2, 5), (2, 6), (2, 7),(2, 8), (2, 9),
               (3, 0), (3, 1), (3, 2), (3, 3),(3, 4), (3, 5), (3, 6), (3, 7),(3, 8), (3, 9)]
        for i in names:
            button = QPushButton(i)
            button.setFont(QFont("Sanserif",17))
            button.setMinimumHeight(60)
            if i == "bck":
                button = QPushButton()
                button.setMinimumHeight(60)
                button.setIcon(QIcon("img/bckspace.png"))
                button.setIconSize(QSize(20,20))
                #button.clicked.connect(self.textLabel(i))
            button.clicked.connect(self.textLabel(i))
            grid.addWidget(button, pos[j][0], pos[j][1])
            j = j + 1
        return grid
    def textLabel(self,i):
        def textWrite():
            if self.girilenText.text() == "0":
                self.girilenText.setText(i)
            else:
                self.girilenText.setText(self.girilenText.text() + i)
        def backSpace():
            old=len(self.girilenText.text())-1
            new=self.girilenText.text()[:old]
            self.girilenText.setText(new)
        def enter():
            f= open(self.girilenText.text()+".txt","w+")
            f.write("[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]")
            self.close()
        if i == 'bck':
            return backSpace
        elif i == "ENTER":
            return enter
        else:
            return textWrite
        
class Window(QWidget):
    girilen = 0
    eklee = 0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIYOTIN")
        #self.showFullScreen()
        self.setGeometry(300,300,1020,640)
        self.setIcon()
        self.girilenText = self.createText("0")
        self.anlikText = self.createText("90")
        self.tablee = self.createTable()
        self.createLayout()
    
    def createTable(self):
        header,data = getData()
        n = len(data)
        tablee = QTableWidget(n,1,self)
        header = QTableWidgetItem()
        header.setText("Konum")
        header.setFont(QFont("Sanserif",25))
        tablee.setHorizontalHeaderItem(0,header)
        tablee.setMinimumWidth(300)
        tablee.setEditTriggers(QTableWidget.NoEditTriggers)
        tablee.setFont(QFont("Sanserif",30))
        tablee.verticalHeader().setDefaultSectionSize(30)
        tablee.horizontalHeader().setDefaultSectionSize(160)
        tablee.verticalScrollBar().setStyleSheet("QScrollBar:vertical { width: 40px; }")
        tablee.setVerticalStepsPerItem(5)
        for i in range(n):
            tablee.setItem(i,0,QTableWidgetItem())
            tablee.item(i,0).setText(str(data[i]))
        return tablee

    def refreshTable(self):
        header,data = getData()
        n = len(data)
        for i in range(self.tablee.rowCount()):
            if i<=n:
                self.tablee.item(i,0).setText(str(data[i]))
            else:
                self.tablee.item(i,0).setText("0.0")
        

    def createText(self,i):
        text = QLabel("0")
        text.setFont(QFont("Sanserif",25))
        text.setMaximumHeight(60)
        return text
    def setIcon(self):
        appIcon = QIcon("img/cut.png")
        self.setWindowIcon(appIcon)   

    def quitApp(self):
        userInfo = QMessageBox.question(self,"Bilgilendirme","CIKMAK ISTIYORMUSUNUZ?",QMessageBox.Yes | QMessageBox.No)
        if userInfo == QMessageBox.Yes:
            myApp.quit()
        elif userInfo == QMessageBox.No:
            pass        
        
    def showDialog(self):
        items = [str(x) for x in range(10)]
        dial = Dialog()
        if dial.exec_() == QDialog.Accepted:
            self.refreshTable()

    def showKeyboard(self):
        key = Keyboard()
        key.exec_()

    def getDialogInfo(self,data_dict):
        self.a = data_dict["secilenData"]
        self.update()

    def createUpperLayout(self):
        groupBox = QGroupBox()
        groupBox2 = QGroupBox("Girilen Değer")
        groupBox3 = QGroupBox("Anlık Konum")
        groupBox.setFont(QFont("Sanserif",13))
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox.addWidget(self.girilenText)
        hbox3.addWidget(self.anlikText)
        groupBox2.setLayout(hbox)
        groupBox3.setLayout(hbox3)
        hbox2.addWidget(groupBox3)
        hbox2.addStretch()
        hbox2.addWidget(groupBox2)
        
        groupBox.setLayout(hbox2)
        
        return groupBox

    def createBottomLayout(self):
        groupBox = QGroupBox()
        groupBox.setFont(QFont("Sanserif",13))
        hbox = QHBoxLayout()
        button = QPushButton("Dosya Aç",self)
        button.setIcon(QIcon("img/openfolder.png"))
        button.clicked.connect(self.showDialog)
        button.setMinimumHeight(60)
        hbox.addWidget(button)

        button4 = QPushButton("Yeni Dosya",self)
        button4.setIcon(QIcon("img/newFile.png"))
        button4.setMinimumHeight(60)
        button4.clicked.connect(self.showKeyboard)
        hbox.addWidget(button4)

        button2 = QPushButton("Kaydet",self)
        button2.setIcon(QIcon("img/save.png"))
        button2.clicked.connect(self.textLabel("kaydet"))
        button2.setMinimumHeight(60)
        hbox.addWidget(button2)


        button6 = QPushButton("Ekle",self)
        button6.setIcon(QIcon("img/signs.png"))
        button6.clicked.connect(self.textLabel("ekle"))
        button6.setMinimumHeight(60)
        hbox.addWidget(button6)

        button1 = QPushButton("Değiştir",self)
        button1.setIcon(QIcon("img/change.png"))
        button1.clicked.connect(self.textLabel("degis"))
        button1.setMinimumHeight(60)
        hbox.addWidget(button1)

        button1 = QPushButton("Satır Sil",self)
        button1.setIcon(QIcon("img/cop.png"))
        button1.clicked.connect(self.textLabel("satirSil"))
        button1.setMinimumHeight(60)
        hbox.addWidget(button1)

        button5 = QPushButton("Kalibre",self)
        button5.setIcon(QIcon("img/caliber.png"))
        button5.setMinimumHeight(60)
        hbox.addWidget(button5)

        btn1 = QPushButton("Çıkış",self)
        btn1.clicked.connect(self.quitApp)
        btn1.setMinimumHeight(60)
        hbox.addWidget(btn1)
        groupBox.setLayout(hbox)
        return groupBox
    
    def createMidLayout(self):
        groupBox2 = QGroupBox()
        groupBox2.setFont(QFont("Sanserif",17))
        
        names = ['7', '8', '9', 'Sil',
                '4', '5', '6', 'bck', '1', '2', '3', 'Gönder',
                '','0', '.',  '']
        grid = QGridLayout()
        j = 0
        pos = [(0, 0), (0, 1), (0, 2), (0, 3),
                (1, 0), (1, 1), (1, 2), (1, 3),
                (2, 0), (2, 1), (2, 2), (2, 3),
                (3, 0), (3, 1), (3, 2), (3, 3 )]
        for i in names:
            if i == "bck":
                button = QPushButton()
                button.setMinimumHeight(60)
                button.setIcon(QIcon("img/bckspace.png"))
                button.setIconSize(QSize(20,20))
                button.clicked.connect(self.textLabel(i))
            elif i == "":
                pass
            elif i == "Gönder":
                pass
            else:
                button = QPushButton(i)
                button.setMinimumHeight(60)
                button.clicked.connect(self.textLabel(i))
            grid.addWidget(button, pos[j][0], pos[j][1])
            j = j + 1
        
        midYatay = QHBoxLayout()
        midSolDikey = QVBoxLayout()
        midOrtaDikey = QVBoxLayout()

        button1 = QPushButton(" İleri",self)
        button1.setIcon(QIcon("img/forward.png"))
        button1.setIconSize(QSize(50,50))
        button1.setMinimumHeight(60)
        button1.setMinimumWidth(120)
        midOrtaDikey.addWidget(button1)


        button2 = QPushButton("Geri",self)
        button2.setIcon(QIcon("img/backward.png"))
        button2.setIconSize(QSize(50,50))
        button2.setMinimumHeight(60)
        button2.setMinimumWidth(120)
        midOrtaDikey.addWidget(button2)

        button3 = QPushButton("Dur",self)
        button3.setIcon(QIcon("img/stop.png"))
        button3.setIconSize(QSize(50,50))
        button3.setMinimumHeight(60)
        button3.setMinimumWidth(120)
        midOrtaDikey.addWidget(button3)

        button4 = QPushButton("Başla",self)
        button4.setIcon(QIcon("img/cut.png"))
        button4.setIconSize(QSize(40,40))
        button4.setMinimumHeight(60)
        button4.setMinimumWidth(120)
        midOrtaDikey.addWidget(button4)


        
        
        midSolDikey.addWidget(self.tablee)
        
        #midOrtaDikey.addStretch()
        
        midYatay.addLayout(midSolDikey)
        midYatay.addStretch()
        midYatay.addLayout(midOrtaDikey)
        midYatay.addStretch()
        midYatay.addLayout(grid)
        
        groupBox2.setLayout(midYatay)
        return groupBox2

    def viewClicked(self, clickedIndex):
        row=clickedIndex.row()
        self.girilen = row

    def textLabel(self,i):
        def textWrite():
            if self.girilenText.text() == "0":
                self.girilenText.setText(i)
            else:
                self.girilenText.setText(self.girilenText.text() + i)
        def Sil():
            self.girilenText.setText("0")
        def backSpace():
            old=len(self.girilenText.text())-1
            new=self.girilenText.text()[:old]
            self.girilenText.setText(new)
            if new == "":
                self.girilenText.setText("0")
        def Degis():
            self.eklee = 1
            f = open('gorunen/gorunenData.txt','r')
            text = f.read()
            data = json.loads(text) 
            data[self.tablee.currentRow()] = float(self.girilenText.text())
            addData(data)
            #self.tablee.item(0,0).setText(self.girilenText.text())
            self.tablee.currentItem().setText(self.girilenText.text())
            self.girilenText.setText("0")

        def addData(data):
            f = open('gorunen/gorunenData.txt','w')
            f.write(str(data))
        
        def ekle():
            n = self.tablee.currentRow()+1
            self.tablee.insertRow(n)
            self.tablee.setItem(n,0,QTableWidgetItem())
            self.tablee.item(n,0).setText("0.0")
        
        def satirSil():
            row = self.tablee.currentRow()
            self.tablee.removeRow(row)

        def kaydet():
            data = []
            for i in range(self.tablee.rowCount()):
                data.append(float(self.tablee.item(i,0).text()))
            print(data)

        if i == "Sil":
            return Sil
        elif i == 'bck':
            return backSpace
        elif i == 'satirSil':
            return satirSil
        elif i == "degis":
            return Degis
        elif i == "ekle":
            return ekle
        elif i == "kaydet":
            return kaydet
        else:
            return textWrite

    def createLayout(self):
        
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.createUpperLayout())
        vbox.addStretch()
        vbox.addWidget(self.createMidLayout())
        vbox.addStretch()
        vbox.addWidget(self.createBottomLayout())
        self.setLayout(vbox)

myApp = QApplication(sys.argv)
window = Window()
window.show()
window.repaint()
window.update()
myApp.exec_()
sys.exit(0)

    