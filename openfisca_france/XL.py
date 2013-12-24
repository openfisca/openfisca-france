'''
Created on 9 juil. 2013

@author: Utilisateur
'''


try:
    import xlwt as xlwt
    import xlwt.Style as Style
except:
    pass
import pandas as pd
import numpy as np

class XLtable(pd.DataFrame):
    def __init__(self, df=None):
        """
        pandas DataFrame with extra methods for setting location and xlwt style
        in an Excel spreadsheet.

        Parameters
        ----------
        df : A pandas DataFrame object

        Example
        -------
        >>> xldata = XLtable(df=data)
        """
        super(XLtable, self).__init__()
        self._data = df._data
        if isinstance(self.columns, pd.MultiIndex):
            self.col_depth = len(self.columns.levels)
        else:
            self.col_depth = 1
        if isinstance(self.index, pd.MultiIndex):
            self.row_depth = len(self.index.levels)
        else:
            self.row_depth = 1
        # xlwt can't handle int64, so we convert it to float64
        idx = self.dtypes[self.dtypes == np.int64].index
        for i in idx:
            self[i] = self[i].astype(np.float64)
        # we need to convert row indexes too
        if isinstance(self.index, pd.MultiIndex):
            for i in range(len(self.index.levels)):
                if self.index.levels[i].dtype == np.int64:
                    self.index.levels[i] = self.index.levels[i].astype(np.float64)
        else:
            if self.index.dtype.type == np.int64:
                self.index = self.index.astype(np.float64)
        # and column indexes
        if isinstance(self.columns, pd.MultiIndex):
            for i in range(len(self.columns.levels)):
                if self.columns.levels[i].dtype == np.int64:
                    self.columns.levels[i] = self.columns.levels[i].astype(np.float64)
        else:
            if self.columns.dtype.type == np.int64:
                self.columns = self.columns.astype(np.float64)
    def place_index(self, ws, row=0, col=0, axis=0, style=Style.default_style):
        """
        Write XLtable row or column names (indexes) into an Excel sheet

        Parameters
        ----------
        ws : An xlwt Worksheet object
        row: The starting row in Excel where the index will be placed
            (integer, base 0, default 0)
        col: The starting column in Excel where the index will be placed
            (integer, base 0, default 0)
        axis: Whether the row or column index is desired
            (0 for row or 1 for column, default 0)
        style: An xlwt style object

        Example
        -------
        >>> XLtable.place_index(ws=Sheet1, row=0, col=0, axis=0, style=hstyle)

        """
        if axis == 0:
            depth = self.row_depth
            index = self.index
        elif axis == 1:
            depth = self.col_depth
            index = self.columns
        else:
            raise ValueError("XLTable has only two axis (0 or 1)")
        if depth == 1:
            if axis == 0:
                for i in range(len(index)):
                    ws.row(row + i).write(col, index[i], style)
            elif axis == 1:
                for i in range(len(index)):
                    ws.row(row).write(col + i, index[i], style)
        else:
            if axis == 0:
                for level in range(self.row_depth):
                    col += level
                    for i in range(len(index)):
                        ws.row(row + i).write(col, index[i][level], style)
            elif axis == 1:
                for level in range(depth):
                    row += level
                    for i in range(len(index)):
                        ws.row(row).write(col + i, index[i][level], style)
    def place_data(self, ws, row=0, col=0, style=Style.default_style):
        """
        Write XLtable data into an Excel sheet

        Parameters
        ----------
        ws : An xlwt Worksheet object
        row: The starting row in Excel where the data will be placed
            (integer, base 0, default 0)
        col: The starting column in Excel where the data will be placed
            (integer, base 0, default 0)
        style: An xlwt style object

        Example
        -------
        >>> XLtable.place_data(ws=Sheet1, row=0, col=0, style=dstyle)

        """
        for irow in range(len(self.index)): # data
            for icol in range(len(self.columns)):
                ws.row(row + irow).write((col + icol),
                       self.ix[self.index[irow]][self.columns[icol]], style)
    def place_table(self, ws, row=0, col=0, rstyle=Style.default_style,
                    cstyle=Style.default_style, dstyle=Style.default_style):
        """
        Write XLtable (indexes and data) into an Excel sheet

        Parameters
        ----------
        ws : An xlwt Worksheet object
        row: The starting row in Excel where the index will be placed
            (integer, base 0, default 0)
        col: The starting column in Excel where the index will be placed
            (integer, base 0, default 0)
        rstyle: An xlwt style object, determines row index style
        cstyle: An xlwt style object, determines column index style
        dstyle: An xlwt style object, determines data style

        Example
        -------
        >>> XLtable.place_index(ws=Sheet1, row=0, col=0, rstyle=hstyle,
            cstyle=hstyle, dstyle=data_style)

        """
        drow = row + self.col_depth
        dcol = col + self.row_depth
        self.place_index(ws=ws, row=drow, col=col, axis=0, style=rstyle)
        self.place_index(ws=ws, row=row, col=dcol, axis=1, style=cstyle)
        self.place_data(ws=ws, row=drow, col=dcol, style=dstyle)

