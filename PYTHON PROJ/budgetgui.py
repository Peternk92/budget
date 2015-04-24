#budgetgui.py
#Written by Andrew Miller
#CIS 4930
#Spring 2015

import budget
import cal

import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *


import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

class BudgetForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Super Mega Awesome Budget Pro v3.0')
        self.budget = budget.budget()
        self.create_main_frame()
	
    def create_main_frame(self):
        self.main_frame = QWidget()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
		
        #Labels for input
        self.funclabel = QLabel('Function: ')
        self.vallabel = QLabel('Enter Value: ')
        self.catlabel = QLabel('Modify Category: ')
		
        #Informational Text
        self.val = QLineEdit()
        self.temp = QLabel('Info will go here')

        #ComboBoxes
        self.func = QComboBox()
        self.func.addItem("Add")
        self.func.addItem("Subtract")
        self.func.addItem("Reset Cell")
        self.func.addItem("Reset Date")
        self.cat = QComboBox()
        cat_map = self.budget.Get_cat_map()
        for category in cat_map:
            if(category != "Day/Category"):
                self.cat.addItem(category)
		
        #submit button and date pick button
        self.subButton = QPushButton('Submit')
        
        self.dateButton = QPushButton('Pick Date')
        self.dateButton.clicked.connect(cal.run_cal)
        #Horizontal Boxes for the various label/input boxes
        self.funcbox = QHBoxLayout()
        self.valbox = QHBoxLayout()
        self.catbox = QHBoxLayout()
		
		#funcbox
        self.funcbox.addWidget(self.funclabel)
        self.funcbox.addWidget(self.func)
		
        #catbox
        self.catbox.addWidget(self.catlabel)
        self.catbox.addWidget(self.cat)
		
        #valbox
        self.valbox.addWidget(self.vallabel)
        self.valbox.addWidget(self.val)
		
        #vertical box for all user input
        vbox1 = QVBoxLayout()
        vbox1.addLayout(self.funcbox)
        vbox1.addLayout(self.catbox)
        vbox1.addLayout(self.valbox)
        vbox1.addWidget(self.dateButton)
        vbox1.addWidget(self.subButton)
		
        #vertical box for graph n shit
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.canvas)
		
        #horizontal box to push em together
        hbox = QHBoxLayout()
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox1)
		
        bottombox = QHBoxLayout()
        bottombox.addWidget(self.temp)
		
        mainbox = QVBoxLayout()
        mainbox.addLayout(hbox)
        mainbox.addLayout(bottombox)
		
		
        #set main layout
        self.main_frame.setLayout(mainbox)
        self.setCentralWidget(self.main_frame)
        self.setGeometry(150, 150, 700, 250)
		
app = QApplication(sys.argv)
form = BudgetForm()
form.show()
app.exec_()	
		
		
		
