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
dataSQL = sqlite3.connect('northwind.db')
dataSQL.text_factory = bytes
c = dataSQL.cursor()
for row in c.execute('''
                     SELECT o.CustomerID, o.OrderID, d.ProductID, p.ProductName
                     FROM Orders o
                     INNER JOIN [Order Details] d
                         on o.OrderID = d.OrderID
                     INNER JOIN Products p
                         on d.ProductID = p.ProductID
                     WHERE o.CustomerID = 'ALFKI' 
                         AND o.OrderID in
                             (SELECT OrderID
                             FROM [Order Details]
                             GROUP BY OrderID
                             HAVING COUNT(*) > 1)'''):
    print(row)
    
#%%

from pymongo import MongoClient #import packages
client = MongoClient('localhost', 27017)
db = client.Northwind # Get the database

for order in db['orders'].find({'CustomerID' : 'ALFKI'}):
    results_count = 0
    results = db['order-details'].find({'OrderID': order['OrderID']})
    results_count = results.count()
    if (results_count>1):
        for product in db['order-details'].find({'OrderID': order['OrderID']}):
            for name in db['products'].find({'ProductID': product['ProductID']}):
                print(order['CustomerID'],order['OrderID'],product['ProductID'],name['ProductName'])