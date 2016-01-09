#!/opt/anaconda/bin/ipython
"""
Program minesweeper.py to implementacja znanej (i lubianej, nie?) gry Saper.
Szczegółowy opis działania aplikacji, wraz z instrukcją obsługi, znajduje się
 w pliku readme.txt.

autor: Lukasz Blaszczyk
modyfikacje: 9 stycznia 2016
"""

import sys
from PyQt4 import QtGui, QtCore
from minesweeper_gamecode import *

class MainApp(QtGui.QMainWindow):
    """
    Główna klasa aplikacji gry. Tworzy okno i umieszcza w nim odpowiednie
    przyciski i pozycje w menu.
    """
    bombsNumberRaisedSignal = QtCore.pyqtSignal()
    
    def __init__(self):
        """
        Konstruktor klasy MainApp, dziedziczącej po klasie QMainWindow.
        """
        super(MainApp, self).__init__()
        
        # zmienne używane w trakcie działania programu
        self.t = 0
        self.defaultLvl = 1
        self.customBoard = (20, 30, 145)
        
        self.smileyIcon = QtGui.QIcon()
        self.smileyIcon.addPixmap(QtGui.QPixmap("smiley.png"), 
                                  QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.normalIcon = QtGui.QIcon()
        self.normalIcon.addPixmap(QtGui.QPixmap("normal.png"), 
                                  QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sadIcon = QtGui.QIcon()
        self.sadIcon.addPixmap(QtGui.QPixmap("sad.png"), 
                                  QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bombIcon = QtGui.QIcon()
        self.bombIcon.addPixmap(QtGui.QPixmap("mine.png"), 
                                  QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.flagIcon = QtGui.QIcon()
        self.flagIcon.addPixmap(QtGui.QPixmap("flag.png"), 
                                  QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.emptyIcon = QtGui.QIcon()
        
        # podłączenie zegara odmierzającego czas gry
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        
        # ustawienie widgetow w oknie (wyniki /sc/ + gra /ex/)
        self.sc = ScoreGUI(self)
        dock = QtGui.QDockWidget(self)
        dock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        dock.setWidget(self.sc)
        dock.setFixedHeight(25)
        dock.setTitleBarWidget(QtGui.QWidget(None))
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock)
        
        self.ex = GameGUI(self) 
        self.setCentralWidget(self.ex) 
        self.windowWidth = 20*self.ex.ny+20
        self.windowHeight = 20*self.ex.nx+88
        self.sc.addNewGameButton()
        
        # utworzenie menu (File i Help)
        newGameAction = QtGui.QAction(QtGui.QIcon('new_game.png'), '&New game', self)
        newGameAction.setShortcut('Ctrl+N')
        newGameAction.setStatusTip('Start new game')
        newGameAction.triggered.connect(self.ex.newGame)
        
        optionsAction = QtGui.QAction(QtGui.QIcon('options.png'), '&Options', self)
        optionsAction.setShortcut('Ctrl+O')
        optionsAction.setStatusTip('Choose options')
        optionsAction.triggered.connect(self.openOptions)
        
        highScoresAction = QtGui.QAction(QtGui.QIcon('high_score.png'), '&High scores', self)
        highScoresAction.setShortcut('Ctrl+H')
        highScoresAction.setStatusTip('Show high scores')
        highScoresAction.triggered.connect(self.openHighScores)
        
        exitAction = QtGui.QAction(QtGui.QIcon('quit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        helpAction = QtGui.QAction(QtGui.QIcon('about.png'), '&Help', self)        
        helpAction.setShortcut('F1')
        helpAction.setStatusTip('Help')
        helpAction.triggered.connect(self.helpWindow)

        aboutAction = QtGui.QAction(QtGui.QIcon('info.png'), '&About', self)        
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('About the game')
        aboutAction.triggered.connect(self.aboutWindow)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newGameAction)
        fileMenu.addAction(highScoresAction)
        fileMenu.addAction(optionsAction)
        fileMenu.addAction(exitAction)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(helpAction)
        helpMenu.addAction(aboutAction)
        
        self.statusBar()

        self.setWindowTitle('MineSweeper')
        self.setWindowIcon(QtGui.QIcon('minesweeper.png'))        
        
    def updateTime(self):
        """
        Funkcja uaktualniająca na wyświetlaczu upływający czas gry.
        """
        self.t += 1
        self.sc.timer.display(str(int(self.t)))
    
    def openHighScores(self):
        """
        Funkcja otwierająca okienko z najlepszymi wynikami.
        """
        self.hs = HighScore()
        self.hs.setWindowTitle('High scores')
        self.hs.show()
    
    def highScoreBoard(self):
        """
        Funkcja highScoreBoard dopisuje do listy wyników (umieszczonej w pliku
        highscores.txt) wynik gry umieszczony w zmiennej t (w głównej klasie). 
        Wynik jest dopisywany pod warunkiem, że jest lepszy od najgorszego, 
        który znajduje się aktualnie w pliku. Wynik dopisywany jest do 
        kategorii gry znajdującej się w zmiennej defaultLvl i tylko jeśli jest
        to jeden z predefiniowanych wcześniej poziomów.
        """
        if self.defaultLvl < 4:
            f = open('highscores.txt','r')
            score = [f.readline().split(',')]
            for line in f:
                score = np.append(score,[line.split(',')],axis=0)
            f.close()
            
            relevantScores = [(score[0,(self.defaultLvl-1)*2], int(score[0,(self.defaultLvl-1)*2+1]))]
            for i in range(9):
                relevantScores = relevantScores+[(score[i+1,(self.defaultLvl-1)*2], int(score[i+1,(self.defaultLvl-1)*2+1]))]
            
            if relevantScores[9][1] > self.t:
                name, ok = QtGui.QInputDialog.getText(self, 'High score!','Enter your name:')
            
                if ok:
                    relevantScores = relevantScores+[(str(name),self.t)]
                    relevantScores = sorted(relevantScores, key=lambda x: x[1])
                    
                    rs = np.array(relevantScores)
                    rs = rs[:-1,:]
                    sc = np.insert(rs,[0],score[:,:(self.defaultLvl-1)*2],axis=1)
                    score = np.append(sc,score[:,(self.defaultLvl-1)*2+2:],axis=1)
                    f = open('highscores.txt','w')
                    for i in range(10):
                        score[i].tofile(f,sep=",")
                    f.close()
                    self.openHighScores()
    
    def openOptions(self):
        """
        Funkcja otwiera okno opcji gry.
        """
        self.w = OptionsMenu()
        self.w.board = self
        
        for i in range(4):
            self.w.options.button(i+1).setChecked(self.w.board.defaultLvl == i+1)
        
        for i in range(3):
            self.w.lne[i].setText(str(self.w.board.customBoard[i]))
        
        self.w.setGeometry(QtCore.QRect(100, 100, 300, 200))
        self.w.setWindowTitle('Options')
        self.w.show()
        
    def helpWindow(self):
        """
        Funkcja otwiera okno z instrukcją jak grać.
        """
        about = "Left clicking uncovers the contents of a given tile.\n" \
                "Right clicking marks a tile as a suspected bomb.\n" \
                "Numbers on tiles mean that there are that number of bombs touching that tile.\n" \
                "If you uncover the bomb, the game is over.\n" \
                "If you uncover all tiles without bombs, you win."
        QtGui.QMessageBox.about(self, "MineSweeper help", about)
            
    def aboutWindow(self):
        """
        Funkcja otwiera okno z informacjami o aplikacji.
        """
        about = "MineSweeper v1.0\n\n" \
                "author: Łukasz Błaszczyk\n" \
                "e-mail: L.Blaszczyk@ire.pw.edu.pl\n\n" \
                "release date: 11.01.2016"
        QtGui.QMessageBox.about(self, "About MineSweeper", about)
    
    
class HighScore(QtGui.QWidget):
    """
    Klasa odpowiadająca za okno z najlepszymi wynikami.
    """
    def __init__(self):
        """
        Konstruktor klasy HighScore, dziedziczącej po klasie QWidget.
        """
        QtGui.QWidget.__init__(self)
        
        layout = QtGui.QGridLayout()
        self.setLayout(layout)
        
        cbs = ('Beginner', 'Intermediate', 'Expert')
        cb = {}
        for i in range(3):
            cb[i] = QtGui.QLabel(cbs[i], self)
            cb[i].setFixedHeight(20)
            cb[i].setFixedWidth(120)
            layout.addWidget(cb[i], 1, 2*i+2, 1, 2)
        
        nb = {}
        for i in range(10):
            nb[i] = QtGui.QLabel(str(i+1)+'.', self)
            nb[i].setFixedHeight(20)
            nb[i].setFixedWidth(20)
            layout.addWidget(nb[i], i+2, 1)
            
        f = open('highscores.txt','r')
        scr = [f.readline().split(',')]
        for line in f:
            scr = np.append(scr,[line.split(',')],axis=0)
        f.close()
        
        self.score = {}
        for i in range(10):
            for j in range(6):
                self.score[(i,j)] = QtGui.QLabel(scr[i,j], self)
                self.score[(i,j)].setFixedHeight(20)
                self.score[(i,j)].setFixedWidth(30+ ((j+1) % 2)*20)
                layout.addWidget(self.score[(i,j)], i+2, j+2)
                
        btn1 = QtGui.QPushButton('Cancel', self)
        btn1.clicked.connect(self.close)
        layout.addWidget(btn1,12,2,1,3)
        
        btn2 = QtGui.QPushButton('Reset high scores', self)
        btn2.clicked.connect(self.resetScores)
        layout.addWidget(btn2,12,5,1,3)
        
    def resetScores(self):
        """
        Funkcja resetScores resetuje najlepsze wyniki ustawiając domyślnie
        nazwe użytkownika jako 'xyz' i wynik 999.
        """
        reply = QtGui.QMessageBox.question(self, 'Seriously?',
            "Are you sure you want to reset all high scores?", 
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
            QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            f = open('highscores.txt','w')
            score = np.array(['xyz','999','xyz','999','xyz','999','\n'])
            for i in range(10):
                score.tofile(f,sep=",")
                for j in range(3):
                    self.score[(i,2*j)].setText('xyz')
                    self.score[(i,2*j+1)].setText('999')
            f.close()
        else:
            self.close
                        
class OptionsMenu(QtGui.QWidget):
    """
    Klasa odpowiadająca za okno z opcjami gry.
    """
    def __init__(self):
        """
        Konstruktor klasy OptionsMenu, dziedziczącej po klasie QWidget.
        """
        QtGui.QWidget.__init__(self)
        
        layout = QtGui.QGridLayout()
        self.setLayout(layout)
        self.options = QtGui.QButtonGroup()
        
        cbs = ('Beginner', 'Intermediate', 'Expert', 'Custom')
        cb = {}
        for i in range(3):
            cb[i] = QtGui.QCheckBox(cbs[i], self)
            self.options.addButton(cb[i],i+1)
            layout.addWidget(cb[i],i+2,1)
        cb[3] = QtGui.QCheckBox(cbs[3], self)
        self.options.addButton(cb[3],4)
        layout.addWidget(cb[3],5,1,2,1)
        
        lbls = ( ('Height', 'Width', 'Mines'),
                 (     '9',     '9',    '10'),
                 (    '16',    '16',    '40'),
                 (    '16',    '30',    '99') )
        lbl = {}
        for i in range(3):
            for j in range(4):
                lbl[(i,j)] = QtGui.QLabel(lbls[j][i], self)
                lbl[(i,j)].setFixedHeight(20)
                lbl[(i,j)].setFixedWidth(60)
                layout.addWidget(lbl[(i,j)], j+1, i+2)
        
        self.lne = {}
        for i in range(3):
            self.lne[i] = QtGui.QLineEdit(self)
            layout.addWidget(self.lne[i],5,i+2)
        
        lnes = ('min. 1', 'min. 8', 'max. H*W-1')   
        lnel = {}
        for i in range(3):
            lnel[i] = QtGui.QLabel(lnes[i], self)
            lnel[i].setFixedHeight(20)
            lnel[i].setFixedWidth(60)
            layout.addWidget(lnel[i], 6, i+2)
        
        btn1 = QtGui.QPushButton('OK', self)
        btn1.clicked.connect(self.updateOptions)
        layout.addWidget(btn1,7,1,1,2)
        
        btn2 = QtGui.QPushButton('Cancel', self)
        btn2.clicked.connect(self.close)
        layout.addWidget(btn2,7,3,1,2)
    
    def updateOptions(self):
        """
        Funkcja aktualizuje opcje gry i resetuje planszę.
        """
        if self.options.checkedId() == 4:
            if  int(self.lne[1].text()) < 8:
                msgBox = QtGui.QMessageBox() ;
                msgBox.setText("Make it wider, ok?");
                msgBox.setWindowTitle(':(')
                msgBox.exec_();
                return None
            if int(self.lne[0].text()) < 1:
                msgBox = QtGui.QMessageBox() ;
                msgBox.setText("Make it higher, ok?");
                msgBox.setWindowTitle(':(')
                msgBox.exec_();
                return None
            if int(self.lne[0].text()) * int(self.lne[1].text()) <= int(self.lne[2].text()):
                msgBox = QtGui.QMessageBox() ;
                msgBox.setText("To many bombs, won't work...");
                msgBox.setWindowTitle(':(')
                msgBox.exec_();
                return None
            if int(self.lne[2].text()) < 1:
                msgBox = QtGui.QMessageBox() ;
                msgBox.setText("To few bombs, won't work...");
                msgBox.setWindowTitle(':(')
                msgBox.exec_();
                return None
        
        self.board.defaultLvl = self.options.checkedId()
        if self.options.checkedId() == 1:
            self.board.ex.nx = 9
            self.board.ex.ny = 9
            self.board.ex.nb = 10
        elif self.options.checkedId() == 2:
            self.board.ex.nx = 16
            self.board.ex.ny = 16
            self.board.ex.nb = 40
        elif self.options.checkedId() == 3:
            self.board.ex.nx = 16
            self.board.ex.ny = 30
            self.board.ex.nb = 99
        elif self.options.checkedId() == 4:
            self.board.ex.nx = int(self.lne[0].text())
            self.board.ex.ny = int(self.lne[1].text())
            self.board.ex.nb = int(self.lne[2].text())
            self.board.customBoard = (int(self.lne[0].text()), int(self.lne[1].text()), int(self.lne[2].text()))
        
        self.board.windowWidth = 20*self.board.ex.ny+20
        self.board.windowHeight = 20*self.board.ex.nx+88
        self.board.setFixedWidth(self.board.windowWidth)
        self.board.setFixedHeight(self.board.windowHeight)
        
        self.board.sc.newGame.move(self.board.windowWidth/2 - 13,1)
        self.board.sc.timer.move(self.board.windowWidth-self.board.sc.timer.width()-10, 1)
        self.board.ex.newGame()
        self.close()
        
class ScoreGUI(QtGui.QWidget):
    """
    Klasa odpowiadająca za wycinek głównego okna z opcjami gry.
    """
    def __init__(self, parent):
        """
        Konstruktor klasy ScoreGUI, dziedziczącej po klasie QWidget.
        """
        super(ScoreGUI, self).__init__(parent)
        self.board = parent
        
        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.resize(64,25)
        self.lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        palette = self.lcd.palette()
        palette.setColor(palette.WindowText, QtGui.QColor(0, 0, 0))
        self.lcd.setPalette(palette)

        self.timer = QtGui.QLCDNumber(self)
        self.timer.resize(64,25)
        self.timer.setSegmentStyle(QtGui.QLCDNumber.Flat)
        paletteT = self.timer.palette()
        paletteT.setColor(paletteT.WindowText, QtGui.QColor(0, 0, 0))
        self.timer.setPalette(paletteT)
        
        self.newGame = QtGui.QPushButton('', self)
        self.newGame.setFixedWidth(25)
        self.newGame.setFixedHeight(25)
        
    def addNewGameButton(self):
        """
        Funkcja dodaje funkcjonalność przycisku nowej gry.
        """
        self.lcd.move(10, 1)
        self.timer.move(self.board.windowWidth-74, 1)
        self.newGame.move(self.board.windowWidth/2 - 13,1)
        
        self.newGame.setIcon(self.board.normalIcon)
        
        self.newGame.clicked.connect(self.board.ex.newGame)
        self.show()
        
class GameGUI(QtGui.QWidget):
    """
    Klasa odpowiadająca za fragment okna z grą.
    """
    def __init__(self, parent):
        """
        Konstruktor klasy GameGUI, dziedziczącej po klasie QWidget.
        """
        super(GameGUI, self).__init__(parent)
        self.board = parent
        self.board.bombsNumberRaisedSignal.connect(self.updateLCD)
        
        self.layout = QtGui.QGridLayout()
        self.layout.setSpacing(0)
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 8))
        self.nx = 9
        self.ny = 9
        self.nb = 10
        
        self.newGame()
        
        self.setLayout(self.layout)
        self.board.setFixedWidth(20*self.ny+20)
        self.board.setFixedHeight(20*self.nx+88)
        
    def updateLCD(self):
        """
        Funkcja uaktualniająca na wyświetlaczu liczbę użytych flag.
        """
        self.board.sc.lcd.display(str(int(self.n)))
    
    def newGame(self):
        """
        Funkcja rozpoczynająca nową grę - tworzącą czystą planszę.
        """
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()
        self.board.timer.stop()
        self.n = 0
        self.clicks = 0
        self.board.bombsNumberRaisedSignal.emit()
        self.board.t = 0
        self.board.sc.timer.display(str(int(self.board.t)))
        self.board.sc.newGame.setIcon(self.board.normalIcon)
        
        self.S = Saper(self.nx,self.ny,self.nb)
        self.btn = {}
        for x in range(self.nx):
            for y in range(self.ny):
                self.btn[(x,y)] = QtGui.QPushButton('', self)
                self.btn[(x,y)].setStyleSheet("background-color: light gray")
                self.btn[(x,y)].setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
                self.btn[(x,y)].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.btn[(x,y)].x = x 
                self.btn[(x,y)].y = y
                self.btn[(x,y)].setFixedWidth(20)
                self.btn[(x,y)].setFixedHeight(20)
                self.btn[(x,y)].clicked.connect(self.leftButtonClicked)
                self.btn[(x,y)].customContextMenuRequested.connect(self.rightButtonClicked)
                self.layout.addWidget(self.btn[(x,y)], x, y)
    
    def leftButtonClicked(self):
        """
        Funkcja odpowiadająca za akcję lewego przycisku myszy.
        """
        sender = self.sender()
        self.S.LeftClick(self, sender)
        
    def rightButtonClicked(self):
        """
        Funkcja odpowiadająca za akcję prawego przycisku myszy.
        """
        sender = self.sender()
        self.S.RightClick(sender, self)
    
    def winningMessage(self):
        """
        Funkcja wyświetlająca komunikat o wygranej i zmieniająca ikonkę
        przycisku nowej gry.
        """
        self.board.sc.newGame.setIcon(self.board.smileyIcon)
        
        msgBox = QtGui.QMessageBox() ;
        msgBox.setText("Yaay! You win!");
        msgBox.setWindowTitle(':)')
        msgBox.exec_();
    
    def loosingMessage(self):
        """
        Funkcja wyświetlająca komunikat o przegranej i zmieniająca ikonkę
        przycisku nowej gry.
        """
        self.board.sc.newGame.setIcon(self.board.sadIcon)
        
        msgBox = QtGui.QMessageBox() ;
        msgBox.setText("Ooops... you lost!");
        msgBox.setWindowTitle(':(')
        msgBox.exec_();
     
def main():
    
    app = QtGui.QApplication(sys.argv)
    ap = MainApp()
    ap.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    