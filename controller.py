import sys
import PyQt5
import PyQt5.QtWidgets

import gui as gi



class Tree:
    
    def __init__(self):
        self.gui = gi.Tree()
        self.set_bindings()
    
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
        self.gui.bind('Space',self.test)
        self.gui.bind('Escape',self.close)
    
    def test(self):
        print(self.gui.get_index())
        print(self.gui.get_row())


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
    itree.show()
    sys.exit(app.exec_())
