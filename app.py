import cv2
import numpy as np
import ctypes,win32,os
import glob
import json
import random
import sys
from datetime import datetime
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class AppTray(QtWidgets.QSystemTrayIcon):
    def __init__(self,icon,parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self,icon,parent)
        self.setToolTip(f'Vocab Daily')
        #Initilaize Word Fetch Class
        self.app=App()
        print("Initialized")
        #Create Menu
        menu=QtWidgets.QMenu(parent)

        todayWordOption=menu.addAction("Today's Word")
        todayWordOption.triggered.connect(self.__todays_word)

        nextWordOption=menu.addAction('Next Word')
        nextWordOption.triggered.connect(self.__next_word)

        setLearnedOption=menu.addAction('Learned Word')
        self.setContextMenu(menu)

    def __todays_word(self):
        print('Today')
        if self.app.create_image(today=True):
            self.app.set_background()
            self.showMessage('Background Set',"Set")

    def __next_word(self):
        print("Next")
        if self.app.create_image(today=False):
            self.app.set_background()
            self.showMessage('Background Set',"Set")




class App:
    def __init__(self,jsonPath='./freewordlist.json',shuffle=True):
        loaded_data=None
        with open(jsonPath,'r') as words:
            loaded_data=json.load(words)
        self.data=loaded_data
        self.ScreenSize=self.__getScreenSize()
        self.current_word=None

    def __getScreenSize(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

    def get_todays_vocab(self,raw_segmented=True):
        seedDate=datetime.now()
        finalSeed=seedDate.strftime("%Y%m%d")
        random.seed(finalSeed)
        new_data=self.data
        random.shuffle(new_data)
        info=new_data[0]
        word,typeWord,definition=info.values()
        #formatData=f"{info['word'].upper()}\t{info['type']}\n{info['definition']}"
        if raw_segmented:
            return word,typeWord,definition
    def get_next_vocab(self):
        print(len(self.data))
        new_data=self.data
        random.seed(datetime.now())
        random.shuffle(new_data)
        info=new_data[0]
        word,typeWord,definition=info.values()
        return word,typeWord,definition



    def create_image(self,today=True):
        word,typeWord,definiton=self.get_next_vocab()
        if today:
            word,typeWord,definiton=self.get_todays_vocab()
        self.current_word=word
        width=max(self.ScreenSize)
        height=min(self.ScreenSize)
        line_padding=50
        base_word_pos=(width//2-10*(len(word)),height//2-100)
        base_type_pos=(base_word_pos[0]+10*len(word),base_word_pos[1]+line_padding)
        base_def_pos=(base_word_pos[0]-10*len(word),base_word_pos[1]+line_padding*2)
        word_color=(0,255,0)
        type_color=(10,255,10)
        blank_image=np.zeros((height,width,3),dtype=np.uint8)
        cv2.putText(blank_image,word.upper(),base_word_pos,cv2.HISTCMP_BHATTACHARYYA,1,word_color,2,cv2.LINE_8)
        cv2.putText(blank_image,typeWord.capitalize(),base_type_pos,cv2.HISTCMP_BHATTACHARYYA,0.60,type_color,1,cv2.LINE_4)
        cv2.putText(blank_image,definiton,base_def_pos,cv2.HISTCMP_BHATTACHARYYA,0.90,type_color,1,cv2.LINE_AA)
        path=os.makedirs('./temp/',exist_ok=True)
        for files in os.listdir('./temp/'):
            os.remove(os.path.join('./temp/',files))
        cv2.imwrite(f'./temp/{word}.png',blank_image)
        return True

    def set_background(self):
        imageName=f'{self.current_word}.png'
        filebasePath="\\".join(__file__.split('\\')[:-1])
        print(filebasePath)
        path=os.path.join(filebasePath,'temp',imageName)
        print(path)
        SPI_SET_WALLPAPER=20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SET_WALLPAPER, 0,path ,0)
        return

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

def main():
    iconPath='./resources/icon.ico'
    app=QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QWidget()
    tray_icon=AppTray(QtGui.QIcon(iconPath),widget)
    tray_icon.show()
    #tray_icon.showMessage('Vocab Daily','Controls for Vocab Daily Wallpapers')
    sys.exit(app.exec_())


if __name__ == "__main__":
    sys.excepthook = except_hook
    main()

