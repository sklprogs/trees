import sys
import PyQt5
import PyQt5.QtWidgets


class Model:
    
    def __init__(self):
        self.model = PyQt5.QtGui.QStandardItemModel()
        self.root = self.model.invisibleRootItem()
        self.parent = self.root
    
    def fill(self, dic):
        self.parse_dic(dic)
    
    def parse_dic(self, value):
        for key in value:
            print('parse_dic:', key)
            self.parse_item(value[key])
    
    def parse_item(self, value):
        if isinstance(value, str):
            print('parse_item:', value)
            #self.addCmd(self.root, value)
            item = PyQt5.QtGui.QStandardItem(value)
            self.model.appendRow(item)
        elif isinstance(value, list):
            print('parse_item: list')
            for item in value:
                self.parse_item(item)
        elif isinstance(value, dict):
            print('parse_item: dict')
            self.parse_dic(value)
    
#    def addChildCmd(self, parent, text):
#        self.addCmd(text, parent)
#
#    def addCmd(self, parent, text):
#        # Add a level to a tree widget
#        item = PyQt5.QtWidgets.QTreeWidgetItem(parent, [text])
#        parent.appendRow(item)
#        return item



class Tree(PyQt5.QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = PyQt5.QtWidgets.QTreeView()
        layout_ = PyQt5.QtWidgets.QHBoxLayout()
        layout_.addWidget(self.tree)
        self.setLayout(layout_)
        self.set_model()
    
    def has_children(self, index_):
        return self.model.model.hasChildren(index_)
    
    def remove_item(self, index_):
        # Remove item and all its children
        self.model.model.removeRow(self.get_row(index_), index_.parent())
    
    def collapse_all(self):
        self.tree.collapseAll()
    
    def expand_all(self):
        self.tree.expandAll()
    
    def set_expanded(self, index_, Expand=False):
        self.tree.setExpanded(index_, Expand)
    
    def is_expanded(self, index_):
        return self.tree.isExpanded(index_)
    
    def set_text(self, item, text):
        item.setText(text)
    
    def get_parent(self, item):
        return item.parent()
    
    def fill(self, dic):
        self.model.fill(dic)
    
    def bind(self, hotkey, action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_model(self):
        self.model = Model()
        self.tree.setModel(self.model.model)
    
    def get_text(self, item):
        return item.text()
    
    def get_child(self, item, rowno, colno):
        return item.child(rowno, colno)
    
    def get_root(self):
        return self.model.model.invisibleRootItem()
    
    def set_cur_index(self, index_):
        flags = self.tree.selectionModel().ClearAndSelect
        self.tree.selectionModel().setCurrentIndex(index_, flags)
    
    def get_cur_index(self):
        # PyQt5.QtCore.QItemSelectionModel.currentIndex
        return self.tree.selectionModel().currentIndex()
    
    def get_root_index(self, rowno):
        return self.model.model.index(rowno, 0)
    
    def get_index(self, rowno, parent_index):
        return self.model.model.index(rowno, 0, parent_index)
    
    def get_index_by_item(self, item):
        return self.model.model.indexFromItem(item)
    
    def get_item(self, index_):
        return self.model.model.itemFromIndex(index_)
    
    def get_item_by_row(self, rowno):
        return self.model.model.item(rowno)


if __name__ == '__main__':
    dic = {'Level1': ['Level1_item1', 'Level1_item2', 'Level1_item3']
          ,'Level2': ['Level2_item1', 'Level2_item2', 'Level2_item3'
                     ,'Level2_item4'
                     ]
          ,'Level3': ['Level3_item1', 'Level3_item2', 'Level3_item3']
          }
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    main = Tree()
    main.fill(dic)
    main.show()
    sys.exit(app.exec_())
