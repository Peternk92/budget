# Input File: data.csv
import sys
import csv
import collections
from operator import itemgetter
#import collections.OrderedDict() as oDict

import math
import numpy as np
import matplotlib.pyplot as plt
import datetime
#import dateutil.relativedelta as dateDelta
#import dateutil.rrule as dateRule
import matplotlib.axes as mplAxes
import matplotlib.cbook as cbook
import matplotlib.cm as cm
import matplotlib.collections as mplCollection
import matplotlib.colors as mplColors
import matplotlib.dates as mplDates
import matplotlib.ticker as ticker


        
csvFileName = 'data.csv'
class DataPlotter:

    Months = mplDates.MonthLocator() # every month
    Days = mplDates.DayLocator()     # every day
    
    def __init__( self ):
        self.dataList = []      # list of OrderedDict's
        self.totals_byField = collections.OrderedDict()    # last row of .csv file
        self.totals_byDate = collections.OrderedDict()
        self.readFile()
        #self.init_Plot()

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
        self.calculateTotals()
        # END readFile()

    # ******************************** #
    # *   Add 'Day' and 'Month' to   * #
    # *      list of field names     * #
    # *** USED IN: self.readFile() *** #
    def correctFieldList( self ):
        temp = self.dataList[0].keys()
        self.FieldList = temp

    # ************************************** #
    # * If no 'Totals' Line at end of file * #
    # *  calculate totals for each column  * #
    def calculateTotals( self ):
        # FIELDS -- columns
        #if not self.totals_byField:
        dataFields = self.getColumnNames()
        for col in dataFields:
            tempList = self.getAttr( col )
            self.totals_byField[ col ] = float( math.fsum(tempList) )
        # DATES -- rows
        dataDates = self.getAttr( 'Date' )
        for date in dataDates:
            tempVals = self.getRowValsByDate( date )
            self.totals_byDate[ date ] = float( math.fsum(tempVals) )
            
            
        

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
            tempYrList = [ datetime.datetime(minYear+yr,1,1,0,0) for yr in range(yrDif+1) ]
            return tempYrList

    # ******************************************* #
    # * return list of MONTHs within data range * #
    # ******************************************* #
    def MonthRange( self ):
        dates = self.getAttr( 'Date' )
        yr0 = dates[0].year
        mo0 = dates[0].month
        yr1 = dates[-1].year
        mo1 = dates[-1].month
        monthRange = []
        if yr0 == yr1:          # within same year
            dif = mo1 - mo0
            monthRange = [datetime.datetime( yr0, mo0+mm_, 1,0,0 ) for mm_ in range(dif)]
        else:
            yrRange = self.YearRange()
            yrDif = yrRange[-1] - yrRange[0]
            rng = 12 - mo0          # 1. yr0,mo0 -> yr0,12
            for mm_ in range(rng+1):
                monthRange.append( datetime.datetime( yr0, mo0+mm_, 1,0,0 ) )
            if yrDif.days > 365:           # 2. yr0+ii,01 -> yr0+ii,12  for ii<yr1
                for yr_ in range( yrDif-1 ):
                    for mm_ in range(12):
                        tmp = datetime.datetime( yr_, mm_+1, 1,0,0 )
                        monthRange.append( tmp )
            for mm_ in range(mo1):  # 3. yr1,01 -> yr1,mo1
                monthRange.append( datetime.datetime( yr1, mm_+1, 1,0,0 ) )

        return monthRange

        

    # xScale: [DAY|MONTH|YEAR|ALL]      #
    # yScale: [SUM|AVERAGE|percent]     #
    # returns: list[list[(X,Y)]] tuples #
    def getXYData( self, xScale, yScale ):
        # Get X-Data, Calculate Y-Values
        if xScale=='MONTH':
            xxList= self.MonthRange()       # [month [column [ a,b,[nums] ] ] ]
            yyLists = self.getAttrDict_byMonth(xxList)
        elif xScale=='YEAR':
            xxList = self.YearRange()       # [year [column ([a,b,[nums] ] ] ]
            yyLists = self.getAttrDict_byYear(xxList)
        elif xScale=='DAY' or scale=='ALL':
            self.getFigData()
            return
        else:
            print '--- You Will Die Cold & Alone ---'
            sys.exit(1)

        # Calculate Y-Data
        if yScale=='SUM':
            yyLists = self.getSum( yyLists )
        elif yScale=='AVERAGE':
            yyLists = self.getAverage( yyLists )

        # More Y-Data Container Formatting
        col = self.getColumnNames()
        self.xAxis = xxList
        self.XY_lists = []
        for cc in col:  # each line on graph
            tmp = []
            ii = 0  # iterating through xxAxis
            for yy in yyLists:
                for zz in yy:
                    if zz[0]==cc:
                        tmpDict = {'Column':cc,
                                   'xDate':xxList[ii],
                                   'yNumber':zz[2]}
                        tmp = tmp + [tmpDict]
                ii = ii + 1
            self.XY_lists.append( tmp )
        # self.XY_lists == for each column:[ (Column,Month,Num) ]

        # Get Y Data
        self.yAxis_lists = []
        for xy in self.XY_lists:
            getY = itemgetter( 'yNumber' )
            tmpY = map( getY,xy )
            self.yAxis_lists.append( tmpY )
        

    def graphStuff( self ):
        self.Lines = []
        ii = 0
        columns = self.getColumnNames()
        for yy in self.yAxis_lists:
            ln = self.ax.plot( self.ind, yy, '1-', label=columns[ii], linewidth=2. )
            self.Lines = self.Lines + ln
            ii = ii + 1

    def getSum( self,yLists ):
        # for MONTH:
        #   yLists == [ month[ column( a,b,nums ) ] ]
        sumLists = []
        for xScale in yLists:
            tmpList = []
            for column in xScale:
                tmp = math.fsum(column[2])
                tmpList.append( [column[0],column[1],tmp] )
            sumLists.append( tmpList )
        return sumLists
                
    def getPercentage( self,yLists ):
        pass
    def getAverage( self,yLists ):
        aveLists = []
        sumLists = self.getSum( yLists )
        ii = 0
        for xScale in sumLists:
            tmpList = []
            jj = 0
            for column in xScale:
                tmp = column[2] / float( len(yLists[ii][jj]) )
                tmpList.append( [column[0],column[1],tmp] )
                jj = jj + 1
            aveLists.append( tmpList )
            ii = ii + 1
