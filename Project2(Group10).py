import sqlite3
import pathlib

class Record(object):
    def __init__(self):
        self.connection = ''
        try:
            dbFile = pathlib.Path('Project2.db')
            if dbFile.exists() == False:
                print('database file',dbFile,'dose not exist')
            else:
                self.connection = sqlite3.connect(dbFile)
        except Exception as ex:
            print('Connection error occured!')
            print(ex)


    def addorders(self, Saleprice, Size, Toppings):
        sql = "INSERT INTO orders (salePrice, size, toppings) VALUES (" + str(Saleprice) + ",'" + str(Size) + "', '" + str(Toppings) + "')"
        print('addorders SQL Command:', sql)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
        except Exception as ex:
            print('Error in addorders method')
            print(ex) 

    def addinventorys(self, Dough, Pepperoni, Mushrooms, Sausage, Peppers, Sause, Cheese):
        sql = "INSERT INTO inventory (Dough, Pepperoni, Mushrooms, Sausage, Peppers, Sause, Cheese) VALUES (" + str(Dough) + ", " + str(Pepperoni) + ", " + str(Mushrooms) + ", " + str(Sausage) + ", " + str(Peppers) + ", " + str(Sause) + ", " + str(Cheese) + ")"
        print('addinventorys SQL Command:', sql)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
        except Exception as ex:
            print('Error in addinventorys method')
            print(ex)

    def addexpense(self, Expense):
        sql = "INSERT INTO profit (expenses) VALUES (" + str(Expense) + ")"
        print('addexpense SQL Command:', sql)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
        except Exception as ex:
            print('Error in addexpense method')
            print(ex)

    def addsale(self):
        sql = "INSERT INTO profit (sales) SELECT IFNULL(SUM(salePrice), 0) FROM orders"
        print('addsale SQL Command:', sql)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
        except Exception as ex:
            print('Error in addsale method')
            print(ex)

    def displaysale(self):
        sql = "SELECT (sales) FROM profit WHERE (sales) IS NOT NULL ORDER BY id DESC LIMIT 1"
        print("displaysale query: ", sql)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            s = 0
            for row in records:
                s = row[0]
            print("sale done")
            return s
        except Exception as ex:
            print("Error in displaysale")
            print(ex)

    def displayexpense(self):
        sql = "SELECT IFNULL(SUM(expenses), 0) FROM profit"
        print("displayexpense query: ", sql)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            sumofex = 0
            for row in records:
                sumofex = row[0]
            print("sumex done")
            return sumofex
        except Exception as ex:
            print("Error in displayexpense")
            print(ex)

    def displayinventory(self):
        sql = "SELECT SUM(Dough), SUM(Pepperoni), SUM(Mushrooms), SUM(Sausage), SUM(Peppers), SUM(Sause), SUM(Cheese) FROM inventory"
        print('displayinventory SQL Command:', sql)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            dough = 0
            pepperoni = 0
            mushroom = 0
            sausage = 0
            pepper = 0
            sause = 0
            cheese = 0
            for row in records:
                dough = round(row[0],2)
                pepperoni = round(row[1],2)
                mushroom = round(row[2],2)
                sausage = round(row[3],2)
                pepper = round(row[4],2)
                sause = round(row[5],2)
                cheese = round(row[6],2)
            print("disinven done")
            return [dough, pepperoni, mushroom, sausage, pepper, sause, cheese]
        except Exception as ex:
            print("Error in displayinventory")
            print(ex)

    def displayR(self, output):
        sql = "SELECT salePrice, size, toppings FROM orders" 
        print('displayorders SQL:', sql)
        try:
            output.delete(0,END)
            cursor = self.connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            for row in records:
                re = "Sale Price: $  "+str(row[0])+"  | Size: "+str(row[1])+" | Toppings: "+str(row[2])
                output.insert(END, re)
            cursor.close
        except Exception as ex:
            print('Error in displayorders method')
            print(ex)



from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import math

mydata = Record()

