#!/usr/bin/python
import sys
from PyQt4.QtGui import QWidget, QPushButton, QMainWindow, QMdiArea, QVBoxLayout, QApplication
from PyQt4.QtCore import Qt

from pylab import *
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QTAgg as NavigationToolbar)



class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        """
        """

        super(MyMainWindow,self).__init__(parent)
        self.setWidgets()

    def setWidgets(self, ):


        vBox = QVBoxLayout()
        mainFrame = QWidget()

        self._plotGraphButton = QPushButton("Plot Random Graph")
        self._plotGraphButton.clicked.connect(self.plotRandom)

        self._fig = figure(facecolor="white")
        self._ax = self._fig.add_subplot(111)

        self._canvas = FigureCanvas(self._fig)
        self._canvas.setParent(mainFrame)
        self._canvas.setFocusPolicy(Qt.StrongFocus)


        vBox.addWidget(self._plotGraphButton)
        vBox.addWidget(self._canvas)
        vBox.addWidget(NavigationToolbar(self._canvas,mainFrame))
        mainFrame.setLayout(vBox)
        self.setCentralWidget(mainFrame)

    def plotRandom(self, ):
        """
        """

        x = linspace(0,4*pi,1000)

        self._ax.plot(x,sin(2*pi*rand()*2*x),lw=2)
        self._canvas.draw()


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    MainWindow = MyMainWindow()

    MainWindow.show()
    sys.exit(qApp.exec_())
