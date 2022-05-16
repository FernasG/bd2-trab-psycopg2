from datetime import datetime
from .database.manager import DatabaseManager
from psycopg2.extensions import AsIs

class Order:
    def __init__(self, **kwargs: dict) -> None:
        self.orderid = kwargs.get("orderid")
        self.customerid = kwargs.get("customerid")
        self.employeeid = kwargs.get("employeeid")
        self.orderdate = datetime.now()
        self.requireddate = kwargs.get("requireddate")
        self.shippeddate = kwargs.get("shippeddate")
        self.freight = kwargs.get("freight")
        self.shipname = kwargs.get("shipname")
        self.shipaddress = kwargs.get("shipaddress")
        self.shipcity = kwargs.get("shipcity")
        self.shipregion = kwargs.get("shipregion")
        self.shippostalcode = kwargs.get("shippostalcode")
        self.shipcountry = kwargs.get("shipcountry")
        self.shipperid = kwargs.get("shipperid")

class NorthwindModel:
    def __init__(self) -> None:
        self.__manager = DatabaseManager()
        self.__order_columns = ["orderid", "customerid", "employeeid", "orderdate", "requireddate", "shippeddate", "freight", "shipname", "shipaddress", "shipcity",  "shipregion", "shippostalcode", "shipcountry", "shipperid"]

    def create_order(self, order: Order):
        query = f"SELECT * FROM northwind.employees WHERE employeeid = {order.employeeid}"
        result = self.__manager.find_one(query)

        if not result: return False

        query = f"SELECT * FROM northwind.customers WHERE customerid = '{order.customerid}'"
        result = self.__manager.find_one(query)

        if not result: return False

        order.orderid = self.__orderid()

        query = f"INSERT INTO northwind.orders ({', '.join(self.__order_columns)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *"
        values = (order.orderid, order.customerid, order.employeeid, order.orderdate, order.requireddate, order.shippeddate, order.freight, order.shipname, order.shipaddress, order.shipcity, order.shipregion, order.shippostalcode, order.shipcountry, order.shipperid)
        status = self.__manager.insert(query, values)
        return status

    def find_order(self, orderid) -> Order:
        query = f"SELECT * FROM northwind.orders WHERE orderid = {orderid}"
        order = self.__manager.find_one(query)

        if isinstance(order, tuple):
            data = {self.__order_columns[idx]: val for idx, val in enumerate(order)}
            return Order(**data)

        return order

    def update_order(self, data: dict):
        orderid = data.get("orderid")
        column = data.get("column")
        value = data.get("value")

        if not column or column not in self.__order_columns: 
            return False

        if column in ["employeeid", "customerid"]:
            table, val = ("employees", value) if column == "employeeid" else ("customers", f"'{value}'")
            query = f"SELECT * FROM northwind.{table} WHERE {column} = {val}"
            result = self.__manager.find_one(query)

            if not result: return False

        query = "UPDATE northwind.orders SET %s = %s WHERE orderid = %s"
        status = self.__manager.update(query, (AsIs(column), value, orderid))
        return status

    def delete_order(self, orderid: int):
        query = "DELETE FROM northwind.order_details WHERE orderid = %s"
        result = self.__manager.delete(query, (str(orderid),))
        if isinstance(result, bool) and not result: return False
        query = "DELETE FROM northwind.orders WHERE orderid = %s"
        status = self.__manager.delete(query, (str(orderid),))
        return status

    def __orderid(self) -> int:
        last_id = self.__manager.find_one("SELECT orderid FROM northwind.orders ORDER BY orderid DESC")
        return last_id[0] + 1 if last_id else 1
