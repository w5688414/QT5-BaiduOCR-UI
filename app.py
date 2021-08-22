import sys
import time
import random
from aip import AipOcr

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlQuery,QSqlDatabase
import glob
from Ui_ocrui import Ui_MainWindow
from PIL import Image
import time
from tqdm import tqdm 
import pandas as pd
# from configDialog import Ui_Dialog #暂时未使用


options = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }


def cut_image(im):
    # im = Image.open(img_path)  # 用PIL打开一个图片
    print(im.size)
    if(im.size[0]==1920):
        box = (80, 100, 360, 150)
        ng = im.crop(box) 

        ng.save('IMEI.png')

        box = (400, 160, 750, 200)
        ng = im.crop(box) 

        ng.save('time1.png')

        box = (450, 250, 650, 280)
        ng = im.crop(box) 

        ng.save('time2.png')

        box = (1050, 240, 1300, 280)
        ng = im.crop(box) 

        ng.save('mileage.png')

    else:
        box = (65, 80, 290, 100)
        ng = im.crop(box) 

        ng.save('IMEI.png')

        box = (300, 100, 600, 150)
        ng = im.crop(box) 

        ng.save('time1.png')

        box = (300, 200, 600, 240)
        ng = im.crop(box) 

        ng.save('time2.png')

        # # x1,y1,x2,y2
        box = (300, 240, 550, 260)
        ng = im.crop(box) 
        ng.save('mileage.png')

        box = (850, 200, 1100, 240)
        ng = im.crop(box) 

        ng.save('mileage1.png')



def judge(x):
    if(x['车牌']==x['车牌gt']):
        return "一致"
    else:
        return '不一致'

def judge_date(x):
    pred=x['播放时间'].split('-')
    pred=''.join(pred)
    if(pred==x['日期gt']):
        return "一致"
    else:
        return '不一致'

def merge_milestone(x):
    # print(x.columns)
    x1=x['里程数1']
    x2=x['里程数2']
    if('总里程' in x1):
        return x1
    else:
        return x2

def post_process(data_path):
    data=pd.read_csv(data_path)
    # data.rename(columns={'0':'image_path','1':'车牌','2':'开始时间','3':'结束时间','4':'播放时间'},inplace=True)
    data.rename(columns={'0':'image_path','1':'车牌','2':'开始时间','3':'结束时间','4':'播放时间','5':'里程数1','6':'里程数2'},inplace=True)
    

    print(data.head())
    data['播放时间']=data['播放时间'].apply(lambda x:x.replace('速度',""))
    data['开始时间']=data['开始时间'].apply(lambda x:x[:-5])
    data['IMEI']=data['车牌'].apply(lambda x:x.split(':')[1])
    data['IMEI']=data['IMEI'].apply(lambda x:x.split(')')[0])
    data['车牌']=data['车牌'].apply(lambda x:x.split('(')[0])

    data['车牌gt']=data['image_path'].apply(lambda x:x.split('-')[-2])
    data['日期gt']=data['image_path'].apply(lambda x:x.split('-')[-1])
    data['日期gt']=data['日期gt'].apply(lambda x:x.split('.')[-2])

    data['结束时间']=data['结束时间'].apply(lambda x:x[:-5])
    data['播放时间']=data['播放时间'].apply(lambda x:x[:10])
    data['里程数']=data.apply(lambda x:merge_milestone(x),axis=1)
    data['车牌号是否一致']=data.apply(lambda x:judge(x),axis=1)
    data['日期是否一致']=data.apply(lambda x:judge_date(x),axis=1)
    data=data.drop(columns=['7','车牌gt','日期gt', '里程数1', '里程数2'])
    # data.to_csv('test_process.csv',index=False)
    data.to_excel('result_process.xlsx',index=False)

class Ui_signin_Dialog(object):
    def setupUi(self, signin_Dialog):
        signin_Dialog.setObjectName("signin_Dialog")
        signin_Dialog.resize(400, 300)
        self.signin_buttonBox = QDialogButtonBox(signin_Dialog)
        self.signin_buttonBox.setGeometry(QRect(290, 230, 80, 56))
        self.signin_buttonBox.setOrientation(Qt.Vertical)
        self.signin_buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.signin_buttonBox.setObjectName("signin_buttonBox")

        self.plabel = QLabel(signin_Dialog)
        self.plabel.setEnabled(True)
        self.plabel.setGeometry(QRect(60, 100, 113, 25))
        self.plabel.setText("APP_ID")
        self.plabel.setObjectName("APPID")

        self.input_lineEdit = QLineEdit(signin_Dialog)
        self.input_lineEdit.setGeometry(QRect(140, 100, 113, 25))
        self.input_lineEdit.setObjectName("input_lineEdit")


        self.plabel1 = QLabel(signin_Dialog)
        self.plabel1.setEnabled(True)

        self.plabel1.setGeometry(QRect(60, 140, 113, 25))
        self.plabel1.setText("API_KEY")
        self.plabel1.setObjectName("API_KEY")

        self.input_lineEdit1 = QLineEdit(signin_Dialog)
        self.input_lineEdit1.setGeometry(QRect(140, 140, 113, 25))
        self.input_lineEdit1.setObjectName("input_lineEdit")

        self.plabel2 = QLabel(signin_Dialog)
        self.plabel2.setEnabled(True)
        self.plabel2.setGeometry(QRect(60, 180, 113, 25))
        self.plabel2.setText("SECRET_KEY")
        self.plabel2.setObjectName("SECRET_KEY")

        self.input_lineEdit2 = QLineEdit(signin_Dialog)
        self.input_lineEdit2.setGeometry(QRect(140, 180, 113, 25))
        self.input_lineEdit2.setObjectName("input_lineEdit")

        self.retranslateUi(signin_Dialog)
