import sys
import PyQt5
import PyQt5.QtWidgets

import gui as gi



class Tree:
    ''' Drag-and-drop/navigation strategy:
        We assume that:
        - major is a root item, it has no parent and is not indented;
        - minor is a non-root item, it has a non-empty parent and is indented;
        - group1 is an item/group to be moved;
        - group2 is a group over which major/minor group1 is dropped;
        - index1 is the index of the initially selected row;
        - index2 is the index where group1 is to be dropped;
        - index2 > index1 if group1 is moved top to bottom and index1 > index2
          otherwise;
        - item1 is an item having the index of index1;
        - item2 is an item having the index of index2.
        Variants:
        - indices are the same: report that no action is required;
        - both index1 and index2 are root entries:
        
        and index2 is the index of the minor/major where group1 was dropped)
        
        
          - index1 and index2 have the same parent: this should happen only if
            index1 == index2 but we skip this variant above;
          - parents of index1 and index2 have the same title (note that
            a shared title does not make them refer to the same node): merge
            groups by inserting all minors of group2 into group1 at the start
            of group1;
          - parents of index1 and index2 have different titles: 
            insert entire group2 
          - ↓ (index1 precedes index2): put index1 and its children after last
            child of index2;
          - ↑ (index2 precedes index1): put index1 and its children ahead of
            first child of index2;
        - both index1 and index2 are non-root entries:
          - index1 and index2 have the same parent:
            - ↓ (index1 precedes index2): put index1 after index2;
            - ↑ (index2 precedes index1): put index1 ahead of index2;
          - index1 and index2 have a different parent:
            - ↓ (index1 precedes index2): duplicate index1 parent after ;
            - ↑ (index2 precedes index1): ?;
        - index1 is a root entry and index2 is a non-root entry:
          - ↓ (index1 precedes index2): 
    '''
    def __init__(self):
        self.majors = []
        self.minors = {}
        self.gui = gi.Tree()
        self.set_bindings()
    
    def select_mode(self,index1,index2):
        # Select same-level or multilevel strategy
        if not index1 or not index2:
            print('empty!')
            return
        item1 = self.gui.get_item(index1)
        item2 = self.gui.get_item(index2)
        if not item1 or not item2:
            print('empty!')
            return
        parent1 = self.gui.get_parent(item1)
        parent2 = self.gui.get_parent(item2)
        if parent1 == parent2:
            print('Same-level strategy')
        else:
            if parent1 is None:
                parent1 = item1
            if parent2 is None:
                parent2 = item2
            print('Multilevel strategy')
            children = self.get_children(parent1)
            print('Move what:',children)
            parent2_index = self.gui.get_index_by_item(parent2)
            rowno2 = self.gui.get_row(index2)
            # Insert before, delete later since row numbers will change
            self.gui.model.model.insertRows(rowno2,len(children),parent2_index)
            # Referring to deleted items will cause an error
            self.gui.remove_item(index1)
    
    def test(self):
        index1 = self.gui.get_root_index(0)
        index2 = self.gui.get_cur_index()
        self.select_mode(index1,index2)
    
    def test1(self):
        # Works: Both are root items
        # Level 1..5..2
        rowno1 = 4
        rowno2 = 1
        index1 = self.gui.get_root_index(rowno1)
        index2 = self.gui.get_root_index(rowno2)
        self.move_item(index1,index2)
    
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
            self.gui.set_expanded(index_,False)
        else:
            self.gui.set_expanded(index_,True)
    
    def move_up(self):
        index1 = self.gui.get_cur_index()
        if index1 is None:
            print('empty!')
            return
        ''' Do not use 'QTreeView.indexAbove' since it can return both major or
            minor.
        '''
        rowno1 = self.gui.get_row(index1)
        if rowno1 == 0:
            print('lazy!')
            return
        rowno2 = rowno1 - 1
        self._move_by_row(index1,rowno1,rowno2)
    
    def move_down(self):
        index1 = self.gui.get_cur_index()
        if index1 is None:
            print('empty!')
            return
        ''' Do not use 'QTreeView.indexBelow' since it can return both major or
            minor.
        '''
        rowno1 = self.gui.get_row(index1)
        item1 = self.gui.get_item(index1)
        if item1 is None:
            print('empty!')
            return
        parent1 = self.gui.get_parent(item1)
        if parent1 is None:
            parent1 = self.gui.get_root()
        if parent1 is None:
            print('empty!')
            return
        rownum = self.gui.get_row_num(parent1)
        if rowno1 == rownum - 1:
            print('lazy!')
            return
        rowno2 = rowno1 + 1
        self._move_by_row(index1,rowno1,rowno2)
    
    def _move_by_row(self,index1,rowno1,rowno2):
        item1 = self.gui.get_item(index1)
        if item1 is None:
            print('empty!')
            return
        parent1 = self.gui.get_parent(item1)
        if parent1 is None:
            parent1 = self.gui.get_root()
        if parent1 is None:
            print('empty!')
            return
        parent_index = self.gui.get_index_by_item(parent1)
        if parent_index is None:
            print('empty!')
            return
        index2 = self.gui.get_index(rowno2,parent_index)
        self.move_item(index1,index2)
    
    def move_item(self,index1,index2):
        if index1 is None or index2 is None:
            print('empty!')
            return
        item1 = self.gui.get_item(index1)
        item2 = self.gui.get_item(index2)
        if item1 is None or item2 is None:
            print('empty!')
            return
        parent = self.gui.get_parent(item1)
        rowno1 = self.gui.get_row(index1)
        rowno2 = self.gui.get_row(index2)
        print('rowno1:',rowno1,', rowno2:',rowno2)
        if parent:
            print('Mode: minor')
            self.gui.insert(parent,rowno1,rowno2)
        else:
            print('Mode: major')
            self.gui.insert(self.gui.get_root(),rowno1,rowno2)
        self.gui.set_cur_index(index2)
    
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
        self.gui.bind('Escape',self.close)
        self.gui.bind('Shift+Up',self.move_up)
        self.gui.bind('Shift+Down',self.move_down)
        self.gui.bind('Space',self.expand_or_collapse)
        self.gui.bind('Ctrl+A',self.expand_or_collapse_all)
        self.gui.bind('Return',self.test)
    
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
          ,'Level4': ['Level4_item1','Level4_item2']
          ,'Level5': ['Level5_item1','Level5_item2','Level5_item3'
                     ,'Level5_item4','Level5_item5'
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