a = 0
top = 0
totalsale = 0
invendou = 0
invenpep = 0
invenmush = 0
invensau = 0
invenpepper = 0
invensause = 0
invencheese = 0
expen = 0
pf = 0
size = ''
topp = ''

def checkinven():
    nowinven = mydata.displayinventory()
    addinven = pizzainven()
    if len(nowinven)==len(addinven):
        afterinven=[]
        for i in range(len(nowinven)):
            afinven=nowinven[i] + addinven[i]
            afterinven.append(afinven)
    return afterinven

def cofiginven():
    i = mydata.displayinventory()
    dough = i[0]
    pepperoni = i[1]
    mushroom = i[2]
    sausage = i[3]
    pepper = i[4]
    sause = i[5]
    cheese = i[6]
    douIn.config(text = dough)
    pepIn.config(text = pepperoni)
    mashIn.config(text = mushroom)
    sauIn.config(text = sausage)
    pepperIn.config(text = pepper)
    sauseIn.config(text = sause)
    cheeseIn.config(text = cheese)

def cmdpizza():
    b = gettop()
    size = b[1]
    topp = b[0]
    d = pizzainven()
    invendou = d[0]
    invenpep = d[1]
    invenmush = d[2]
    invensau = d[3]
    invenpepper = d[4]
    invensause = d[5]
    invencheese = d[6]
    i=0

    if option.get() == 0:
        messagebox.showwarning("Error", "please selet pizza")
    else:
        if min(checkinven()) <= 0:
            messagebox.showwarning("Error", "Insufficient inventory")
        else:
            mydata.addorders(getsale(), size, topp)
            mydata.addinventorys(invendou, invenpep, invenmush, invensau, invenpepper, invensause, invencheese)
            mydata.addsale()

    sales.config(text = '$%.2f' % mydata.displaysale())

    cofiginven()

    p = mydata.displaysale() - mydata.displayexpense()
    profit.config(text = '$%.2f' % p)

    mydata.displayR(transactions)
    


def cmdinven():
    if any([doutwoVar.get(), peptwoVar.get(), mashtwoVar.get(), sautwoVar.get(), peppertwoVar.get(), sausetwoVar.get(), cheesetwoVar.get()]):
        e = invenorder()
        indou = e[0]
        inpep = e[1]
        inmush = e[2]
        insau = e[3]
        inpepper = e[4]
        insause = e[5]
        incheese = e[6]
        mydata.addinventorys(indou, inpep, inmush, insau, inpepper, insause, incheese)
        mydata.addexpense(getexpense())
    else:
        messagebox.showwarning("Error", "please selet inventory")

    expenses.config(text = '$%.2f' % mydata.displayexpense())

    p = mydata.displaysale() - mydata.displayexpense()
    profit.config(text = '$%.2f' % p)

    cofiginven()


def gettop():
    global a
    a = option.get()
    global topp
    global size
    size = ''
    topp = ''
    if a == 15:
        size = 'Large'
    if a == 13:
        size = 'Medium'
    if a == 10:
        size = 'Small'
    if a == 15 or a == 13 or a == 10:
        if pepVar.get() == 1:
            topp = 'Pepperoni '
        if mashVar.get() == 1:
            topp = topp + 'Mushrooms '
        if sauVar.get() == 1:
            topp = topp + 'Sausage '
        if pepperVar.get() == 1:
            topp = topp + 'Peppers'
    print(topp)
    return [topp, size]


def getsale():
    global a
    a = option.get()
    global top
    top = 0
    global totalsale
    if a == 15 or a == 13 or a == 10:
        if pepVar.get() == 1:
            top = top+0.5
        if mashVar.get() == 1:
            top = top+0.5
        if sauVar.get() == 1:
            top = top+0.5
        if pepperVar.get() == 1:
            top = top+0.5
    totalsale = a + top
    return totalsale


