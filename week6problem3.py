# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 11:20:02 2017

@author: andre
"""

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
                     SELECT o.CustomerID, p.ProductName, c.CategoryName, o.ShippedDate --#Output
                     FROM Orders o
                     INNER JOIN [Order Details] d --#INNER JOINS Orders and Order Details
                         on o.OrderID = d.OrderID
                     INNER JOIN Products p --#INNER JOINS with products
                         on d.ProductID = p.ProductID
                     INNER JOIN Categories c --#INNER JOINS with categories
                         on p.CategoryID = c.CategoryID
                     WHERE o.CustomerID = 'ALFKI' --#For ALFKI
                     AND o.ShippedDate in --#add constraint
                         (SELECT ShippedDate --On ShippedDate
                         FROM Orders
                         ORDER BY ShippedDate)'''): #Orders By Shipped Date
    print(row)
    
#%%

from pymongo import MongoClient #import packages
client = MongoClient('localhost', 27017) #find Database
db = client.Northwind # Get the database                                 
               
for order in db['orders'].find({'CustomerID' : 'ALFKI'}): #For ALFKI
    for product in db['order-details'].find({'OrderID': order['OrderID']}): #Find Order Details
        for dates in db['orders'].find({'OrderID': product['OrderID']}): #Find Shipped date
            for name in db['products'].find({'ProductID': product['ProductID']}): #Find ProductID
                for cname in db['categories'].find({'CategoryID': name['CategoryID']}): #Find CategoryID
                    print(order['CustomerID'],name['ProductName'], cname['CategoryName'], dates['ShippedDate'])
                
                
                
                
                
                