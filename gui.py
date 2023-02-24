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
    
    def _print(self,rowno,colno):
        index_ = self.model.model.index(rowno,colno)
        item = self.model.model.itemFromIndex(index_)
        if item is None:
            print(f'No item for ({rowno},{colno})!')
        else:
            print(f'({rowno},{colno}):',item.text())
    
    def print_index(self):
        self._print(0,0)
        self._print(0,1)
        self._print(1,0)
        self._print(2,0)
        self._print(3,0)
    
    def inspect_item(self,item):
        if item is None:
            print('Empty item!')
            return
        print('text:',item.text())
        parent = item.parent()
        if parent is None:
            print('This is root item')
            return
        print('parent text:',parent.text())
    
    def get_children(self,item):
        #item.childCount()
        if item is None:
            print('Empty item!')
            return
        child = item.child(0,0)
        if child is None:
            print('Empty child!')
            return
        print(f'({item.text()}): child at (0,0):',child.text())
    
    def get_row(self):
        pass
        '''
        index_ = self.get_index()
        print('index:',index_)
        item = self.model.model.itemFromIndex(index_)
        print('item.index:',item.index())
        print('text:',item.text())
        print('row:',index_.row(),'column:',index_.column())
        parent = item.parent()
        print('parent:',parent)
        if not parent:
            return
        print('parent row:',parent.row())
        '''
        #item = self.model.model.invisibleRootItem()
        #child = item.child()
        #print('type(child):',type(child))
        #print('child',child)
        #print('root row:',item.row())
        #print('root row:',index_.row(),'root column:',index_.column())
        #return(index_.row(),index_.column())


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
