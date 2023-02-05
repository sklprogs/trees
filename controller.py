import sys
import PyQt5
import PyQt5.QtWidgets


class Model:
    
    def __init__(self):
        self.model = PyQt5.QtGui.QStandardItemModel()
        self.Success = True
    
    def fill(self,dic):
        f = 'Model.fill'
        if not dic:
            self.Success = False
            print(f'{f}:Empty')
            return
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
        f = 'Model.parse_json'
        if not self.Success:
            print(f'{f}:Cancel')
            return
        self.root = self.model.invisibleRootItem()
        for key in self.dic:
            self._set_item(key)
    
    def set_headers(self):
        f = 'Model.set_headers'
        if not self.Success:
            print(f'{f}:Cancel')
            return
        self.model.setHorizontalHeaderLabels(['Level'])



class Widget(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.tree = PyQt5.QtWidgets.QTreeView()
        layout_ = PyQt5.QtWidgets.QHBoxLayout()
        layout_.addWidget(self.tree)
        self.setLayout(layout_)

    def set_model(self,model):
        self.tree.setModel(model)


if __name__ == '__main__':
    dic = {'Level1': ['Level1_item1','Level1_item2','Level1_item3']
          ,'Level2': ['Level2_item1','Level2_item2','Level2_item3'
                     ,'Level2_item4'
                     ]
          ,'Level3': ['Level3_item1','Level3_item2','Level3_item3']
          }
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    imodel = Model()
    imodel.fill(dic)
    main = Widget()
    main.set_model(imodel.model)
    main.show()
    sys.exit(app.exec_())
