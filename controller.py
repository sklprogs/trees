import sys
import PyQt5
import PyQt5.QtWidgets

import gui as gi



class Tree:
    
    def __init__(self):
        self.majors = []
        self.minors = {}
        self.gui = gi.Tree()
        self.set_bindings()
    
    def move_item_up(self):
        self.move_item_delta(-1)
    
    def move_item_down(self):
        self.move_item_delta(1)
    
    def move_item_delta(self,delta=-1):
        rowno1 = self.gui.get_cur_row()
        rowno2 = rowno1 + delta
        
        index1 = self.gui.get_cur_index()
        item1 = self.gui.get_item(index1)
        
        parent_item = self.gui.get_parent(item1)
        parent_index = self.gui.get_index_by_item(parent_item)
        
        # Swap root-related adjacent rows (moves their children as well)
        if parent_item is None:
            self.gui.swap_rows(rowno1,rowno2)
            return
        
        index2 = self.gui.get_index(rowno2,parent_index)
        item2 = self.gui.get_item(index2)
        
        if not item1 or not item2:
            print('item empty!')
            return
        
        text1 = self.gui.get_text(item1)
        text2 = self.gui.get_text(item2)
        self.gui.set_text(item1,text2)
        self.gui.set_text(item2,text1)
    
    def move_up(self):
        rowno = self.gui.get_cur_row()
        if rowno == 0:
            print('Create new group first')
        else:
            self.move_item_up()
        self.set_majors()
        self.set_minors()
    
    def move_down(self):
        rowno = self.gui.get_cur_row()
        index_ = self.gui.get_cur_index()
        item = self.gui.get_item(index_)
        rownum = self.gui.get_row_num(item)
        if rowno == rownum - 1:
            print('Create new group first')
        else:
            self.move_item_down()
        self.set_majors()
        self.set_minors()
    
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
        self.gui.bind('Shift+Up',self.move_up)
        self.gui.bind('Shift+Down',self.move_down)
        self.gui.bind('Escape',self.close)
    
    def get_children(self,item):
        children = []
        if not item:
            print('empty!')
            return children
        rownum = self.gui.get_row_num(item)
        if not rownum:
            print('empty!')
            return children
        for i in range(rownum):
            subitem = self.gui.get_child(item,i,0)
            children.append(self.gui.get_text(subitem))
        return children

    def set_majors(self):
        self.majors = self.get_children(self.gui.get_root())
        print('Majors:',self.majors)
    
    def set_minors(self):
        if not self.majors:
            print('empty!')
            return
        root = self.gui.get_root()
        if not root:
            print('empty!')
            return
        for i in range(len(self.majors)):
            item = self.gui.get_child(root,i,0)
            self.minors[self.majors[i]] = self.get_children(item)
        print('Minors:',self.minors)


if __name__ == '__main__':
    dic = {'Level1': ['Level1_item1','Level1_item2','Level1_item3']
          ,'Level2': ['Level2_item1','Level2_item2','Level2_item3'
                     ,'Level2_item4'
                     ]
          ,'Level3': ['Level3_item1','Level3_item2','Level3_item3']
          }
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    itree = Tree()
    itree.fill(dic)
    itree.gui.tree.expandAll()
    itree.show()
    #itree.set_majors()
    #itree.set_minors()
    sys.exit(app.exec_())
