from abc import ABC, abstractmethod


class UserInterface(ABC):
    

    @abstractmethod
    def get_sides(self):
      
        raise NotImplementedError


class ConsoleUserInterface(UserInterface):
   

    def get_sides(self):
        side1 = input("Введите длину стороны A: ")
        side2 = input("Введите длину стороны B: ")
        side3 = input("Введите длину стороны C: ")
        return side1, side2, side3