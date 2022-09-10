import sqlite3
from datetime import datetime

cnt = sqlite3.connect("d:/store.db")
isloggin = False
isadmin = False
userid = ""


#################################products
# cnt=sqlite3.connect("d:/store.db")
# sql='''CREATE TABLE products
# (p_id INTEGER PRIMARY KEY,
# pname CHAR(30),
# quantity INT(20),
# bprice INT(20),
# sprice INT(20),
# edate CHAR(15),
# exdate CHAR(15),
# brand CHAR(40),
# reserve1 CHAR(20))'''
# cnt.execute(sql)
# cnt.close()
###############################users-table
# cnt=sqlite3.connect("d:/store.db")
# sql='''CREATE TABLE users
# (u_id INTEGER PRIMARY KEY,
# fname CHAR(20),
# lname CHAR(50),
# addr CHAR(50),
# grade INT(10),
# username CHAR(15),
# password CHAR(15),
# edate CHAR(10),
# ncode CHAR(12),
# reserve1 CHAR(20))'''
# cnt.execute(sql)
# cnt.close()
##############################create-transaction
# cnt = sqlite3.connect("d:/store.db")
# sql = '''CREATE TABLE report
# (b_id INTEGER PRIMARY KEY,
# uid INT(15),
# pid INT(15),
# bdate CHAR(15),
# qnt INT(5),
# comment CHAR(50),
# exdate CHAR(15),
# reserve1 CHAR(30))'''
# cnt.execute(sql)
# cnt.close()
#############################main-program