def pizzainven():
    global a
    a = option.get()
    global invendou
    global invenpep
    global invenmush
    global invensau
    global invenpepper
    global invensause
    global invencheese
    if a == 15:
        invendou = - 28.5
        invensause = - 17.1
        invencheese = - 19
        invenpep = 0
        invenmush = 0
        invensau = 0
        invenpepper = 0
    if a == 13:
        invendou = -19.5
        invensause = -11.7
        invencheese = -13
        invenpep = 0
        invenmush = 0
        invensau = 0
        invenpepper = 0
    if a == 10:
        invendou = -15
        invensause = -9
        invencheese = -10
        invenpep = 0
        invenmush = 0
        invensau = 0
        invenpepper = 0
    if a == 15:
        if pepVar.get() == 1:
            invenpep = invenpep - 3.42
        if mashVar.get() == 1:
            invenmush = invenmush - 1.9
        if sauVar.get() == 1:
            invensau = invensau - 2.47
        if pepperVar.get() == 1:
            invenpepper = invenpepper - 1.52
    if a == 13:
        if pepVar.get() == 1:
            invenpep = invenpep - 2.34
        if mashVar.get() == 1:
            invenmush = invenmush - 1.3
        if sauVar.get() == 1:
            invensau = invensau - 1.69
        if pepperVar.get() == 1:
            invenpepper = invenpepper - 1.04
    if a == 10:
        if pepVar.get() == 1:
            invenpep = invenpep - 1.8
        if mashVar.get() == 1:
            invenmush = invenmush - 1
        if sauVar.get() == 1:
            invensau = invensau - 1.3
        if pepperVar.get() == 1:
            invenpepper = invenpepper - 0.8
    return [invendou, invenpep, invenmush, invensau, invenpepper, invensause, invencheese]


def invenorder():
    global invendou
    global invenpep
    global invenmush
    global invensau
    global invenpepper
    global invensause
    global invencheese
    if doutwoVar.get() == 1:
        invendou = 100
    else:
        invendou = 0
    if peptwoVar.get() == 1:
        invenpep = 100
    else:
        invenpep = 0
    if mashtwoVar.get() == 1:
        invenmush = 100
    else:
        invenmush = 0
    if sautwoVar.get() == 1:
        invensau = 100
    else:
        invensau = 0
    if peppertwoVar.get() == 1:
        invenpepper = 100
    else:
        invenpepper = 0
    if sausetwoVar.get() == 1:
        invensause = 100
    else:
        invensause = 0
    if cheesetwoVar.get() ==1:
        invencheese = 100
    else:
        invencheese = 0
    return [invendou, invenpep, invenmush, invensau, invenpepper, invensause, invencheese]


def getexpense():
    global expen
    expen = 0
    if doutwoVar.get() == 1:
        expen = expen + 10
    if peptwoVar.get() == 1:
        expen = expen + 40
    if mashtwoVar.get() == 1:
        expen = expen + 30
    if sautwoVar.get() == 1:
        expen = expen + 25
    if peppertwoVar.get() == 1:
        expen = expen + 23
    if sausetwoVar.get() == 1:
        expen = expen + 10
    if cheesetwoVar.get() ==1:
        expen = expen + 15
    return expen
    

def getprofit():
    global totalsale
    global expen
    pf = totalsale - expen
    return pf


root = Tk()
root.title("Project2-Group10")
root.geometry("600x400")

#大小

Label(root, text="Size").grid(row=0,column=0,sticky=W)

option = IntVar()
Large = Radiobutton(root, text="Large", variable = option, value = 15)
Large.grid(row=1, column=0, sticky=W)
Medium = Radiobutton(root, text="Medium", variable = option, value = 13)
Medium.grid(row=2, column=0, sticky=W)
Small = Radiobutton(root, text ="Small", variable = option, value = 10)
Small.grid(row=3, column=0, sticky=W)

Button(root, text="order pizza", command=cmdpizza).grid(row=5, column=0, sticky=W)

#顶料

Label(root, text="Toppings").grid(row=0,column=1,sticky=W)

pepVar = IntVar()
pep = Checkbutton(root, text="Pepperoni", variable=pepVar)
pep.grid(row=1, column=1, sticky=W)

