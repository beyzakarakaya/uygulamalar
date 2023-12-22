import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget,QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView
from ast import Index
import enum

from PyQt5.QtGui import QPixmap
from uzanti import Ui_MainWindow
from uzanti import*
from PyQt5 import QtGui



import sqlite3
baglanti = sqlite3.connect("kayit2.db")
islem = baglanti.cursor()
baglanti.commit()

table = islem.execute("Create Table If Not Exists Kayit2(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, marka text, adet text, fiyat text, tarih text, tur text, depo text)")
baglanti.commit()



class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()


        self.setupUi(self)
        self.label7.setPixmap(QPixmap("logo.png"))
        # self.pushButton1.clicked.connect(self.kayit_ekle)
        # self.loaddata()
        # self.kayit_listele()
        self.pushButton3.clicked.connect(lambda: self.kayit_sil())  
        self.pushButton1.clicked.connect(lambda: self.kayit_ekle())
        self.pushButton2.clicked.connect(lambda: self.kayit_listele())
       
        self.kayit_listele()
        


    def kayit_ekle(self):
        marka = self.lineEdit1.text()
        adet = self.lineEdit2.text() 
        fiyat = self.lineEdit3.text()
        tarih = self.lineEdit4.text()
        tur = "a"
        if self.radioButton1.isChecked():
            tur = "ithal"
        elif self.radioButton2.isChecked():
            tur = "yerel"
        else:
            tur = "Diger"

        depo = self.lineEdit_5.text()

        try:
            ekle = ('''INSERT INTO kayit2(marka, adet, fiyat, tarih, tur, depo) VALUES (?,?,?,?,?,?)''')
            # islem.execute(ekle, marka, adet, fiyat, tarih, tarih, depo)
            islem.execute(ekle, (marka, adet, fiyat, tarih, tur, depo))
            baglanti.commit()
            self.statusbar.showMessage("Kayit eklendi", 10000)

        except Exception as e:
            self.statusbar.showMessage(f"Hata: {str(e)}", 10000)
        self.kayit_listele()


    def kayit_sil(self):
        
        sil_mesaj = QMessageBox.question(self, "Silme onayi", "Silmek istediginize emin misiniz?")
        QMessageBox.Yes |QMessageBox.No 

        if sil_mesaj == QMessageBox.Yes:
            secilen_kayit = self.tbl1.selectedItems()     
            silinecek_kayit = secilen_kayit[0].text()
            
            secilen_satir = self.tbl1.currentRow()
            if secilen_satir >= 0:  
                marka = self.tbl1.item(secilen_satir, 0).text()     
                sorgu = "DELETE FROM Kayit2 WHERE ID = ?"

                try:
                    islem.execute(sorgu, (silinecek_kayit,))
                    baglanti.commit()
                    self.statusbar.showMessage("Kayit silindi", 10000)
                    # self.loaddata()
                    
                except:
                    self.statusbar.showMessage("Kayit silinemedi", 10000)
                # self.loaddata()
            else:
                self.statusbar.showMessage("Lütfen bir satir seçin", 10000)

        else:
            self.statusbar.showMessage("İslem iptal", 10000)

        
        # self.tbl1.clearSelection()
        self.kayit_listele()



    # def loaddata(self):
    #     self.tbl1.clearContents()
    #     sqlquery = "SELECT * FROM Kayit2"
    #     tableRow = 0
    #     for row in islem.execute(sqlquery):
    #         self.tbl1.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(row[0]))
    #         self.tbl1.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(row[1]))
    #         self.tbl1.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row[2]))
    #         self.tbl1.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(row[3]))
    #         self.tbl1.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(row[4]))
    #         self.tbl1.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(row[5]))
    #         self.tbl1.setItem(tableRow, 6, QtWidgets.QTableWidgetItem(row[6]))
            

    #         tableRow+=1
    #         baglanti.commit()
            
           

    def kayit_listele(self):
        self.tbl1.clearContents()
        self.tbl1.setRowCount(0)

        self.tbl1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl1.setHorizontalHeaderLabels(("ID", "marka", "adet", "fiyat", "tarih", "tur","depo"))

        sorgu = "SELECT * FROM kayit2"
        islem.execute(sorgu)

        for indexSatir, satirVerisi in enumerate(islem.fetchall()):
            self.tbl1.insertRow(indexSatir)
            for indexSutun, deger in enumerate(satirVerisi):
                self.tbl1.setItem(indexSatir, indexSutun, QTableWidgetItem(str(deger)))

    
        # # self.tbl1.setHorizontalHeaderLabels(("marka","adet","fiyat","tarih","tur","depo"))
        # # sorgu = "SELECT * from Kayit"
        # # islem.execute(sorgu)
    
    
        #     # for indexSatir, kayitNumarasi in enumerate(islem):        me
        #     #     for indexSutun, kayitSutun in enumerate(kayitNumarasi):
        #     #         self.tbl1.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))  
        #     for indexSatir, kayitNumarasi in enumerate(islem.fetchall()):     
        #         self.tbl1.insertRow(indexSatir)
        #         for indexSutun, kayitSutun in enumerate(kayitNumarasi):
        #             self.tbl1.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))  

           
    


def app():
    app=QtWidgets.QApplication(sys.argv)
    win=Window()
    win.show()
    sys.exit(app.exec_())
    
app()