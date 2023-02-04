#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TableModel(PyQt5.QtCore.QAbstractTableModel):
    
    def __init__(self,datain,*args):
        PyQt5.QtCore.QAbstractTableModel.__init__(self,*args)
        self.arraydata = datain
    
    def rowCount(self,parent):
        return len(self.arraydata)

    def columnCount(self,parent):
        return 1

    def data(self,index,role):
        f = '[MClientQt] subjects.priorities.gui.TableModel.data'
        if not index.isValid():
            return PyQt5.QtCore.QVariant()
        if role == PyQt5.QtCore.Qt.DisplayRole:
            try:
                return PyQt5.QtCore.QVariant(self.arraydata[index.row()])
            except Exception as e:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(),index.column())
                sh.objs.get_mes(f,mes,True).show_warning()
                return PyQt5.QtCore.QVariant()



class App(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def set_gui(self):
        self.layout_ = PyQt5.QtWidgets.QHBoxLayout()
        self.tree = PyQt5.QtWidgets.QTreeView()
        self.layout_.addWidget(self.tree)
        self.setLayout(self.layout_)
    
    def set_model(self,model):
        self.tree.setModel(model)


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    table = ['hello','bye']
    model = TableModel(table)
    app = App()
    app.set_model(model)
    app.show()
    sh.com.end()