class XLseries(pd.Series):
    def __new__(cls, *args, **kwargs):
        arr = pd.Series.__new__(cls, *args, **kwargs)
        # xlwt can't handle int64, so we convert it to float64
        if arr.dtype.type == np.int64:
            arr = arr.astype(np.float64)
        # we need to convert indexes too
        if isinstance(arr.index, pd.MultiIndex):
            for i in range(len(arr.index.levels)):
                if arr.index.levels[i].dtype == np.int64:
                    arr.index.levels[i] = arr.index.levels[i].astype(np.float64)
        else:
            if arr.index.dtype.type == np.int64:
                arr.index = arr.index.astype(np.float64)
        return arr.view(XLseries)
    def __init__(self, series=None):
        """
        pandas Series with extra methods for setting location and xlwt style
        in an Excel spreadsheet.

        Parameters
        ----------
        df : A pandas Series object

        Example
        -------
        >>> xlvector = XLseries(series=vector)
        """
        if isinstance(self.index, pd.MultiIndex):
            self.index_depth = len(self.index.levels)
        else:
            self.index_depth = 1
    def place_index(self, ws, row=0, col=0, axis=0, style=Style.default_style):
        """
        Write XLseries index into an Excel sheet

        Parameters
        ----------
        ws : An xlwt Worksheet object
        row: The starting row in Excel where the index will be placed
            (integer, base 0, default 0)
        col: The starting column in Excel where the index will be placed
            (integer, base 0, default 0)
        axis: Whether the index will be placed in vertical or horizontal
            (0 for vertical or 1 for horizontal, default 0)
        style: An xlwt style object

        Example
        -------
        >>> XLseries.place_index(ws=Sheet1, row=0, col=0, axis=0, style=hstyle)

        """
        depth = self.index_depth
        index = self.index
        if axis not in [0,1]:
            raise ValueError("Excel has only two axis (0 or 1)")
        if depth == 1:
            if axis == 0:
                for i in range(len(index)):
                    ws.row(row + i).write(col, index[i], style)
            elif axis == 1:
                for i in range(len(index)):
                    ws.row(row).write(col + i, index[i], style)
        else:
            if axis == 0:
                for level in range(depth):
                    col += level
                    for i in range(len(index)):
                        ws.row(row + i).write(col, index[i][level], style)
            elif axis == 1:
                for level in range(depth):
                    row += level
                    for i in range(len(index)):
                        ws.row(row).write(col + i, index[i][level], style)
    def place_data(self, ws, row=0, col=0, axis=0, style=Style.default_style):
        """
        Write XLseries data into an Excel sheet

        Parameters
        ----------
        ws : An xlwt Worksheet object
        row: The starting row in Excel where the data will be placed
            (integer, base 0, default 0)
        col: The starting column in Excel where the data will be placed
            (integer, base 0, default 0)
        axis: Whether the index will be placed in vertical or horizontal
            (0 for vertical or 1 for horizontal, default 0)
        style: An xlwt style object

        Example
        -------
        >>> XLseries.place_data(ws=Sheet1, row=0, col=0, style=dstyle)

        """
        if axis == 0:
            for i in range(len(self)):
                ws.row(row + i).write(col, self.view(np.ndarray)[i], style)
        elif axis == 1:
            for i in range(len(self)):
                ws.row(row).write(col + i, self.view(np.ndarray)[i], style)
    def place_series(self, ws, row=0, col=0, axis=0,
                     istyle=Style.default_style, dstyle=Style.default_style):
        """
        Write XLseries (index and data) into an Excel sheet

        Parameters
        ----------
        ws : An xlwt Worksheet object
        row: The starting row in Excel where the index will be placed
            (integer, base 0, default 0)
        col: The starting column in Excel where the index will be placed
            (integer, base 0, default 0)
        axis: Whether the series will be placed in vertical or horizontal
            (0 for vertical or 1 for horizontal, default 0)
        istyle: An xlwt style object, determines index style
        dstyle: An xlwt style object, determines data style

        Example
        -------
        >>> XLseries.place_index(ws=Sheet1, row=0, col=0, istyle=hstyle,
            dstyle=data_style)

        """
        self.place_index(ws=ws, row=row, col=col, axis=axis, style=istyle)
        if axis == 0:
            col = col + self.index_depth
        else:
            row = row + self.index_depth
        self.place_data(ws=ws, row=row, col=col, axis=axis, style=dstyle)



if __name__ == '__main__':
    pass