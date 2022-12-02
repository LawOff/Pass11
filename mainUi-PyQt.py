# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 21:39:50 2022

@author: Raghav
"""
import contextlib
import js2py, os, ctypes
import string, secrets
import sys, platform
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC
import PyQt6.QtGui as QtG
from algo import AlgoCheck

PATH = os.path.dirname(os.path.realpath(__file__))
default_path = os.getcwd()
result, tempfile = js2py.run_file("./assets/js/script.js")
Platform=sys.platform
Stylesheet=open("./assets/darkStylesheet.qss","r").read()
if Platform=="win32":
    dwm=ctypes.windll.Dwmapi
    DWMWA_USE_IMMERSIVE_DARK_MODE=20
    DWMWA_SYSTEMBACKDROP_TYPE = 38
    DWMWA_MICA_EFFECT=1029
    DWMWA_NCRENDERING_POLICY=2
    winBuild=platform.version().split('.')[2]
    class MARGINS_Struct(ctypes.Structure):
        _fields_ = [("cxLeftWidth", ctypes.c_int),
                ("cxRightWidth", ctypes.c_int),
                ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int)
                ]
    def ExtendFrameIntoClientArea(hWnd,left=1,right=1,top=1,bottom=1):
        margins = MARGINS_Struct(left,right,top,bottom)
        dwm.DwmExtendFrameIntoClientArea(hWnd, ctypes.byref(margins))
    def EnableDarkMode(hWnd,value=2):
        value=ctypes.c_int(value)
        dwm.DwmSetWindowAttribute(hWnd,
                                  ctypes.c_int(DWMWA_USE_IMMERSIVE_DARK_MODE),
                                  ctypes.byref(value),
                                  ctypes.sizeof(value))
    #
    def enableMica(hWnd):
        if int(winBuild) >= 22523:
            print("MICA_2")
            value=2
            value=ctypes.c_int(value)
            dwm.DwmSetWindowAttribute(hWnd,
                                      ctypes.c_int(DWMWA_SYSTEMBACKDROP_TYPE),
                                      ctypes.byref(value),
                                      ctypes.sizeof(value))
            ExtendFrameIntoClientArea(hWnd,-1)
        elif int(winBuild) >= 22100:
            print("MICA_1")
            value=1
            value=ctypes.c_int(value)
            dwm.DwmSetWindowAttribute(hWnd,
                                      ctypes.c_int(DWMWA_MICA_EFFECT),
                                      ctypes.byref(value),
                                      ctypes.sizeof(value))
            ExtendFrameIntoClientArea(hWnd,-1)
class MainWindow(QtW.QMainWindow):
    def __init__(self):
        super().__init__()
        #Setting Layout
        self.setStyleSheet(Stylesheet)
        centralWidget=QtW.QWidget()
        self.centralLayout=QtW.QVBoxLayout()
        centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(centralWidget)
        #
        self.pwdEnterLbl=QtW.QLabel(text="No Password Entered")
        self.centralLayout.addWidget(self.pwdEnterLbl,
                                     0,
                                     QtC.Qt.AlignmentFlag.AlignHCenter)
        #Password text field and side buttons
        pwdEnterLayout=QtW.QHBoxLayout()
        self.autoPwdBtn=QtW.QPushButton(text="")
        self.autoPwdBtn.clicked.connect(self.RandomPass)
        self.autoPwdBtn.setIcon(QtG.QIcon("./assets/load_image.svg"))
        pwdEnterLayout.addWidget(self.autoPwdBtn)
        self.pwdTxtBox=QtW.QLineEdit()
        self.pwdTxtBox.textChanged.connect(self.pwdEnter)
        pwdEnterLayout.addWidget(self.pwdTxtBox)
        self.showval=True
        self.hidePwdBtn=QtW.QPushButton(text="")
        self.hidePwdBtn.setIcon(QtG.QIcon("./assets/showeye_image.svg"))
        self.hidePwdBtn.setCheckable(True)
        self.hidePwdBtn.clicked.connect(self.hidePwd)
        pwdEnterLayout.addWidget(self.hidePwdBtn)
        self.centralLayout.addLayout(pwdEnterLayout)
        #Progress Bar
        self.progBar=QtW.QProgressBar()
        self.progBar.setTextVisible(False)
        self.centralLayout.addWidget(self.progBar)
        #time taken to crack text
        self.crackTime="0 Seconds"
        self.crackTxt=QtW.QLabel(text=f"Can be cracked in: {self.crackTime}")
        self.centralLayout.addWidget(self.crackTxt,
                                     0,
                                     QtC.Qt.AlignmentFlag.AlignHCenter)
        #
        pwdContainLayout=QtW.QHBoxLayout()
        expander=QtW.QWidget()
        pwdContainLayout.addWidget(expander,1)
        self.smallCaseChkLbl=QtW.QLabel()
        self.smallCaseChkLbl.setPixmap(QtG.QPixmap("./assets/lower_image.svg"))
        pwdContainLayout.addWidget(self.smallCaseChkLbl,
                                   0,
                                   QtC.Qt.AlignmentFlag.AlignHCenter)
        self.capsCaseChkLbl=QtW.QLabel()
        self.capsCaseChkLbl.setPixmap(QtG.QPixmap("./assets/upper_image.svg"))
        pwdContainLayout.addWidget(self.capsCaseChkLbl,
                                   0,
                                   QtC.Qt.AlignmentFlag.AlignHCenter)
        self.numberChkLbl=QtW.QLabel()
        self.numberChkLbl.setPixmap(QtG.QPixmap("./assets/number_image.svg"))
        pwdContainLayout.addWidget(self.numberChkLbl,
                                   0,
                                   QtC.Qt.AlignmentFlag.AlignHCenter)
        self.specialSymbolChkLbl=QtW.QLabel()
        self.specialSymbolChkLbl.setPixmap(QtG.QPixmap("./assets/special_image.svg"))
        pwdContainLayout.addWidget(self.specialSymbolChkLbl,
                                   0,
                                   QtC.Qt.AlignmentFlag.AlignHCenter)
        pwdContainLayout.addWidget(expander,1)
        self.centralLayout.addLayout(pwdContainLayout)
        #ProgressBar Animation
        self.progAnimator=QtC.QPropertyAnimation(self.progBar, b"value")
        self.progAnimator.setDuration(150)
        self.progAnimator.setEasingCurve(QtC.QEasingCurve.Type.OutExpo)
    
    def RandomPass(self):
        alphabet = string.ascii_letters + string.digits + "@$!%*?&"
        password = "".join(secrets.choice(alphabet) for _ in range(10))
        self.pwdTxtBox.setText(password)
    def progAnim(self,endVal):
        self.progAnimator.stop()
        self.progAnimator.setStartValue(self.progBar.value())
        self.progAnimator.setEndValue(endVal)
        self.progAnimator.start()
    def pwdEnter(self):
        global tempfile
        self.step = 0.01
        password = self.pwdTxtBox.text()
        res = AlgoCheck(password,tempfile)
        #print(res)
        self.value = int(res["nstrength"])/4
        self.progAnim(int(self.value*100))
        self.progBar.setStyleSheet(f"QProgressBar::chunk{{background:{res['color']} }}")
        with contextlib.suppress(Exception):
            if res["length"] > 0:
                self._setPass(res["strength"], res["time"])
            else:
                self._setPass("No Password Entered", res["time"])
            if res["lowercase"] == True:
                self.smallCaseChkLbl.setStyleSheet("background-color:#107C10")
            else:
                self.smallCaseChkLbl.setStyleSheet("background-color:none")
            if res["uppercase"] == True:
                self.capsCaseChkLbl.setStyleSheet("background-color:#107C10")
            else:
                self.capsCaseChkLbl.setStyleSheet("background-color:none")
            if res["numbers"] == True:
                self.numberChkLbl.setStyleSheet("background-color:#107C10")
            else:
                self.numberChkLbl.setStyleSheet("background-color:none")
            if res["special"] == True:
                self.specialSymbolChkLbl.setStyleSheet("background-color:#107C10")
            else:
                self.specialSymbolChkLbl.setStyleSheet("background-color:none")
    
    def _setPass(self, password, time):
        self.pwdEnterLbl.setText(password)
        self.crackTxt.setText(f"Can be cracked in: {time}")
    
    def hidePwd(self):
        if self.showval:
            self.showval = False
            self.hidePwdBtn.setIcon(QtG.QIcon("./assets/hideeye_image.svg"))
            self.pwdTxtBox.setEchoMode(QtW.QLineEdit.EchoMode.Password)
        else:
            self.showval = True
            self.hidePwdBtn.setIcon(QtG.QIcon("./assets/showeye_image.svg"))
            self.pwdTxtBox.setEchoMode(QtW.QLineEdit.EchoMode.Normal)

if __name__ == '__main__':
    app=QtW.QApplication(sys.argv)
    window=MainWindow()
    hWnd=int(window.winId())
    if Platform=="win32":
        EnableDarkMode(hWnd)
        enableMica(hWnd)
    else:
        window.setStyleSheet(window.styleSheet()+"QMainWindow{background:rgb(10,10,10);}")
    window.show()
    app.exec()
