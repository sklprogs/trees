import sys
import PyQt5
import PyQt5.QtWidgets

import gui as gi

#from skl_shared_qt.localize import _
#import skl_shared_qt.shared as sh



class Tree:

    def __init__(self):
        self.gui = gi.Tree()
        self.set_bindings()
    
    def has_expanded(self):
        row_num = self.gui.get_row_num(self.gui.get_root())
        for rowno in range(row_num):
            if self.gui.is_expanded(self.gui.get_root_index(rowno)):
                return True
    
    def expand_or_collapse_all(self):
        if self.has_expanded():
            self.gui.collapse_all()
        else:
            self.gui.expand_all()
    
    def expand_or_collapse(self):
        index_ = self.gui.get_cur_index()
        if index_ is None:
            print('empty!')
            return
        if self.gui.is_expanded(index_):
            self.gui.set_expanded(index_, False)
        else:
            self.gui.set_expanded(index_, True)
    
    def close(self):
        self.gui.close()
    
    def show(self):
        self.gui.show()
    
    def fill(self,dic):
        f = '[Trees] controller.Tree.fill'
        if not dic:
            print(f,'Empty!')
            return
        self.gui.fill(dic)
    
    def set_bindings(self):
        self.gui.bind('Escape', self.close)
        self.gui.bind('Space', self.expand_or_collapse)
        self.gui.bind('Ctrl+A', self.expand_or_collapse_all)
    
    def get_children(self, item):
        children = []
        if not item:
            print('empty!')
            return children
        rownum = self.gui.get_row_num(item)
        if not rownum:
            print('empty!')
            return children
        for i in range(rownum):
            subitem = self.gui.get_child(item, i, 0)
            if not subitem:
                print('Avoid None')
                continue
            children.append(self.gui.get_text(subitem))
        return children


if __name__ == '__main__':
    dic = {'Level1': ['Level1_item1', 'Level1_item2', 'Level1_item3']
          ,'Level2': ['Level2_item1', 'Level2_item2', 'Level2_item3'
                     ,'Level2_item4'
                     ]
          ,'Level3': ['Level3_item1', 'Level3_item2', 'Level3_item3']
          ,'Level4': ['Level4_item1', 'Level4_item2']
          ,'Level5': ['Level5_item1', 'Level5_item2', 'Level5_item3'
                     ,'Level5_item4', 'Level5_item5'
                     ]
          }
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    itree = Tree()
    itree.fill(dic)
    itree.gui.tree.expandAll()
    #itree.show()
    itree.gui.showMaximized()
    #itree.set_majors()
    #itree.set_minors()
    sys.exit(app.exec_())
