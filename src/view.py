from datetime import datetime
from decimal import Decimal
from typing import Union

from .model import Order

class NorthwindView:
    def __init__(self) -> None:
        self.warning = "\033[93m"
        self.success = "\033[92m"
        self.error = "\033[91m"
        self.endc = "\033[0m"

    def menu(self) -> int:
        options = ["Criar pedido", "Encontrar pedido", "Remover pedido", "Atualizar pedido", "Sair"]

        print(" Menu ".center(50, "="))
        for i, val in enumerate(options):
            print(f"{i+1} - {val}")
        print("=" * 50)

        user_input = int(input("Escolha uma opção: "))

        return user_input

    def create_order(self) -> dict:
        customerid = input("ID do consumidor: ")
        employeeid = int(input("ID do vendedor: "))
        requireddate = datetime.strptime(input("Data da requisição (DD/MM/AAAA): "), "%d/%m/%Y")
        shippeddate = datetime.strptime(input("Data da entrega (DD/MM/AAAA): "), "%d/%m/%Y")
        freight = Decimal(input("Peso do pacote: "))
        shipname = input("Nome entrega: ")
        shipaddress = input("Endereço de destino: ")
        shipcity = input("Cidade de destino: ")
        shipregion = input("Região de destino: ")
        shippostalcode = input("CEP do destino: ")
        shipcountry = input("Pais de destino: ")
        shipperid = int(input("ID do entregador: "))

        return { 
            "customerid": customerid, "employeeid": employeeid, "requireddate": requireddate, 
            "shippeddate": shippeddate, "freight": freight, "shipname": shipname, 
            "shipaddress": shipaddress, "shipcity": shipcity, "shipregion": shipregion,
            "shippostalcode": shippostalcode, "shipcountry": shipcountry, "shipperid": shipperid
        }

    def show_create_result(self, result: Union[tuple, str]) -> None:
        if isinstance(result, tuple):
            print(f"{self.success}Pedido criado com sucesso! ID: {result[0]}{self.endc}")
        else:
            print(f"{self.error}Ocorreu um erro ao criar pedido.{self.endc}")

    def find_order(self) -> int:
        orderid = int(input("Insira o ID do pedido: "))
        return orderid

    def show_find_result(self, order: Union[Order, None]) -> None:
        if order and isinstance(order, Order):
            print(f" Pedido: {str(order.orderid)} ".center(50, "="))
            print(f"ID do consumidor: {order.customerid}")
            print(f"ID do vendedor: {str(order.employeeid)}")
            print(f"Data da requisição: {datetime.strftime(order.requireddate, '%d/%m/%Y')}")
            print(f"Data da entrega: {datetime.strftime(order.shippeddate, '%d/%m/%Y') if order.shippeddate else '-'}")
            print(f"Peso: {str(order.freight)}")
            print(f"Nome entrega: {order.shipname}")
            print(f"Endereço de destino: {order.shipaddress}")
            print(f"Cidade de destino: {order.shipcity}")
            print(f"Região de destino: {order.shipregion}")
            print(f"CEP do destino: {order.shippostalcode}")
            print(f"Pais de destino: {order.shipcountry}")
            print(f"ID do entregador: {str(order.shipperid)}")
        else:
            print(f"{self.warning}Pedido não encontrado.{self.endc}")

    def update_order(self) -> dict:
        orderid = int(input("ID do pedido: "))
        column = input("Coluna a ser atualizada: ")
        value = input(f"Novo valor da coluna '{column}': ")

        return {"orderid": orderid, "column": column, "value": value}

    def show_update_result(self, response: Union[bool, str]):
        if isinstance(response, bool) and response:
            print(f"{self.success}Pedido atualizado com sucesso.{self.endc}")
        else:
            print(f"{self.error}Erro ao atualizar pedido{self.endc}")

    def delete_order(self):
        orderid = int(input("ID do pedido: "))
        return orderid

    def show_delete_result(self, rowcount: Union[bool, int]):
        if isinstance(rowcount, int) and rowcount > 0:
            print(f"{self.success}Pedido removido com succeso.{self.endc}")
        else:
            print(f"{self.error}Erro ao remover pedido.{self.endc}")