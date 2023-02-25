import sys
import PyQt5
import PyQt5.QtWidgets


class Model:
    
    def __init__(self):
        self.model = PyQt5.QtGui.QStandardItemModel()
    
    def fill(self,dic):
        self.dic = dic
        self.parse_json()
        self.set_headers()
    
    def _set_item(self,key):
        item = PyQt5.QtGui.QStandardItem(str(key))
        self.root.appendRow(item)
        for value in self.dic[key]:
            child = PyQt5.QtGui.QStandardItem(str(value))
            item.appendRow(child)
    
    def parse_json(self):
        self.root = self.model.invisibleRootItem()
        for key in self.dic:
            self._set_item(key)
    
    def set_headers(self):
        self.model.setHorizontalHeaderLabels(['Level'])



class Tree(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.tree = PyQt5.QtWidgets.QTreeView()
        layout_ = PyQt5.QtWidgets.QHBoxLayout()
        layout_.addWidget(self.tree)
        self.setLayout(layout_)
        self.set_model()

    def set_expanded(self,index_,Expand=False):
        self.tree.setExpanded(index_,Expand)
    
    def is_expanded(self,index_):
        return self.tree.isExpanded(index_)
    
    def set_text(self,item,text):
        item.setText(text)
    
    def get_parent(self,item):
        return item.parent()
    
    def swap_rows(self,rowno1,rowno2):
        # Only adjacent rows should be swapped, otherwise rows may disappear
        item_list = self.model.model.takeRow(rowno1)
        self.model.model.insertRow(rowno2,item_list)
    
    def fill(self,dic):
        self.model.fill(dic)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def set_model(self):
        self.model = Model()
        self.tree.setModel(self.model.model)
    
    def get_text(self,item):
        return item.text()
    
    def get_row_num(self,item):
        return item.rowCount()
    
    def get_child(self,item,rowno,colno):
        return item.child(rowno,colno)
    
    def get_root(self):
        return self.model.model.invisibleRootItem()
    
    def get_row(self,index_):
        return index_.row()
    
    def get_cur_row(self):
        return self.get_cur_index().row()
    
    def get_cur_index(self):
        return self.tree.selectionModel().currentIndex()
    
    def get_index(self,rowno,parent_index):
        return self.model.model.index(rowno,0,parent_index)
    
    def get_index_by_item(self,item):
        return self.model.model.indexFromItem(item)
    
    def get_item(self,index_):
        return self.model.model.itemFromIndex(index_)
    
    def get_item_by_row(self,rowno):
        return self.model.model.item(rowno)


if __name__ == '__main__':
    dic = {'Level1': ['Level1_item1','Level1_item2','Level1_item3']
          ,'Level2': ['Level2_item1','Level2_item2','Level2_item3'
                     ,'Level2_item4'
                     ]
          ,'Level3': ['Level3_item1','Level3_item2','Level3_item3']
          }
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    main = Tree()
    main.fill(dic)
    main.show()
    sys.exit(app.exec_())
