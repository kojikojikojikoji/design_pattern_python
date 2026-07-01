from abc import ABCMeta, abstractmethod
from typing import final
import sys



def main():
    d1 = CarDisplay("H")
    d1.display()
    
class AbstractDisplay(metaclass=ABCMeta):

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def close(self):
        pass
    
    @final
    def display(self):
        self.open()
        for i in range(5):
            self.print()
        self.close()
        
        
class CarDisplay(AbstractDisplay):
    def __init__(self, ch):
        self.ch = ch
    
    def open(self):
        sys.stdout.write("<<")
    
    def print(self):
        sys.stdout.write(self.ch)
    
    def close(self):
        sys.stdout.write(">>")
      
      
if __name__ == "__main__":
    # 他のプログラムから関数が呼ばれても、ファイルそのものが呼び出されない限りmain()は実行されないように制限する
    main()

        
                