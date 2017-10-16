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
dataSQL = sqlite3.connect('northwind.db') #connect to SQLite data base
dataSQL.text_factory = bytes #avoid decoding errors
c = dataSQL.cursor() #define cursor
for row in c.execute('''
                     SELECT o.CustomerID, o.OrderID, d.ProductID, p.ProductName -- #Output
                     FROM Orders o
                     INNER JOIN [Order Details] d --#INNER JOINS Orders and Order Details
                         on o.OrderID = d.OrderID
                     INNER JOIN Products p --#INNER JOINS with products
                         on d.ProductID = p.ProductID
                     WHERE o.CustomerID = 'ALFKI' --#For ALFKI
                         AND o.OrderID in --#Add constraint
                             (SELECT OrderID
                             FROM [Order Details] 
                             GROUP BY OrderID --#GROUPs OrderID's
                             HAVING COUNT(*) > 1)'''): #Processing only GROUP's bigger than 1 COUNT's 
    print(row)
    
#%%

from pymongo import MongoClient #import packages
client = MongoClient('localhost', 27017) #Finds Database
db = client.Northwind # Get the database

for order in db['orders'].find({'CustomerID' : 'ALFKI'}): #For ALFKI
    results_count = 0
    results = db['order-details'].find({'OrderID': order['OrderID']})
    results_count = results.count() #Order Counter
    if (results_count>1): #Constraint
        for product in db['order-details'].find({'OrderID': order['OrderID']}):
            for name in db['products'].find({'ProductID': product['ProductID']}):
                print(order['CustomerID'],order['OrderID'],product['ProductID'],name['ProductName'])
                
                
                
                
                
                
                