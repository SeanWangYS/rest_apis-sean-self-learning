import sqlite3

class ItemModel:
    def __init__(self, name, price):
        self.name  = name
        self.price = price