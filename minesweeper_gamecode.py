# -*- coding: utf-8 -*-
"""
Pakiet zawierający funkcje odpowiadające za "silnik" gry Saper.

autor: Lukasz Blaszczyk
modyfikacje: 9 stycznia 2016
"""
import numpy as np

class Saper:
    """
    Klasa odpowiadająca za grę Saper.
    """
    def __init__(self, Xsize, Ysize, BombCount):
        """
        Konstruktor klasy Saper, przyjmujący 3 argumenty - wymiary planszy
        oraz liczbę bomb. Zakłada się, że dane są poprawne.
        """        
        self.x = Xsize
        self.y = Ysize
        self.n = BombCount
        
        b_rand = np.random.choice(self.x * self.y, self.n, replace = False)
        self.bombs_coordinates = np.zeros([self.n, 2])
        self.bombs_matrix = np.zeros([self.x, self.y])
        self.neighbourhood = np.zeros([self.x, self.y])
        
        for i in range(self.n):
            x = b_rand[i] % self.x
            y = b_rand[i] // self.x
            self.bombs_coordinates[i, :] = np.array([x, y])
            self.bombs_matrix[x, y] = 1
            if x > 0:
                self.neighbourhood[x-1,y] += 1
                if y > 0:
                    self.neighbourhood[x-1,y-1] += 1
                if y < self.y-1:
                    self.neighbourhood[x-1,y+1] += 1
            if x < self.x-1:
                self.neighbourhood[x+1,y] += 1
                if y > 0:
                    self.neighbourhood[x+1,y-1] += 1
                if y < self.y-1:
                    self.neighbourhood[x+1,y+1] += 1
            if y > 0:
                self.neighbourhood[x,y-1] += 1
            if y < self.y-1:
                self.neighbourhood[x,y+1] += 1
                
        self.uncovered = np.zeros([self.x, self.y])
        self.expected = np.zeros([self.x, self.y])
        
        self.neighbours_colors = { 1: "(  0,  0,204)",
                                   2: "(  0,102, 51)",
                                   3: "(255,128,  0)",
                                   4: "(255, 51, 51)",
                                   5: "(153,  0,153)",
                                   6: "(255,255,  0)",
                                   7: "(255, 51,153)",
                                   8: "(  0,  0,  0)"}
    
    def RevealZero(self, board, Xc, Yc):
        """
        Funkcja odkrywająca na planszy pole o współrzędnych Xc,Yc, które nie
        zawiera bomby, a więc odkrywająca również wszystkie pola wokół.
        """
        board.btn[(Xc,Yc)].setText('')
        board.btn[(Xc,Yc)].setStyleSheet("background-color: rgba(192,192,192)")
        board.btn[(Xc,Yc)].setDisabled(True)
        self.uncovered[Xc, Yc] = 1
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if (Xc + i >= 0) and (Xc + i <= self.x-1) and (Yc + j >= 0) and (Yc + j <= self.y-1) and self.uncovered[Xc+i,Yc+j] == 0 and not(i == 0 and j == 0):
                    if self.neighbourhood[Xc+i,Yc+j] == 0:
                        self.RevealZero(board, Xc+i, Yc+j)
                    else:
                        board.btn[(Xc+i,Yc+j)].setText(str(int(self.neighbourhood[Xc+i, Yc+j])))
                        color = self.neighbours_colors[int(self.neighbourhood[Xc+i, Yc+j])]
                        board.btn[(Xc+i,Yc+j)].setStyleSheet("background-color: rgba(192,192,192); color: rgba"+color)
                        board.btn[(Xc+i,Yc+j)].setDisabled(True)
                        self.uncovered[Xc+i,Yc+j] = 1
                    
    def gameOver(self, board):
        """
        Funkcja kończąc grę, w przypadku przegranej (wyłączenie planszy)
        """
        for x in range(self.x):
            for y in range(self.y):
                board.btn[(x,y)].setDisabled(True)
                if self.bombs_matrix[x, y] == 1:
                    board.btn[(x,y)].setIcon(board.board.bombIcon)
                    board.btn[(x,y)].setStyleSheet("background-color: rgba(204,0,0); color: white")
                elif self.uncovered[x,y] == 0:
                    board.btn[(x,y)].setStyleSheet("background-color: light gray")
                
    def gameWin(self, board):
        """
        Funkcja kończąc grę, w przypadku wygranej (wyłączenie planszy)
        """
        for x in range(self.x):
            for y in range(self.y):
                if self.uncovered[x,y] == 0:
                    board.btn[(x,y)].setStyleSheet("background-color: rgba(255,255,153)")
                    board.btn[(x,y)].setIcon(board.board.flagIcon)
                    board.btn[(x,y)].setDisabled(True)
                
    def LeftClick(self, board, sender):
        """
        Funkcja odpowiadająca za działanie lewego przycisku myszy, dla danego
        pola na planszy. Jeśli jest to pierwsze kliknięcie w grze - uruchamia
        zegar gry.
        """
        if board.clicks == 0:
            board.board.timer.start(1000)
        board.clicks += 1
        
        Xc = sender.x
        Yc = sender.y
        sender.setDisabled(True)
        sender.setIcon(board.board.emptyIcon)
        
        if self.bombs_matrix[Xc, Yc] == 1:
            board.board.timer.stop()
            sender.setIcon(board.board.bombIcon)
            sender.setStyleSheet("background-color: rgba(204,0,0); color: white")
            self.gameOver(board)
            board.loosingMessage()
            
 
        elif self.uncovered[Xc,Yc] == 0 and self.neighbourhood[Xc, Yc] > 0:
            sender.setText(str(int(self.neighbourhood[Xc, Yc])))
            color = self.neighbours_colors[int(self.neighbourhood[Xc, Yc])]
            sender.setStyleSheet("background-color: rgba(192,192,192); color: rgba"+color)
            self.uncovered[Xc, Yc] = 1
            
        elif self.uncovered[Xc,Yc] == 0 and self.neighbourhood[Xc, Yc] == 0:
            self.RevealZero(board, Xc, Yc)
        self.CheckIfWin(board)
    
    def RightClick(self, sender, board):
        """
        Funkcja odpowiadająca za działanie prawego przycisku myszy, dla danego
        pola na planszy. Jeśli jest to pierwsze kliknięcie w grze - uruchamia
        zegar gry.
        """
        if board.clicks == 0:
            board.board.timer.start(1000)
        board.clicks += 1
        Xc = sender.x
        Yc = sender.y
        if self.uncovered[Xc, Yc] == 0:
            if self.expected[Xc, Yc] == 1:
                sender.setText('')
                sender.setStyleSheet("background-color: light gray")
                sender.setIcon(board.board.emptyIcon)
                self.expected[Xc, Yc] = 0
                board.n -= 1
                board.board.bombsNumberRaisedSignal.emit()
            else:
                sender.setText('')
                sender.setStyleSheet("background-color: rgba(255,255,153)")
                sender.setIcon(board.board.flagIcon)
                self.expected[Xc, Yc] = 1
                board.n += 1
                board.board.bombsNumberRaisedSignal.emit()
                
    def CheckIfWin(self, board):
        """
        Funkcja sprawdzająca, czy dany układ na planszy odpowiada wygranej.
        """
        if self.uncovered.sum() == self.x * self.y - self.n:
            board.board.timer.stop()
            self.gameWin(board)
            board.winningMessage()
            board.board.highScoreBoard()