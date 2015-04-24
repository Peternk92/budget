# NOTE: I've been using IDLE and Python v2.7.9

# Input File: data.csv
import sys
import csv
import collections
from operator import itemgetter

import math
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.axes as mplAxes
import matplotlib.cbook as cbook
import matplotlib.cm as cm
import matplotlib.collections as mplCollection
import matplotlib.colors as mplColors
import matplotlib.dates as mplDates
import matplotlib.ticker as ticker
        
csvFileName = 'data.csv'

class DataPlotter:
    
    def __init__( self ):
        self.dataList = []      # list of OrderedDict's
        self.totals_byField = collections.OrderedDict()    # last row of .csv file
        self.totals_byDate = collections.OrderedDict()
        self.readFile()
        self.init_Plot()

    def readFile( self ):
        csvFile = open( csvFileName, 'rb' )
        reader = csv.reader( csvFile )
        self.FieldList = reader.next()      # !!!

        for row in reader:
            ii = 0  # column number
            tempData = collections.OrderedDict()
            for cell in row:
                if ii!=0 and cell!='':          # not date, not blank
                    tempData[ self.FieldList[ii] ] = float(cell)
                elif ii != 0 and cell == '':    # not date, blank
                    tempData[ self.FieldList[ii] ] = cell
                elif ii==0:
                    try:                        # date
                        # date format: YYYY-MM-DD
                        tempData[ 'Date' ] = datetime.datetime.strptime( cell, '%Y-%m-%d' )
                    except ValueError,ex:       # totals @ eof
                        jj = 0
                        for xx in row:
                            if jj == 0:
                                pass
                            else:
                                self.totals_byField[ self.FieldList[jj] ] = float(xx)
                            jj = jj + 1
                ii = ii + 1
            self.dataList.append( tempData )
            # END --for--
        csvFile.close()
        self.correctFieldList()
        #self.calculateTotals()
        # END readFile()

    # ******************************** #
    # *   Add 'Day' and 'Month' to   * #
    # *      list of field names     * #
    # *** USED IN: self.readFile() *** #
    def correctFieldList( self ):
        temp = self.dataList[0].keys()
        self.FieldList = temp

    # ******************************************* #
    # * return list of YEARs within data range  * #
    # ******************************************* #
    # ----- USED IN: self.PLOT()>formatting ----- #
    def YearRange( self ):
        dates = self.getAttr( 'Date' )
        minYear = dates[0].year
        maxYear = dates[-1].year
        if minYear == maxYear:
            return minYear
        else:
            yrDif = maxYear - minYear
            tempYrList = [ minYear+yr for yr in range(yrDif+1) ]
            return tempYrList

    # ******************************* #
    # ******** GETTING LISTS ******** #
    # 'key': column/field name
    # return: list of values in column 'key'
    def getAttr( self, key, data=0 ):
        if data == 0:
            data = self.dataList
        itGet = itemgetter( key )
        return map( itGet, data )
    # return: list of column/field names (w/out date)
    def getColumnNames( self ):
        return self.FieldList[1:]


    # ****************************** #
    # ********** GRAPHING ********** #
    # ****************************** #
    # * 1. init_Plot()             * #
    # *     a. getFigData()        * #
    # *     b. init_LinePlot()     * #
    # *     c. format_LineFig()    * #
    # *     d. initLegend()        * #
    # * 2. Plot_Fig()              * #
    # ****************************** #
    # * In order to display plot,  * #
    # *      call function #2      * #
    # * (#1 is already called from * #
    # *  the __init__() function)  * #
    # ****************************** #

    # 1.
    def init_Plot( self ):
        # Create Figure 
        self.fig , self.ax = plt.subplots()
        self.ax.set_title( 'Super Mega-Awesome Budget Graph ' )
        self.ax.set_xlabel( 'Dates' )    # will be reset during formatting
        self.ax.set_ylabel( 'Amount', rotation='vertical' )
        self.ax.grid( True )
        
        self.getFigData()               # 1.a

        # Plot Data
        self.NN = len( self.xAxis )  # num x-axis entries
        ind = np.arange( self.NN )   # evenly spaced plot indices| range:(0,len(xx)]

        self.ax.autoscale(tight=True)
        
        self.init_LinePlot(ind)         # 1.b
        self.format_LineFig()           # 1.c
        self.initLegend()               # 1.d

    # 1.a
    def getFigData( self ):
        # for (X,Y)-Pairs
        self.XY = []
        # Get X-Axis Data
        self.xAxis = self.getAttr( 'Date' )
        # Get Y-Axis Data
        self.columns = self.getColumnNames()
        self.yAxis_lists = []   # each list elem == all values for one key/column
        for col in self.columns:
            self.yAxis_lists.append( self.getAttr(col) )

    # 1.b
    def init_LinePlot( self,ind ):
               
        ii = 0  # increment
        self.Lines = []
        for yy in self.yAxis_lists:
            ln = self.ax.plot( ind, yy, '1-', label=self.columns[ii], linewidth=2. )
            self.Lines = self.Lines + ln
            ii = ii+1

    # 1.c
    def format_LineFig( self ):
        # Create Custom Formatter
        def xAxis_formatter_noYear( x, pos=None ):
            thisInd = np.clip( int(x+0.5), 0, self.NN-1 )
            return self.xAxis[thisInd].strftime( '%m-%d' )
        def xAxis_formatter_Year( x, pos=None ):
            thisInd = np.clip( int(x+0.5), 0, self.NN-1 )
            return self.xAxis[thisInd].strftime( '%Y-%m-%d' )
        def yAxis_formatter( y, pos=None ):
            return '$%1.2f'%y
        
        # Apply Formatting
        plotYear = self.YearRange()
        if isinstance( plotYear, int ):
            self.ax.set_xlabel( 'Dates (%d)'%plotYear )
            self.ax.xaxis.set_major_formatter( ticker.FuncFormatter(xAxis_formatter_noYear) )
        else:
            self.ax.set_xlabel( 'Dates (%(aa)d-%(bb)d)'
                                %{'aa':plotYear[0],'bb':plotYear[1]} )
            self.ax.xaxis.set_major_formatter( ticker.FuncFormatter(xAxis_formatter_Year) )
            
        self.ax.yaxis.set_major_formatter( ticker.FuncFormatter(yAxis_formatter) )
        self.fig.autofmt_xdate()

    # 1.d
    def initLegend( self ):     # ** Clickable Legend ** #
        #self.lgnd = self.ax.legend( loc='upper right', fancybox=True )
        self.lgnd = self.ax.legend( bbox_to_anchor=(0,0,1,1),
                                    bbox_transform=plt.gcf().transFigure )
        self.lgnd.get_frame().set_alpha(0.4)
        
        # dict mapping legend-line to original-line
        lineDict = dict()
        for lgndLine,origLine in zip( self.lgnd.get_lines(), self.Lines ):
            lgndLine.set_picker(5)  # enable 'pick'ing (5 pt tolerance)
            lineDict[lgndLine] = origLine
            
        # define action to take for 'pick'
        def onpick( event ):
            # find origLine linked to lgndLine
            lgndLine = event.artist
            origLine = lineDict[ lgndLine ]
            # invert visibility
            visibility = not origLine.get_visible()
            origLine.set_visible( visibility )
            # make labels for visible lines stand out
            if visibility:
                lgndLine.set_alpha( 0.7 )
            else:
                lgndLine.set_alpha( 0.2 )
            # re-adjust y-axis & show changes
            self.ax.relim( visible_only=True )
            self.ax.autoscale_view( tight=True, scalex=False, scaley=True )
            self.fig.canvas.draw()

        self.fig.canvas.mpl_connect( 'pick_event',onpick )

    # 2.
    def Plot_Fig( self, type ):
        plt.show()




if __name__ == "__main__":
    stuff = DataPlotter()
    stuff.Plot_Fig('shit')
