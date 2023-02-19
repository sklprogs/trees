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

    def fill(self,dic):
        self.model.fill(dic)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def set_model(self):
        self.model = Model()
        self.tree.setModel(self.model.model)
    
    def get_index(self):
        return self.tree.selectionModel().currentIndex()
    
    def get_row(self):
        index_ = self.get_index()
        return(index_.row(),index_.column())


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
