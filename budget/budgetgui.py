#budgetgui.py
#Written by Andrew Miller
#CIS 4930
#Spring 2015

import budget
import cal
import DataPlotting

import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *


import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

from PyQt4.QtGui import QWidget, QPushButton, QMainWindow, QMdiArea, QVBoxLayout, QApplication
from PyQt4.QtCore import Qt

from pylab import *
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QTAgg as NavigationToolbar)


class BudgetForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Super Mega Awesome Budget Pro v3.0')
        self.budget = budget.budget()
        self.create_main_frame()
        self.selected_date = self.budget.Get_today()
        self.months = ["none","January","Febuary","March","April","May","June","July","August","September","October","November","December",]
        self.graph_canvas = DataPlotting.DataPlotter()
    def create_main_frame(self):
        self.main_frame = QWidget()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        #Labels for input
        self.funclabel = QLabel('Function: ')
        self.vallabel = QLabel('Enter Value:   $')
        self.catlabel = QLabel('Modify Category: ')
		
        #info1rmational Text
        self.val = QLineEdit()
        self.info1 = QLabel('Info here')
        self.info2 = QLabel('')
        
        #Calendar Widget
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.clicked[QDate].connect(self.showDate)

        #ComboBoxes
        self.func = QComboBox()
        self.func.addItem("Add")
        self.func.addItem("Subtract")
        self.func.addItem("Set Cell")
        self.func.addItem("Reset Cell")
        self.func.addItem("Reset Date")
        self.func.addItem("Overall Total")
        self.func.addItem("Cat. Total")
        self.func.addItem("Cat. Total (month)")
        self.func.addItem("Cat. Percent")
        self.func.addItem("Cat. Percent (month)")
        self.func.addItem("Cat. Average")
        self.func.addItem("Cat. Average (month)")
        
        self.cat = QComboBox()
        cat_map = self.budget.Get_cat_map()
        for category in cat_map:
            if(category != "Day/Category"):
                self.cat.addItem(category)
		
        #submit button and date pick button
        self.subButton = QPushButton('Submit')
        self.subButton.clicked.connect(self.Perform_action)
        
        #self.dateButton = QPushButton('Pick Date')
        #self.dateButton.clicked.connect()
        test = cal.run_cal
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
        vbox1.addWidget(self.cal)
        vbox1.addLayout(self.funcbox)
        vbox1.addLayout(self.catbox)
        vbox1.addLayout(self.valbox)
        #vbox1.addWidget(self.dateButton)
        vbox1.addWidget(self.subButton)
		
        #vertical box for graph n shit
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.canvas)
		
        #horizontal box to push em together
        hbox = QHBoxLayout()
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox1)
		
        bottombox = QHBoxLayout()
        bottombox.addWidget(self.info1)
        bottombox.addWidget(self.info2)
		
        mainbox = QVBoxLayout()
        mainbox.addLayout(hbox)
        mainbox.addLayout(bottombox)
		
		
        #set main layout
        self.main_frame.setLayout(mainbox)
        self.setCentralWidget(self.main_frame)
        self.setGeometry(150, 150, 700, 250)
    
    def showDate(self, date):
        #self.funclabel.setText(date)
        self.selected_date = date.toPyDate()
        date_info = self.budget.Get_date_info(self.selected_date)
        print_line = date_info[0] + '\n' + date_info[1]
        print print_line
        self.info1.setText(print_line)
        return print_line
        #self.info2.setText(date_info[1])
    
    def Perform_action(self):
        function = str(self.func.currentText())
        category = str(self.cat.currentText())
        amount = float(self.val.text())
        
        if(function == "Add"):
            self.budget.AddTo(self.selected_date, category, amount)
        if(function == "Subtract"):
            self.budget.SubFrom(self.selected_date, category, amount)
        if(function == "Set Cell"):
            self.budget.Set_specific(self.selected_date, category, amount)
        if(function == "Reset Cell"):
            self.budget.Reset_cell(self.selected_date, category)
        if(function == "Reset Date"):
            self.budget.Reset_date(self.selected_date)
        if(function == "Overall Total"):
            self.info1.setText('Overall Total:  $' + str(self.budget.Total()))
        if(function == "Cat. Total"):
            self.info1.setText(category + 'Total:  $' + str(self.budget.Total_per_cat(category)))
        if(function == "Cat. Total (month)"):
            month_str = self.selected_date.strftime('%Y-%m-%d')
            month_str = self.months[int(month_str.split("-")[1])]
            amount_str = str(self.budget.Total_per_cat_per_month(category, self.selected_date))
            output_str = category + ' total for ' + month_str + ': $' + amount_str
            self.info1.setText(output_str)
        if(function == "Cat. Percent"):
            self.info1.setText(category + ' percentage overall: ' + str(self.budget.Percent_per_cat(category)) + '%')
        if(function == "Cat. Percent (month)"):
            month_str = self.selected_date.strftime('%Y-%m-%d')
            month_str = self.months[int(month_str.split("-")[1])]
            self.info1.setText(category + ' percentage for ' + month_str + ': ' + str(self.budget.Percent_per_cat_per_month(category, self.selected_date)) + '%')
        if(function == "Cat. Average"):
            self.info1.setText(category + ' average:  $' + str(self.budget.Avg_per_cat(category)))
        if(function == "Cat. Average (month)"):  
            month_str = self.selected_date.strftime('%Y-%m-%d')
            month_str = self.months[int(month_str.split("-")[1])]
            self.info1.setText(category + ' average for ' + month_str + ':  $' + str(self.budget.Average_per_cat_per_month(category, self.selected_date)))

app = QApplication(sys.argv)
form = BudgetForm()
form.show()
app.exec_()

		
		
		