#        self.signin_buttonBox.accepted.connect(signin_Dialog.accept)           # ---
        self.signin_buttonBox.rejected.connect(signin_Dialog.reject)
        QMetaObject.connectSlotsByName(signin_Dialog)

    def retranslateUi(self, signin_Dialog):
        _translate = QCoreApplication.translate
        signin_Dialog.setWindowTitle(_translate("signin_Dialog", "Dialog"))

class SignIn(QDialog):

    def __init__(self, *args, **kwargs):
        """SignIn constructor."""
        super().__init__(*args, **kwargs)
        self.ui = Ui_signin_Dialog()
        self.ui.setupUi(self)
        self.APP_ID=''
        self.API_KEY=''
        self.SECRET_KEY=''
        # Connects the function that inputs data for sign in to the OK button.
        self.ui.signin_buttonBox.accepted.connect(self.sign_in_authenticate)

    def sign_in_authenticate(self):
        self.APP_ID = self.ui.input_lineEdit.text()
        self.API_KEY=self.ui.input_lineEdit1.text()
        self.SECRET_KEY=self.ui.input_lineEdit2.text()
        if self.APP_ID == "":
            QMessageBox.critical(self,"Note", "Please input your data.")
        else:                                                                   # +++
            self.accept()  

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.text = ""
        self.strTime = ""
        self.basicid = ""
        self.filePath = ""

        self.APP_ID = 'yourId'   #APP_ID
        self.API_KEY = 'yourKey'  #API_KEY
        self.SECRET_KEY =  'yoursecret'  #SECRET_KEY
        self.aipOcr = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def loadImage(self):
        # self.filePath,_ = QFileDialog.getOpenFileName(self,'打开文件','.','图像文件(*.png *.jpg *.jpeg)')
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        print(folderpath)
        self.filePaths=glob.glob(folderpath+'/*.*')
        img_ext=['png','bmp','jpg']
        self.filePaths=[item for item in self.filePaths if item.split('.')[-1] in img_ext]

        self.jpg = QtGui.QPixmap(self.filePaths[0]).scaled(self.plabel.width(), self.plabel.height())
        self.plabel.setPixmap(self.jpg)

    def recognize(self):
        if(len(self.filePaths) ==0):
            print(QMessageBox.warning(self, "错误", "没有找到图片", QMessageBox.Yes, QMessageBox.Yes))
            return
        # images=['IMEI.png','time1.png','time2.png','mileage.png']
        
        list_data=[]
        for file_path in tqdm(self.filePaths):
            im = Image.open(file_path) 
            cut_image(im)
            data=[file_path]
            if(im.size[0]==1920):
                images=['IMEI.png','time1.png','time2.png','mileage.png']
            else:
                images=['IMEI.png','time1.png','time2.png','mileage.png','mileage1.png']
            for image_path in images:
                time.sleep(1)
                result = self.aipOcr.basicAccurate(self.get_file_content(image_path), options)
                print(result)
                words_result = result['words_result']
                for i in range(len(words_result)):
                    data.append(words_result[i]['words'])
                    self.text = self.text + words_result[i]['words'] +'\n'
            list_data.append(data)
        print(list_data)
        df=pd.DataFrame(list_data)
        csv_path='result.csv'
        df.to_csv(csv_path,index=False)
        post_process(csv_path)
            
        self.tedit.setPlainText(self.text)
        self.tedit.repaint()    # 解决mac端文本无法显示的问题

        self.text = ''

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
            
    def cleanText(self):
        self.tedit.repaint()    # 解决mac端文本无法显示的问题

    def configApi(self):
        self.sigin = SignIn()
        # self.sigin.show()
        if self.sigin.exec_() ==QDialog.Accepted:
            if(self.sigin.APP_ID!=''):
                print(self.sigin.APP_ID)
                print(self.sigin.API_KEY)
                print(self.sigin.SECRET_KEY)
                self.APP_ID = self.sigin.APP_ID   #APP_ID
                self.API_KEY = self.sigin.API_KEY  #API_KEY
                self.SECRET_KEY =  self.sigin.SECRET_KEY  #SECRET_KEY
                self.aipOcr = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.sigin.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())