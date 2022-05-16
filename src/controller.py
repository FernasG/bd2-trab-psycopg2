from .model import NorthwindModel, Order
from .view import NorthwindView

class NorthwindController:
    def __init__(self) -> None:
        self.__view = NorthwindView()
        self.__model = NorthwindModel()

    def start(self):
        while True:
            user_input = self.__view.menu()

            if user_input == 1:
                data = self.__view.create_order()
                order = Order(**data)
                response = self.__model.create_order(order)
                self.__view.show_create_result(response)
            elif user_input == 2:
                orderid = self.__view.find_order()
                response = self.__model.find_order(orderid)
                self.__view.show_find_result(response)
            elif user_input == 3:
                orderid = self.__view.delete_order()
                response = self.__model.delete_order(orderid)
                self.__view.show_delete_result(response)
            elif user_input == 4:
                data = self.__view.update_order()
                response = self.__model.update_order(data)
                self.__view.show_update_result(response)
            elif user_input == 5:
                print("Saindo...")
                break
            else:
                print("Opção inválida, tente um dos valores a cima.")