import sys
import PyQt5
import PyQt5.QtWidgets, PyQt5.QtCore


class Model:
    
    def __init__(self):
        self.model = PyQt5.QtGui.QStandardItemModel()
        self.Success = True
    
    def print(self):
        rownum = self.model.rowCount()
        colnum = self.model.columnCount()
        mes = f'Table size: {rownum}x{colnum}'
        print(mes)
        for rowno in range(rownum):
            for colno in range(colnum):
                index_ = self.model.index(rowno, colno)
                data = self.model.data(index_, PyQt5.QtCore.Qt.DisplayRole)
                print(type(data))
                print(data)
    
    def fill(self, dic):
        f = 'Model.fill'
        if not dic:
            self.Success = False
            print(f'{f}:Empty')
            return
        self.dic = dic
        self.parse_json()
    
    def _set_item(self, parent, section):
        if isinstance(section, dict):
            for key, value in section.items():
                item = PyQt5.QtGui.QStandardItem(str(key))
                if isinstance(value, dict):
                    parent.appendRow(item)
                    self._set_item(item, value)
                else:
                    parent.appendRow([item])
    
    def parse_json(self):
        f = 'Model.parse_json'
        if not self.Success:
            print(f'{f}:Cancel')
            return
        parent = self.model.invisibleRootItem()
        self._set_item(parent, self.dic)



class Widget(PyQt5.QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = PyQt5.QtWidgets.QTreeView()
        layout_ = PyQt5.QtWidgets.QHBoxLayout()
        layout_.addWidget(self.tree)
        self.setLayout(layout_)
    
    def expand_all(self):
        self.tree.expandAll()

    def set_model(self, model):
        self.tree.setModel(model)


if __name__ == '__main__':
    dic = {'RootLevel':
              {'Level1': {'Level1_item1': 14
                         ,'Level1_item2': 1.2
                         ,'Level1_item3': 3.55
                         }
              ,'Level2': {'Level2_SubLevel1':
                             {'Level2_SubLevel1_item1': 3.52
                             ,'Level2_SubLevel1_item2': 2.55
                             ,'Level2_SubLevel1_item3': 13
                             }
                         ,'Level2_SubLevel2':
                             {'Level2_SubLevel2_item1': 2
                             ,'Level2_SubLevel2_item2': 4
                             ,'Level2_SubLevel2_item3': 3.11
                             }
                         ,'Level2_SubLevel3':
                             {'Level2_SubLevel3_item1': 0
                             ,'LEVEL2_SUBLEVEL3_ITEM2': 
                                 {'Level2_SubLevel31_item1': 1
                                 ,'Level2_SubLevel31_item2': 2
                                 ,'Level2_SubLevel31_item3': 3
                                 ,'Level2_SubLevel31_item4': 4
                                 ,'Level2_SubLevel31_item5': 5
                                 ,'Level2_SubLevel31_item6': 6
                                 ,'Level2_SubLevel31_item7a': 7
                                 }
                             ,'Level2_SubLevel3_item3': 2
                             }
                         ,'Level2_SubLevel4':
                             {'Level2_SubLevel4_item1': 0
                             ,'Level2_SubLevel4_item2': 1
                             ,'Level2_SubLevel4_item3': 2
                             ,'Level2_SubLevel4_item4': 3
                             }
                         }
              ,'Level3': {'Level3_item1': 12
                         ,'Level3_item2': 13.55
                         ,'Level3_item3': 122
                         }
              }
          }
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    imodel = Model()
    imodel.fill(dic)
    main = Widget()
    main.set_model(imodel.model)
    main.expand_all()
    main.resize(400, 650)
    main.show()
    imodel.print()
    sys.exit(app.exec_())