mashVar = IntVar()
mash = Checkbutton(root, text="Mushrooms", variable=mashVar)
mash.grid(row=2, column=1, sticky=W)

sauVar = IntVar()
sau = Checkbutton(root, text ="Sausage", variable =sauVar)
sau.grid(row=3, column =1, sticky=W)

pepperVar = IntVar()
pepper = Checkbutton(root, text="Peppers", variable=pepperVar)
pepper.grid(row=4, column=1, sticky=W)

#成本销售利润

Label(root, text="Expenses:").grid(row=1, column=2, sticky=W)
expenses = Label(root, text="$0.00")
expenses.grid(row=1, column=3, sticky=W)

Label(root, text="Sales:").grid(row=2, column=2, sticky=W)
sales = Label(root, text="$0.00")
sales.grid(row=2, column=3, sticky=W)

Label(root, text="Profit:").grid(row=3, column=2, sticky=W)
profit = Label(root, text="$0.00")
profit.grid(row=3, column=3, sticky=W)

#库存

Label(root, text="Inventory").grid(row=0,column=4,sticky=W)

doutwoVar = IntVar()
dou = Checkbutton(root, text="Dough", variable=doutwoVar)
dou.grid(row=1, column=4, sticky=W)

douIn = Label(root, text="0")
douIn.grid(row=1, column=5, sticky=W)

peptwoVar = IntVar()
peptwo = Checkbutton(root, text="Pepperoni", variable=peptwoVar)
peptwo.grid(row=2, column=4, sticky=W)

pepIn = Label(root, text="0")
pepIn.grid(row=2, column=5, sticky=W)

mashtwoVar = IntVar()
mashtwo = Checkbutton(root, text ="Mushrooms", variable =mashtwoVar)
mashtwo.grid(row=3, column =4, sticky=W)

mashIn = Label(root, text="0")
mashIn.grid(row=3, column=5, sticky=W)

sautwoVar = IntVar()
sautwo = Checkbutton(root, text="Sausage", variable=sautwoVar)
sautwo.grid(row=4, column=4, sticky=W)

sauIn = Label(root, text="0")
sauIn.grid(row=4, column=5, sticky=W)

peppertwoVar = IntVar()
peppertwo = Checkbutton(root, text="Peppers", variable=peppertwoVar)
peppertwo.grid(row=5, column=4, sticky=W)

pepperIn = Label(root, text="0")
pepperIn.grid(row=5, column=5, sticky=W)

sausetwoVar = IntVar()
sausetwo = Checkbutton(root, text="Sause", variable=sausetwoVar)
sausetwo.grid(row=6, column=4, sticky=W)

sauseIn = Label(root, text="0")
sauseIn.grid(row=6, column=5, sticky=W)

cheesetwoVar = IntVar()
cheesetwo = Checkbutton(root, text="Cheese", variable=cheesetwoVar)
cheesetwo.grid(row=7, column=4, sticky=W)

cheeseIn = Label(root, text="0")
cheeseIn.grid(row=7, column=5, sticky=W)

Button(root, text="order inventory", command = cmdinven).grid(row=8, column=4, sticky=W)

label4 = Label(root, text="Past Orders")
label4.grid(row=9, column=0, sticky=W)
transactionFrame = Frame(root)
transactionFrame.grid(row=10, columnspan=10, column=0, sticky=W)
scrollbar = Scrollbar(transactionFrame)
scrollbar.pack(side=RIGHT, fill=Y)
transactions = Listbox(transactionFrame, height=5, width=70, yscrollcommand=scrollbar.set)
transactions.pack()
scrollbar.config(command=transactions.yview)   

sales.config(text = '$%.2f' % mydata.displaysale())
expenses.config(text = '$%.2f' % mydata.displayexpense())
p = mydata.displaysale() - mydata.displayexpense()
profit.config(text = '$%.2f' % p)
cofiginven()
mydata.displayR(transactions)

root.mainloop()