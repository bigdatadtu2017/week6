# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 11:19:35 2017

@author: andre
"""
#1 FROM, 2 ON, 3 JOIN, 4 WHERE, 5 GROUP BY, 6 WITH CUBE or WITH ROLLUP, 7 HAVING, 8 SELECT, 9 DISTINCT,10 ORDER BY, 11 TOP
#https://stackoverflow.com/questions/4596467/order-of-execution-of-the-sql-query
#https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins


#SQLite
import sqlite3 # import packages
dataSQL = sqlite3.connect('northwind.db')   #connect to SQLite data base
dataSQL.text_factory = bytes    #avoid decoding errors
c = dataSQL.cursor()    #define cursor
for row in c.execute('''
                     SELECT o.CustomerID, o.OrderID, d.ProductID, p.ProductName -- #Output
                     FROM Orders o
                     INNER JOIN [Order Details] d --#INNER JOINS Orders and Order Details
                     on o.OrderID = d.OrderID
                     INNER JOIN Products p --#INNER JOINS with products
                     on d.ProductID = p.ProductID
                     WHERE o.CustomerID = 'ALFKI' '''): #For ALFKI
    print(row)
    
#%%

from pymongo import MongoClient #import packages
client = MongoClient('localhost', 27017)    #Finds DB
db = client.Northwind # Get the database
for order in db['orders'].find({'CustomerID' : 'ALFKI'}): #For ALFKI
    for product in db['order-details'].find({'OrderID': order['OrderID']}): #Run over Order Details
        for name in db['products'].find({'ProductID': product['ProductID']}): #Run over Products
            print(order['CustomerID'],order['OrderID'],product['ProductID'],name['ProductName'])