class my_store:

    def submit(self):
        fname = input("please enter your first name: ")
        lname = input("please enter your last name: ")
        addr = input("please enter your address: ")
        grade = 0
        edate = datetime.today().strftime('%Y-%m-%d')
        username = input("please enter your username: ")
        password = input("please enter your password: ")
        cpassword = input("please confirm your password: ")
        ncode = input("please enter your national code: ")
        result = obj.validation(fname, lname, addr, username, password, cpassword, ncode)
        if len(result) > 0:
            for err_msg in result:
                print(err_msg)
            return
        sql = '''INSERT INTO users(fname, lname, addr,grade,edate, username, password,ncode)
        VALUES(?,?,?,?,?,?,?,?)'''
        cnt.execute(sql, (fname, lname, addr, grade, edate, username, password, ncode))
        cnt.commit()
        print("Submit done!")

    def login(self):
        global isloggin, isadmin, userid
        user = input("Please enter your username: ")
        passw = input("Please enter your password: ")
        sql = "SELECT username,u_id FROM users WHERE username=? and password=?"
        cursor = cnt.execute(sql, (user, passw))
        rows = cursor.fetchone()
        if not rows:
            print("wrong username or password!!")
            return
        print("Welcome to your account")
        userid = rows[1]
        isloggin = True
        if user == "admin":
            isadmin = True

    def logout(self):
        global isloggin, isadmin
        print("Are you sure that you want to logout?\n" + "1.Logout from my account", "   ", "2.Cancel the operation")
        choice = input("Enter one of the numbers: ")
        if choice == "1":
            print("You logout from your account successfully!")
            isloggin = False
            isadmin = False
            return
        print("You has been cancelled the operation")

    def mpproducts(self):
        global isloggin, isadmin
        if isadmin == True:
            cnt = sqlite3.connect("d:/store.db")
            pname = input("Enter the name of your product: ")
            quantity = int(input("How much stock do you have? "))
            bprice = int(input("Enter the price of buying: "))
            sprice = int(input("Enter the price of selling: "))
            edate = datetime.today().strftime('%Y-%m-%d')
            exdate = ""
            brand = input("Enter your brand: ")
            reserve = ""
            ###############################################
            sql = '''SELECT pname FROM products WHERE pname=?'''
            cursor = cnt.execute(sql, (pname,))
            rows = cursor.fetchall()
            if len(rows) > 0:
                print("product already exist!!!!")
                return
            ###############################################
            sql = '''INSERT INTO products(pname,quantity,bprice,sprice,edate,exdate,brand,reserve1)
            VALUES(?,?,?,?,?,?,?,?)'''
            cnt.execute(sql, (pname, quantity, bprice, sprice, edate, exdate, brand, reserve))
            cnt.commit()
            print("Your product has been register successfully!")
            cnt.close()
            return
        elif isloggin == False:
            print("Please logging first!")
            return
        else:
            print("This section is only for admins!!!")

    def buy(self):
        global isloggin, userid
        if not (isloggin):
            print("you are not logged in..")
            return
        bdate = datetime.today().strftime('%Y-%m-%d')
        pname = input("What do you want to buy? ")
        sql = '''SELECT * FROM products WHERE pname=?'''
        cursor = cnt.execute(sql, (pname,))
        row = cursor.fetchone()
        if not row:
            print("Wrong product name! ")
            return
        print("product:", row[1], "  Q:", row[2], '  brand:', row[7], "  sprice:", row[4])
        num = int(input("How many you want to buy? "))
        if num <= 0:
            print("Wrong number!")
            return
        if num > row[2]:
            print("not enough numbers of product!")
            return
        print("Total cost: ", num * row[4])
        print("Are you sure that you want to buy this product?\n" + "1.YES", "  ", "2.NO")
        confirm = input("Select by entering number: ")
        if confirm != "1":
            print("You cancelled the operation...")
            return
        newquant = int(row[2]) - num
        sql2 = '''UPDATE products SET quantity=? WHERE pname=?'''
        cnt.execute(sql2, (newquant, pname))
        print("Thanks for your shopping!!!")
        cnt.commit()
        sql3 = '''INSERT INTO report(uid,pid,bdate,qnt)
        VALUES(?,?,?,?)'''
        cnt.execute(sql3, (userid, row[0], bdate, num))
        cnt.commit()

    def plist(self):
        sql = '''SELECT pname,quantity,sprice FROM products WHERE quantity>0 '''
        cursor = cnt.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print("Product:", row[0], "/Qnt:", row[1], "/Price:", row[2])
        return

    def search(self):
        sql = '''SELECT pname,quantity,sprice,brand From products WHERE sprice<=?'''
        pprice = int(input("Enter a price: "))
        cursor = cnt.execute(sql, (pprice,))
        row = cursor.fetchone()
        if not row:
            print("Nothing exist under this price!")
            return
        else:
            print("All the products under this price: ")
            while row:
                print("products:", row[0], "/Qnt:", row[1], "/Price:", row[2], "/Brand:", row[3])
                row = cursor.fetchone()
            print("")
        return

    def search2(self):
        sql = '''SELECT pname,quantity,sprice,brand From products WHERE sprice<? AND sprice>?'''
        pprice1 = int(input("Enter your max price: "))
        pprice2 = int(input("Enter your min price: "))
        cursor = cnt.execute(sql, (pprice1, pprice2))
        row = cursor.fetchone()
        if not row:
            print("Nothing exist between this prices!")
            return
        else:
            print("All the products between this prices: ")
            while row:
                print("products:", row[0], "/Qnt:", row[1], "/Price:", row[2], "/Brand:", row[3])
                row = cursor.fetchone()
            print("")
        return

    def search3(self):
        mysearch = input("What are you searching for? ")
        sql = "SELECT * FROM products WHERE pname LIKE ?  "
        cursor = cnt.execute(sql, ('%' + mysearch + '%',))
        row = cursor.fetchone()
        while row:
            print("Product:", row[1], "/Inventory:", row[2], "/Price:", row[4], "/brand:", row[7])
            row = cursor.fetchone()

    def alltrac(self):
        global isloggin, isadmin
        if not isadmin:
            print("You are not allowed for this action!")
            return
        if not isloggin:
            print("Your arent logged in!!")
            return
        sql = '''SELECT users.fname,products.pname,report.qnt,report.bdate FROM report 
        INNER JOIN users ON report.uid=users.u_id
        INNER JOIN products ON report.pid=products.p_id'''
        cursor = cnt.execute(sql)
        for row in cursor:
            print("user: ", row[0], "  product: ", row[1], "  Qnt: ", row[2], "  date: ", row[3])

    def forgetpass(self):
        user = input("Enter your username: ")
        fname = input("Enter your first name: ")
        lname = input("Enter your last name: ")
        ncode = input("Enter your national code: ")
        ###########################################
        if not (ncode.isnumeric()):
            print("National code should be completely numeric!!")
        ###########################################
        sql = '''SELECT password FROM users WHERE username=? AND fname=? AND lname=? AND ncode=?'''
        cursor = cnt.execute(sql, (user, fname, lname, ncode))
        row = cursor.fetchone()
        while row:
            print("Here is your password")
            print(row[0], "\n")
            row = cursor.fetchone()
        print("What is your plan?\n" + "1.Change my password" + "  " + "2.Keep this password")
        choice = input("Enter one of the numbers: ")
        if choice != "1":
            print("returning to first menu...")
            return
        ##########################################
        while True:
            passw = input("Enter your new password: ")
            confirmpass = input("Please Confirm your password: ")
            if len(passw) < 8:
                print("Your password should have at least 8 characters!!!")
            elif passw != confirmpass:
                print("Miss match, please try again!!!")
            elif passw == confirmpass:
                sql2 = '''UPDATE users SET password=? WHERE username=? AND ncode=? '''
                cnt.execute(sql2, (passw, user, ncode))
                cnt.commit()
                print("Your password has changed to__", passw, "__successfully!")
                return
            else:
                print("Something went wrong,please try again!!")

    def delete(self):
        global isloggin, isadmin
        if not isloggin:
            print("please login in first!!")
            return
        user = input("please enter your username: ")
        passw = input("please enter your password: ")
        sql = '''SELECT * FROM users WHERE username=? and password=?'''
        cursor = cnt.execute(sql, (user, passw))
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Something went wrong,you can try again")
            return
        print(user, '''Are you sure that you want to delete your account?\n1.Delete my account''', "  ",
              "2.Cancel the operation")
        confirm = input("Enter a number: ")
        if confirm != "1":
            print("Delete operation has cancelled!!!")
            return
        sql2 = '''DELETE FROM users WHERE username=? and password=?'''
        cnt.execute(sql2, (user, passw))
        cnt.commit()
        print("your account has been deleted successfully")

    def info_changer(self):
        ###########################################
        user = input("Enter your username: ")
        passw = input("Enter your password: ")
        ncode = input("Enter your national code: ")
        if not (ncode.isnumeric()):
            print("National code should be completely numeric!!")
        print(
            "What is your plan?\n" + "1.Changing username" + "  " + "2.Changing password" + "  " + "3.Cancel operation")
        plan = input("Choose your plan by entering numbers: ")
        sql = '''SELECT username FROM users WHERE username=? AND password=?'''
        cursor = cnt.execute(sql, (user, passw))
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Something is wrong,please try again!!")
        ###########################################
        if plan == "1":
            while True:
                newuser = input("Enter your new username: ")
                sql2 = '''SELECT username FROM users WHERE username=?'''
                cursor2 = cnt.execute(sql2, (newuser,))
                row = cursor2.fetchall()
                if len(row) != 0:
                    print("This username already exist,Try another one!!")
                else:
                    sql3 = "UPDATE users SET username=? WHERE password=? AND ncode=?"
                    cnt.execute(sql3, (newuser, passw, ncode))
                    print("Your user name has changed to", newuser, "successfully...")
                    return
        elif plan == "2":
            while True:
                passw = input("Enter your new password: ")
                confirmpass = input("Please Confirm your password: ")
                if len(passw) < 8:
                    print("Your password should have at least 8 characters!!!")
                elif passw != confirmpass:
                    print("Miss match, please try again!!!")
                elif passw == confirmpass:
                    sql2 = '''UPDATE users SET password=? WHERE username=? AND ncode=? '''
                    cnt.execute(sql2, (passw, user, ncode))
                    cnt.commit()
                    print("Your password has changed to__", passw, "__successfully!")
                    return
                else:
                    print("Something went wrong,please try again!!")
        else:
            print("returning to main menu...")
            return

    def validation(self, fname, lname, addr, username, password, cpassword, ncode):
        errorlist = []
        if fname == "" or lname == "" or username == "" or addr == "" or password == "" or cpassword == "" or ncode == "":
            msg = "please fill all of the blanks"
            errorlist.append(msg)
        if len(password) < 8:
            msg = "pass length must be at least 8"
            errorlist.append(msg)
        elif password != cpassword:
            msg = "pass and confirm mismatch"
            errorlist.append(msg)
        if not (ncode.isnumeric()):
            msg = "national code should be numeric"
            errorlist.append(msg)
        sql = 'SELECT * from users WHERE ncode=?'
        cursor = cnt.execute(sql, (ncode,))
        row = cursor.fetchall()
        if len(row)!=0:
            msg = "national code already exist"
            errorlist.append(msg)
        sql2 = 'SELECT * from users WHERE username=?'
        cursor2 = cnt.execute(sql2, (username,))
        rows = cursor2.fetchall()
        if len(rows) != 0:
            msg = "username already exist"
            errorlist.append(msg)
        return errorlist


