import cv2
import numpy as np
import ctypes
import json
import random
import sys
from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AppTray(QSystemTrayIcon):
    def __init__(self,icon,parent=None):
        #Initilaize Word Fetch Class
        self.app=App()
        #Create Menu
        menu=QMenu(parent)
        nextWordOption=QAction('Next Word')
        nextWordOption.triggered.connect(self.__next_word)

        setLearnedOption=QAction('Learned Word')

        actionsList=[nextWordOption,setLearnedOption]
        menu.addActions(actionsList)
        self.setContextMenu(menu)

    def __next_word(self):
        self.app.create_image(today=True)




class App:
    def __init__(self,jsonPath='./freewordlist.json',shuffle=True):
        loaded_data=None
        with open(jsonPath,'r') as words:
            loaded_data=json.load(words)
        self.data=loaded_data
        self.ScreenSize=self.__getScreenSize()

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
        width=max(self.ScreenSize)
        height=min(self.ScreenSize)
        line_padding=50
        base_word_pos=(width//2-10*(len(word)),height//2-100)
        base_type_pos=(base_word_pos[0]+10*len(word),base_word_pos[1]+line_padding)
        #base_def_pos=(base_word_pos[0]-10*len(word),base_word_pos[1]+line_padding*2)
        #base_def2_pos=(base_word_pos[0],base_word_pos[1]+line_padding*2)
        definiton="Once upon a time in nepal there was a man named kanchan .He was very good with whatever he did and was cool."
        brokenDefinitions=self.break_definiton(definiton)

        word_color=(0,255,0)
        type_color=(10,255,10)
        blank_image=np.zeros((height,width,3),dtype=np.uint8)
        cv2.putText(blank_image,word.upper(),base_word_pos,cv2.HISTCMP_BHATTACHARYYA,1,word_color,2,cv2.LINE_8)
        cv2.putText(blank_image,typeWord.capitalize(),base_type_pos,cv2.HISTCMP_BHATTACHARYYA,0.60,type_color,1,cv2.LINE_4)
        for gap,defPart in enumerate(brokenDefinitions):
            base_def_pos=(base_word_pos[0]-10*len(word),base_word_pos[1]+line_padding*(2+gap))
            cv2.putText(blank_image,definiton,base_def_pos,cv2.HISTCMP_BHATTACHARYYA,0.90,type_color,1,cv2.LINE_AA)

        #cv2.imwrite(f'./{word}.png',blank_image)
        #print("Image Saved")

    def break_definiton(self,definition):
        brokenDefs=[]
        splitDef=definition.strip(' ')
        splitDef=definition.split(' ')
        totalWords=len(splitDef)
        breakWordCount=5
        print(splitDef)
        breakParts=totalWords//breakWordCount
        print(breakParts)
        for i in range(0,breakParts):
            partDefine=splitDef[i*breakParts:breakWordCount]
            print(partDefine)
            finalPartDefine=' '.join(partDefine)
            brokenDefs.append(finalPartDefine)
        print(brokenDefs)
        return brokenDefs




def main():
    iconPath='./resources/icon.ico'
    app=QApplication(sys.argv)
    widget=QWidget()
    tray=AppTray(iconPath,widget)
    tray.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    app=App()
    print(app.get_todays_vocab())
    app.create_image()