#        for x in sumLists:
#            print x,'\n'
#        print '\n\n\n'
#        for x in aveLists:
#            print x,'\n'
        return aveLists

    def getAttrDict_byDay( self ):
        listByDay = []
        for row in self.dataList:
            tmp = []
            tmpDate = row[ 'Date' ]
            for kk,vv in row.items():
                if kk=='Date':
                    pass
                else:
                    tmp.append( [kk,tmpDate,[vv]] )
            listByDay.append( tmp )
        return listByDay
    def getAttrDict_byMonth( self, xRange ):
        col = self.getColumnNames()
        listByMonth = []
        for mm in xRange:
            tmp = []
            mRows = self.getRowsByMonth( mm.month )
            for cc in col:
                tmpData = self.getAttr(cc,mRows)
                tmpMonth = mm #[mm for x in range( len(tmpData) )]
                tmpCol = cc #[cc for x in range( len(tmpData) )]
                tmp.append( [tmpCol,tmpMonth,tmpData] )
            listByMonth.append( tmp )
        return listByMonth
    def getAttrDict_byYear( self, xRange ):
        col = self.getColumnNames()
        listByYear = []
        for yr in xRange:
            tmp = []
            yrRows = self.getRowsByYear( yr.year )
            for cc in col:
                tmpData = self.getAttr(cc,yrRows)
                tmpYear = yr #[yr for x in range( len(tmpData) )]
                tmpCol = cc #[cc for x in range( len(tmpData) )]
                tmp.append( [tmpCol,tmpYear,tmpData] )
            listByYear.append( tmp )
        return listByYear
        

    # ****************************** #
    # ******* PRINTING LISTS ******* #
    # ****************************** #
    def printList( self, li ):
        if isinstance( li, list ):
            for x in li:
                print '\t',x
        else:
            for k,v in li.items():
                print '\t',k,':  ',v
    def printAll( self ):
        self.printList( self.dataList )
    def printTotals( self ):
        self.printList( self._TOTALS )
    def printAttr( self,key ):
        tt = self.getAttr( key )
        print key,':\n'
        self.printList( tt )

    # ******************************* #
    # ******** GETTING LISTS ******** #
    # ******************************* #
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
    # 'date_': date of row to search for
    # return: list of vals in that row (other than the date, cause duh)
    def getRowValsByDate( self,date_ ):        
        rVals = [ row.values() for row in self.dataList if row['Date']==date_ ]
        return rVals[0][1:]
    # returns dictionary
    def getRowsByMonth( self,month_ ):
        rVals = [ row for row in self.dataList if row['Date'].month==month_ ]
        return rVals
    def getRowsByYear( self,year_ ):
        rVals = [ row for row in self.dataList if row['Date'].year==year_ ]
        return rVals


    # ****************************** #
    # ********** GRAPHING ********** #
    # ****************************** #
    # * 1. init_LinePlot()         * #
    # *     -- getFigData()        * #
    # *
    # *     -- format_Axes()       * #
    # *     -- initLegend()        * #
    # * 2. Plot_Fig()              * #
    # ****************************** #
        # 'self.xAxis == 'xx'
        # self.yAxis_lists == 'yy_lists'

    def init_Plot( self, xType, yType ):
        # set types:
        self.xType = xType
        self.yType = yType
        # create figure:
        self.fig , self.ax = plt.subplots()
        self.ax.set_title( 'Super Mega-Awesome Budget Graph ' )
        self.ax.set_xlabel( xType )    # will be reset during formatting
        self.ax.set_ylabel( yType, rotation='vertical' )
        self.ax.grid( True )
        
        #self.getFigData()
        self.getXYData(xType,yType)

        # Plot Data:
        self.NN = len( self.xAxis )  # num x-axis entries
        self.ind = np.arange( self.NN )   # evenly spaced plot indices| range:(0,len(xx)]
        
        self.ax.autoscale(tight=True)

        self.graphStuff()
        self.format_Axes()
        self.initLegend()


    def init_LinePlot( self,ind ):
        # Create Figure        
        ii = 0  # increment
        self.Lines = []
        for yy in self.yAxis_lists:
            ln = self.ax.plot( ind, yy, '1-', label=self.columns[ii], linewidth=2. )
            self.Lines = self.Lines + ln
            ii = ii+1

        self.format_Axes()
        self.initLegend()

        
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
            self.XY.append( zip(self.xAxis,self.getAttr(col)) ) # x,y pairs


    def format_Axes( self ):
        # Create Custom Formattering Functions #
        def xAxisFMT_DAY( x, pos=None ):
            thisInd = np.clip( int(x+0.5), 0, self.NN-1 )
            return self.xAxis[thisInd].strftime( strFmt )
        
        def yAxisFMT( y, pos=None ):
            return '$%1.2f'%y

        # *** Format Y-Axis *** #
        yLabel = self.yType.lower()
        if yLabel=='sum':   yLabel = 'Total'
        else:               yLabel = yLabel.capitalize()
        xLabel = self.xType.lower()
        xLabel = xLabel.capitalize()
        self.ax.set_ylabel( '%(yy)s Spent per %(xx)s'%{'yy':yLabel,'xx':xLabel},
                            rotation='vertical' )
        self.ax.yaxis.set_major_formatter( ticker.FuncFormatter(yAxisFMT) )

        
        # *** Format X-Axis *** #
        plotYear = self.YearRange()
        
            # single year
        if isinstance( plotYear, int ):
            if   self.xType=='DAY':      strFmt = '%m-%d';  self.ax.set_xlabel( 'Dates (%d)'%plotYear )
            elif self.xType=='MONTH':    strFmt = '%b';     self.ax.set_xlabel( 'Months (%d)'%plotYear )
            elif self.xType=='YEAR':     strFmt = '%Y';     self.ax.set_xlabel( 'Year' )
            else:
                print '--- Roses Are Red ---'
                sys.exit(1)

            # multiple years
        else:
            if   self.xType=='DAY':     strFmt = '%Y-%m-%d';    self.ax.set_xlabel( 'Dates (%(aa)d-%(bb)d)'
                                                                                    %{'aa':plotYear[0].year,'bb':plotYear[1].year} )
            elif self.xType=='MONTH':   strFmt = '%b %Y';       self.ax.set_xlabel( 'Months (%(aa)d-%(bb)d)'
                                                                                    %{'aa':plotYear[0].year,'bb':plotYear[1].year} )
            elif self.xType=='YEAR':    strFmt = '%Y';          self.ax.set_xlabel( 'Years' )
            
            else:
                print '--- Violets Are Blue ---'
                sys.exit(1)
    
        self.ax.xaxis.set_major_formatter( ticker.FuncFormatter(xAxisFMT_DAY) )
        
        self.fig.autofmt_xdate()


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

    def Plot_Fig( self, xType, yType ):
        self.init_Plot( xType,yType )
        plt.show()

        


if __name__ == "__main__":
    stuff = DataPlotter()
    stuff.Plot_Fig( 'YEAR','AVERAGE' )  # Plot_Fig( ['DAY'|'MONTH'|'YEAR'], ['SUM'|'AVERAGE'] )