obj = my_store()

print("****Welcome to our shop****")
while True:
    if isloggin == False:
        print('''1.Submit\n2.Login\n3.Enter new product\n4.Buy\n5.products list\n6.Search for products\n''' +
              '''7.Search under the price\n8.Search between two price\n9.All transaction\n''' +
              "10.Forget my password\n" + "11.Changing my info\n" + "12.Delete your account\n" + "13.Exit")
    elif isloggin == True:
        print('''1.Submit\n2.logout\n3.Enter new product\n4.Buy\n5.products list\n6.Search for products\n''' +
              '''7.Search under the price\n8.Search between two price\n9.All transaction\n''' +
              "10.Forget my password\n" + "11.Changing my info\n" + "12.Delete your account\n" + "13.Exit")
    plan = input("Choose your plan by entering numbers: ")
    if plan == "1":
        obj.submit()
    elif plan == "2":
        if isloggin == False:
            obj.login()
        elif isloggin == True:
            obj.logout()
    elif plan == "3":
        obj.mpproducts()
    elif plan == "4":
        obj.buy()
    elif plan == "5":
        obj.plist()
    elif plan == "6":
        obj.search3()
    elif plan == "7":
        obj.search()
    elif plan == "8":
        obj.search2()
    elif plan == "9":
        obj.alltrac()
    elif plan == "10":
        obj.forgetpass()
    elif plan == "11":
        obj.info_changer()
    elif plan == "12":
        obj.delete()
    elif plan == "13":
        print("Goodbye")
        break
    else:
        print("Error")
