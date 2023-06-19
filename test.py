import sys
import PyQt5
import PyQt5.QtWidgets, PyQt5.QtCore


class Widget(PyQt5.QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = PyQt5.QtWidgets.QTreeWidget()
        layout_ = PyQt5.QtWidgets.QHBoxLayout()
        layout_.addWidget(self.tree)
        self.setLayout(layout_)
    
    def _set_item(self, parent, section):
        if not isinstance(section, dict):
            print('_set_item', f'Unexpected type: {type(section)}')
            return
        for key, value in section.items():
            item = PyQt5.QtWidgets.QTreeWidgetItem([key])
            if parent is None:
                self.tree.addTopLevelItem(item)
            else:
                parent.addChild(item)
            self._set_item(item, value)
    
    def fill(self, dic):
        self.tree.setColumnCount(1)
        self._set_item(None, dic)
    
    def expand_all(self):
        self.tree.expandAll()


if __name__ == '__main__':
    dic = {'RootLevel':
              {'Level1': {'Level1_item1': {}
                         ,'Level1_item2': {}
                         ,'Level1_item3': {}
                         }
              ,'Level2': {'Level2_SubLevel1':
                             {'Level2_SubLevel1_item1': {}
                             ,'Level2_SubLevel1_item2': {}
                             ,'Level2_SubLevel1_item3': {}
                             }
                         ,'Level2_SubLevel2':
                             {'Level2_SubLevel2_item1': {}
                             ,'Level2_SubLevel2_item2': {}
                             ,'Level2_SubLevel2_item3': {}
                             }
                         ,'Level2_SubLevel3':
                             {'Level2_SubLevel3_item1': {}
                             ,'LEVEL2_SUBLEVEL3_ITEM2': 
                                 {'Level2_SubLevel31_item1': {}
                                 ,'Level2_SubLevel31_item2': {}
                                 ,'Level2_SubLevel31_item3': {}
                                 ,'Level2_SubLevel31_item4': {}
                                 ,'Level2_SubLevel31_item5': {}
                                 ,'Level2_SubLevel31_item6': {}
                                 ,'Level2_SubLevel31_item7a': {}
                                 }
                             ,'Level2_SubLevel3_item3': {}
                             }
                         ,'Level2_SubLevel4':
                             {'Level2_SubLevel4_item1': {}
                             ,'Level2_SubLevel4_item2': {}
                             ,'Level2_SubLevel4_item3': {}
                             ,'Level2_SubLevel4_item4': {}
                             }
                         }
              ,'Level3': {'Level3_item1': {}
                         ,'Level3_item2': {}
                         ,'Level3_item3': {}
                         }
              }
          }
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    main = Widget()
    main.fill(dic)
    main.expand_all()
    main.resize(400, 650)
    main.show()
    sys.exit(app.exec_())
