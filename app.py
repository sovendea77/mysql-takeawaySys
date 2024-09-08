# -*- coding=utf-8 -*-
'''
Descripttion: 
Version: 1.0
Author: ZhangHongYu
Date: 2020-11-02 09:24:31
LastEditors: ZhangHongYu
LastEditTime: 2022-04-19 18:58:12
'''
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pymysql
import os
import argparse
import sys
import importlib

importlib.reload(sys)

app = Flask(__name__)
pwd = "18715218029zxy"
db_name = "appDB"
# 全局变量
user_name = "root"
# TODO: username变量的赋值  方法1：全局变量实现，随登录进行修改  方法2：给每个页面传递username
userRole = ""
notFinishedNum = 0
# 上传文件要储存的目录
UPLOAD_FOLDER = '/static/images/'
# 允许上传的文件扩展名的集合
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
# 首页
def indexpage():
    return render_template('index.html')


# 注册
@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('Register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        addr = request.form.get('addr')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB",charset='utf8')

        if userRole == 'RESTAURANT':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT ShopID,ShopPassword,ShopAddress,ShopPhone,Shop.img_res from Shop where ShopID = '{}' ".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # 如果已经存在该商家
            if num == 1:
                print("失败！商家已注册！")
                msg = "fail1"
            else:
                sql2 = "insert into Shop (ShopID, ShopPassword, ShopAddress, ShopPhone) values ('{}', '{}', '{}', '{}') ".format(username, password, addr, phone)

                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("商家注册成功")
                    msg = "done1"
                except ValueError as e:
                    print("--->", e)
                    print("注册出错，失败")
                    msg = "fail1"
            return render_template('Register.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'CUSTOMER':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from Users where UserID = '{}'".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # 如果已存在该用户
            if num == 1:
                print("用户已注册！请直接登录。")
                msg = "fail2"
            else:
                sql2 = "insert into Users (UserID, UserPassword,  UserAddress, UserPhone) values ('{}', '{}', '{}', '{}') ".format(username, password, addr, phone)

                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("商家注册成功")
                    msg = "done2"
                except ValueError as e:
                    print("--->", e)
                    print("注册出错，失败")
                    msg = "fail2"
            return render_template('Register.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'DeliveryPerson':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from DeliveryPersons where DeliveryPersonID = '{}'".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # 如果已存在该用户
            if num == 1:
                print("用户已注册！请直接登录。")
                msg = "fail2"
            else:
                sql2 = "insert into DeliveryPersons (DeliveryPersonID, DeliveryPersonPassword,  DeliveryPersonPos, DeliveryPersonPhone) values ('{}', '{}', '{}', '{}') ".format(username, password, addr, phone)

                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("外卖员注册成功")
                    msg = "done2"
                except ValueError as e:
                    print("--->", e)
                    print("注册出错，失败")
                    msg = "fail2"
            return render_template('Register.html', messages=msg, username=username, userRole=userRole)


# 登录
@app.route('/logIn', methods=['GET', 'POST'])
def logInPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('logIn.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')

        if userRole == 'ADMIN':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from ADMIN where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该管理员且密码正确
            if num == 1:
                print("登录成功！欢迎管理员！")
                msg = "done1"
            else:
                print("您没有管理员权限或登录信息出错。")
                msg = "fail1"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'shop':
            cursor = db.cursor()
            try:
                cursor.execute("use test2")
            except:
                print("Error: unable to use database!")
            sql = "SELECT ShopID,ShopPassword,ShopAddress,ShopPhone,Shop.img_res from Shop where ShopID = '{}' and ShopPassword='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该商家且密码正确
            if num == 1:
                print("登录成功！欢迎商家用户！")
                msg = "done2"
            else:
                print("您没有商家用户权限或登录信息出错。")
                msg = "fail2"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'CUSTOMER':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from Users where UserID = '{}' and UserPassword='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该用户且密码正确
            if num == 1:
                print("登录成功！欢迎用户！")
                msg = "done3"
            else:
                print("您没有用户权限，未注册或登录信息出错。")
                msg = "fail3"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'DeliveryPerson':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from DeliveryPersons where DeliveryPersonID = '{}' and DeliveryPersonPassword='{}'".format(
                username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该外卖员且密码正确
            if num == 1:
                print("登录成功！欢迎外卖员用户！")
                msg = "done4"
            else:
                print("您没有用户权限，未注册或登录信息出错。。")
                msg = "fail4"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)


# 管理员的店铺列表页面
@app.route('/adminRestList', methods=['GET', 'POST'])
def adminRestListPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT ShopID,ShopPassword,ShopAddress,ShopPhone,Shop.img_res from Shop"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminRestList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminRestList.html', username=username, messages=msg)
    elif request.form["action"] == "移除":
        RESTName = request.form.get('RESTName')
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # TODO: 点击移除后显示移除成功，但数据库里没有删掉
        # 删除DISHES的
        sql1 = "DELETE FROM Dishes WHERE ShopID = '{}'".format(RESTName)
        cursor.execute(sql1)
        db.commit()
        # 删除订单表里的
        sql2 = "DELETE FROM Orders WHERE ShopID = '{}'".format(RESTName)
        cursor.execute(sql2)
        db.commit()

        # 删除shop的
        sql4 = "DELETE FROM Shop WHERE ShopID = '{}'".format(RESTName)
        cursor.execute(sql4)
        db.commit()
        print(sql4)

        msg = "delete"
        print(msg)

        return render_template('adminRestList.html', username=username, messages=msg)

#管理员查看用户信息
@app.route('/adminUserList', methods=['GET', 'POST'])
def adminUserPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM Users"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminUserList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminUserList.html', username=username, messages=msg)

#管理员管理退款
@app.route('/adminOrderList', methods=['GET', 'POST'])
def adminOrder():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM Orders where Status=6"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminOrderList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminOrderList.html', username=username, messages=msg)

    elif request.form["action"]=="退款成功":
        order_id1 = request.form['order_id1']

        # 连接数据库
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        try:
            with db.cursor() as cursor:
                # 更新数据库
                sql = "UPDATE Orders SET Status=7 WHERE OrderID = %s"  # 假设你的表名是ORDERS，字段是status和id
                cursor.execute(sql, (order_id1))

            db.commit()
            msg = "Order status updated successfully!"

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            msg = "Error updating order status!"

        finally:
            db.close()

        return redirect(url_for('adminOrder'))

    elif request.form["action"]=="退款失败":
        order_id2 = request.form['order_id2']

        # 连接数据库
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        try:
            with db.cursor() as cursor:
                # 更新数据库
                sql = "UPDATE Orders SET Status=8 WHERE OrderID = %s"
                cursor.execute(sql, (order_id2))

            db.commit()
            msg = "Order status updated successfully!"

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            msg = "Error updating order status!"

        finally:
            db.close()

        return redirect(url_for('adminOrder'))




# 管理员查看评论列表
@app.route('/adminCommentList', methods=['GET', 'POST'])
def adminCommentPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT Orders.OrderID,Orders.UserID,Orders.Status,Orders.OrderTotalPrice,Comments.Description,transactiontime FROM Orders join Comments on Comments.OrderID=Orders.OrderID WHERE Orders.Status in(5,7,8) AND Comments.Description <> ''"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminCommentList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminCommentList.html', username=username, messages=msg)


# 用户登录后显示商家列表
@app.route('/UserRestList',methods=['GET', 'POST'])
def UserRestListPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM Shop"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('UserRestList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('UserRestList.html', username=username, messages=msg)

#选择商家进入菜单列表
@app.route('/Menu',methods=['GET', 'POST'])
def menu():
    msg = ""
    global restaurant
    if request.form["action"] == "进入本店":
        restaurant = request.form['restaurant']
        print(restaurant)
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM Dishes WHERE ShopID = '%s'" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "特色菜":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM DISHES WHERE restaurant = '%s' AND isSpecialty = 1" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "按销量排序":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY sales DESC" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY price DESC" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)

# 查看商家评论
@app.route('/ResComment',methods=['GET','POST'])
def resComment():
    msg = ""
    global restaurant
    if request.form["action"] == "查看评价":
        restaurant = request.form['restaurant']
        print(restaurant)
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s' AND isFinished = 1 AND text <> '' "% restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('ResComment.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('ResComment.html', username=username, RESTAURANT=restaurant, messages=msg)

# 商家查看评论
@app.route('/ResCommentList', methods=['GET', 'POST'])
def ResCommentList():
    msg = ""
    # 连接数据库，默认数据库用户名root，密码空
    restaurant=username
    print(restaurant)
    db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use appDB")
    except:
        print("Error: unable to use database!")
    # 查询
    sql = "SELECT Orders.OrderID,Orders.UserID,Orders.Status,Orders.OrderTotalPrice,Comments.Description,transactiontime FROM Orders join Comments on Comments.OrderID=Orders.OrderID WHERE Orders.ShopID = '%s' AND Orders.Status in(5,7,8) AND Comments.Description <> '' " % restaurant
    cursor.execute(sql)
    res = cursor.fetchall()
    # print(res)
    # print(len(res))
    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        return render_template('ResCommentList.html', username=username, RESTAURANT=restaurant, result=res,
                                   messages=msg)
    else:
        print("NULL")
        msg = "none"
    return render_template('ResCommentList.html', username=username, RESTAURANT=restaurant, messages=msg)

# 404跳转
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

order_id=None
yhq=None
new_status=None
price=None
# 购物车
@app.route('/settlement',methods=['GET', 'POST'])
def shopping():
    msg = ""
    global order_id
    global yhq
    global new_status
    global price
    if request.method == 'GET':
        #print("myOrder-->GET")
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "insert into Orders(ShopID,UserID) values('{}' ,'{}')".format(restaurant, username)
        cursor.execute(sql)
        db.commit()
        # 查询
        sql = "SELECT * FROM Dishes WHERE ShopID = '%s'" % restaurant
        cursor.execute(sql)
        res1 = cursor.fetchall()
        sql = "SELECT * from Orders where OrderID=LAST_INSERT_ID()"
        cursor.execute(sql)
        res2 = cursor.fetchall()
        order_id = res2[0][0]

        # 目前的价钱
        price = 0.0
        # print(len(res))
        if len(res1) != 0 and len(res2) != 0:
            msg = "done"
            print(msg)
            #print(len(res1))
            return render_template('settlement.html', username=username, result1=res1,pr=price,oid=order_id, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('settlement.html', username=username, messages=msg)


    elif request.form["action"] == "选择":

        #order_id = request.form.get('order_id')
        new_status = request.form.get('new_status')

        # 连接数据库
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "call  Sel_dish({},{})".format(int(order_id),int(new_status))
        cursor.execute(sql)
        db.commit()

        sql = "select OrderTotalPrice from Orders where OrderID ={}".format(int(order_id))
        cursor.execute(sql)
        res2 = cursor.fetchall()
        #目前的价钱
        price=float(res2[0][0])

        #菜品信息
        sql = "SELECT * FROM Dishes WHERE ShopID = '%s'" % restaurant
        cursor.execute(sql)
        res1 = cursor.fetchall()
        # print(len(res))
        if len(res1) != 0 :
            msg = "done"
            print(msg)
            #print(len(res1))
            return render_template('settlement.html', username=username, result1=res1,pr=price,oid=order_id,
                                           messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('settlement.html', username=username, messages=msg)



    elif request.form["action"] == "提交":
        yhq = request.form.get('yhq')
        #order_id = request.form.get('order_id')
        print(order_id)
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        if len(yhq)!=0:
            # 更新订单表
            sql = "update Orders set CouponID={} where OrderID={}".format(int(yhq), int(order_id))
            cursor.execute(sql)
            db.commit()
            # 更新用户拥有表
            sql = "update UsersCoupons set Quantity=Quantity-1 where UserID='{}' and CouponID={}".format(username,
                                                                                                         int(yhq))
            cursor.execute(sql)
            db.commit()
        msg = "Order status updated successfully!"
        sql = "SELECT * FROM Dishes WHERE ShopID = '%s'" % restaurant
        cursor.execute(sql)
        res1 = cursor.fetchall()
        # print(len(res))
        if len(res1) != 0 :
            msg = "done"
            print(msg)
            print(len(res1))
            return render_template('settlement.html', username=username, result1=res1,pr=price,oid=order_id,
                                   messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('settlement.html', username=username, messages=msg)

    else:
        print("咋回事")
        return render_template('index.html')

@app.route('/jiesuan',methods=['GET', 'POST'])
def js():
    if request.method == 'GET':
        print(order_id)
        #print("myOrder-->GET")
        db =  pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB",charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "call settlement({},{})".format(int(order_id), int(yhq))
        cursor.execute(sql)
        db.commit()
        # 查询
        sql = "SELECT * FROM Orders WHERE OrderID={}".format(int(order_id))
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('jiesuan.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('jiesuan.html', username=username, messages=msg)



    else:
        print("咋回事")
        return render_template('index.html')

# 个人中心页面
@app.route('/personal')
def personalPage():
    return render_template('personal.html')


# 修改个人信息页面
@app.route('/ModifyPersonalInfo', methods=['GET', 'POST'])
def ModifyPersonalInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "Update {} SET address = '{}', phone = '{}' where username = '{}'".format(userRole, address, phonenum,
                                                                                        username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('ModifyPersonalInfo.html', messages=msg, username=username)


# 修改密码页面
@app.route('/ModifyPassword', methods=['GET', 'POST'])
def ModifyPassword():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPassword.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            # 连接数据库，默认数据库用户名root，密码空
            db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "Update {} SET password = '{}' where username = '{}'".format(userRole, psw1, username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('ModifyPassword.html', messages=msg, username=username)
        else:
            msg = "not equal"
            return render_template('ModifyPassword.html', messages=msg, username=username)


# 用户订单页面
@app.route('/OrderPage', methods=['GET', 'POST'])
def OrderPage():
    msg = ""
    global notFinished_num
    # 显示订单
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use test2")
        except:
            print("Error: unable to use database!")

        # 查询未完成订单数量,status = 1 /2 /3 /4
        unfinished_sql = "SELECT * FROM orders WHERE userID = '%s' AND (status = 1 or status = 2 or status = 3 or status = 4)" % username
        cursor.execute(unfinished_sql)
        unfinished_res = cursor.fetchall()
        print(unfinished_res)
        notFinished_num = len(unfinished_res)
        print(f"未完成订单数量{notFinished_num}")

        # 查询已完成订单数量 status = 5 /7 /8
        finished_sql = "SELECT * FROM orders WHERE userID = '%s' AND (status = 5 or status = 7 or status = 8)" % username
        cursor.execute(finished_sql)
        finished_res = cursor.fetchall()
        print(finished_res)
        finished_num = len(finished_res)
        print(f"已完成订单数量{finished_num}")

        # 查询待退款订单数量 status = 6
        pending_refund_sql = "SELECT * FROM orders WHERE userID = '%s' AND status = 6" % username
        cursor.execute(pending_refund_sql)
        pending_refund_res = cursor.fetchall()
        print(pending_refund_res)
        pending_refund_num = len(pending_refund_res)
        print(f"已完成订单数量{pending_refund_num}")

        if len(unfinished_res) and len(finished_res) and len(pending_refund_res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   messages=msg)

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "确认收货":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use test2")
        except:
            print("Error: unable to use database!")
        print("用户要确认收货啦")
        orderID = request.form.get('orderID')
        print(f"orderID为{orderID}")
        # 更新订单状态，使其进入已完成序列
        sql1 = "UPDATE orders SET status = 5 where orderID = %s"
        cursor.execute(sql1, (orderID,))
        db.commit()

        # 查询未完成订单数量
        unfinished_sql = "SELECT * FROM orders WHERE userID = '%s' AND (status = 1 or status = 2 or status = 3 or status = 4)" % username
        cursor.execute(unfinished_sql)
        unfinished_res = cursor.fetchall()
        print(unfinished_res)
        notFinished_num = len(unfinished_res)
        print(f"未完成订单数量{notFinished_num}")
        # 查询已完成订单数量
        finished_sql = "SELECT * FROM orders WHERE userID = '%s' AND (status = 5 or status = 7 or status = 8)" % username
        cursor.execute(finished_sql)
        finished_res = cursor.fetchall()
        print(finished_res)
        finished_num = len(finished_res)
        print(f"已完成订单数量{finished_num}")

        # 查询待退款订单数量
        pending_refund_sql = "SELECT * FROM orders WHERE userID = '%s' AND status = 6" % username
        cursor.execute(pending_refund_sql)
        pending_refund_res = cursor.fetchall()
        print(pending_refund_res)
        pending_refund_num = len(pending_refund_res)
        print(f"已完成订单数量{pending_refund_num}")

        if len(unfinished_res) and len(finished_res) and len(pending_refund_res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   messages=msg)
    # 跳转到写评价页面
    elif request.form["action"] == '去评价':
        print("跳转到评价页面")
        return render_template('WriteComments.html', username=username, messages=msg)

    # 申请退款，即status=6
    elif request.form["action"] == '申请退款':
        print("进入申请退款函数")
        db = pymysql.connect(host="localhost", user="root", password='0158', database="test2", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use test2")
        except:
            print("Error: unable to use database!")
        print("用户要申请退款")
        orderID = request.form.get('orderID')
        print(f"orderID为{orderID}")
        # 更新订单状态，
        sql1 = "UPDATE orders SET status = 6 where orderID = %s"
        cursor.execute(sql1, (orderID,))
        print("execute")
        db.commit()
        print("committed")

        # 查询未完成订单数量
        unfinished_sql = "SELECT * FROM orders WHERE userID = '%s' AND (status = 1 or status = 2 or status = 3 or status = 4)" % username
        cursor.execute(unfinished_sql)
        unfinished_res = cursor.fetchall()
        print(unfinished_res)
        notFinished_num = len(unfinished_res)
        print(f"未完成订单数量{notFinished_num}")
        # 查询已完成订单数量
        finished_sql = ("SELECT * FROM orders WHERE userID = '%s' AND "
                        "(status = 5 or status = 7 or status = 8)") % username
        cursor.execute(finished_sql)
        finished_res = cursor.fetchall()
        print(finished_res)
        finished_num = len(finished_res)
        print(f"已完成订单数量{finished_num}")

        # 查询待退款订单数量
        pending_refund_sql = "SELECT * FROM orders WHERE userID = '%s' AND status = 6" % username
        cursor.execute(pending_refund_sql)
        pending_refund_res = cursor.fetchall()
        print(pending_refund_res)
        pending_refund_num = len(pending_refund_res)
        print(f"已完成订单数量{pending_refund_num}")

        if len(unfinished_res) and len(finished_res) and len(pending_refund_res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   messages=msg)


# 我的评论页面
@app.route('/MyComments', methods=['GET', 'POST'])
def MyCommentsPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use test2")
        except:
            print("Error: unable to use database!")
        # 查询已完成订单(此处未改)
        unfinished_sql = "SELECT * FROM orders WHERE userID = '%s' AND status != 5 and status != 7 and status != 8" % username
        cursor.execute(unfinished_sql)
        unfinished_res = cursor.fetchall()
        print(unfinished_res)
        notFinished_num = len(unfinished_res)
        print(f"未完成订单数量{notFinished_num}")
        if len(unfinished_res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username,
                                   unfinished_result=unfinished_res, messages=msg,
                                   notFinishedNum=notFinished_num)
        else:
            print("NULL")
            msg = "none"
            return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY transactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "待评价订单":
        # 未评价订单跳转到写评论中
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print("MyCommentsPage - 未评价订单: {}".format(len(res)))
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("MyCommentsPage - 待评价订单 - NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=len(res))

    else:
        return render_template('MyComments.html', username=username, messages=msg)


# 写评论页面
@app.route('/WriteComments', methods=['GET', 'POST'])
def WriteCommentsPage():
    msg=""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use test2")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单
        unfinished_sql = "SELECT * FROM orders WHERE userID = '%s' AND (status = 1 or status = 2 or status = 3 or status = 4)" % username
        cursor.execute(unfinished_sql)
        unfinished_res = cursor.fetchall()
        print(unfinished_res)
        notFinished_num = len(unfinished_res)
        print(f"未完成订单数量{notFinished_num}")
        if len(unfinished_res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username,
                                   unfinished_result=unfinished_res, messages=msg,
                                   notFinishedNum=notFinished_num)
        else:
            print("NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username,
                                   unfinished_result=unfinished_res, messages=msg,
                                   notFinishedNum=notFinished_num)
    elif request.method == 'POST':
        comment = request.form['comment']
        # 第一，WriteComments中使用for循环来展示订单，导致评论只输入一个，待评价的订单就没了
        # 第二，修改orders的stastu状态为已评价
        print(comment)
        return render_template('WriteComments.html', username=username, messages=msg)
    else:
        return render_template('WriteComments.html', username=username, messages=msg)


# 用户评论页面
@app.route('/CommentForm', methods=['GET', 'POST'])
def CommentFormPage():
    msg = ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "写评论":
        orderID = request.form['orderID']
        print(orderID)
        msg = "WriteRequest"
        print(msg)
        return render_template('CommentForm.html', username=username, orderID=orderID, messages=msg)
    elif request.form["action"] == "提交评论":
        print("提交评论!")
        orderID = request.form.get('orderID')
        c_rank = request.form.get('rank')
        text = request.form.get('text')
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "Update ORDER_COMMENT SET text = '{}', c_rank = {} where orderID = '{}'".format(text, c_rank, orderID)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print("用户评论成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("用户评论失败")
            msg = "fail"
        return render_template('CommentForm.html', messages = msg, username=username)

# 钱包（查看余额 充值钱包）
@app.route('/Wallet', methods=['GET', 'POST'])
def wallet():
    msg = ""
    if request.method == 'GET':
        # 连接数据库
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        # 创建一个游标对象
        cursor = db.cursor()
        try:
            # 使用参数化查询防止 SQL 注入
            sql = "SELECT money FROM users WHERE userID = %s"
            cursor.execute(sql, (username,))
            # 获取查询结果
            result = cursor.fetchone()
            money = result[0]  # 打印查询到的 username
        finally:
            # 关闭游标和数据库连接
            cursor.close()
            db.close()
        return render_template('Wallet.html', username=username, money=money)

    if request.method == 'POST':
        # 连接数据库
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        # 创建游标对象
        cursor = db.cursor()
        # 获取用户的充值金额
        recharge_amount = request.form.get('rechargeAmount')
        print(f"收到的充值金额为: {recharge_amount}")
        with cursor as cursor:
            # 调用存储过程
            cursor.callproc("recharge", (recharge_amount, username))
            db.commit()
            try:
                # 更新余额
                sql = "SELECT money FROM users WHERE userID = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                money = result[0]
            finally:
                sql_test = "select money from users where userid = {}".format(username)
                db.close()

        return render_template('Wallet.html', username=username, money=money)


# 商家查看菜品信息
@app.route('/MerchantMenu',methods=['GET', 'POST'])
def MerchantMenu():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT Dishes.DishName,Dishes.ShopID,DishDescription,DishPrice,Dishes.Quantity,Dishes.imgsrc FROM Dishes WHERE Dishes.ShopID = '%s'" % username

        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
    if request.method == 'POST':
        if request.form["action"] == "删除该菜品":
            dishname = request.form.get('dishname')
            rest = request.form.get('restaurant')
            print(rest)
            db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "DELETE FROM Dishes where Dishes.DishName = '{}' and Dishes.ShopID = '{}'".format(dishname,rest)
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
                print("菜品删除成功")
                dmsg = "done"
            except ValueError as e:
                print("--->", e)
                print("菜品删除失败")
                dmsg = "fail"
            return render_template('MerchantMenu.html', dishname=dishname, rest=rest, dmessages=dmsg)
        elif request.form["action"] == "按数量排序":
            db = pymysql.connect(host="localhost", user="root", password='123456', database="appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT Dishes.DishName,Dishes.ShopID,DishDescription,DishPrice,Dishes.Quantity,Dishes.imgsrc FROM Dishes WHERE Dishes.ShopID = '%s' Order BY Dishes.Quantity DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html',username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
        elif request.form["action"] == "按价格排序":
            db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT Dishes.DishName,Dishes.ShopID,DishDescription,DishPrice,Dishes.Quantity,Dishes.imgsrc FROM Dishes WHERE Dishes.ShopID = '%s' Order BY Dishes.DishPrice DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username,messages=msg)


# 商家修改菜品信息
@app.route('/MenuModify', methods=['GET', 'POST'])
def MenuModify():
    msg = ""

    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "修改菜品信息":
        dishname = request.form['dishname']#传递过去菜品名
        rest = request.form['restaurant']#传递过去商家名
        dishinfo = request.form['dishinfo']
        price = request.form.get('price')
        num = request.form.get('num')
        #imagesrc = request.form['imagesrc']
        print(dishname)

        
		
        return render_template('MenuModify.html', dishname=dishname, rest=rest, dishinfo=dishinfo,  price=price, num=num,username=username, messages=msg)
    elif request.form["action"] == "提交修改":

        dishname = request.form.get('dishname')
        rest = request.form.get('rest')
        dishinfo = request.form['dishinfo']
        price = request.form.get('price')
        num = request.form.get('num')


        db = pymysql.connect(host="localhost", user="root", password='123456', database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "Update Dishes SET DishDescription = '{}', DishPrice = {} ,Dishes.Quantity={}  where DishName = '{}'".format(dishinfo,price,num,dishname)
        print(sql)
		
        try:
            cursor.execute(sql)
            db.commit()
            print("菜品信息修改成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("菜品信息修改失败失败")
            msg = "fail"
        return render_template('MenuModify.html',dishname=dishname, rest=rest, username=username, messages=msg)

@app.route('/MenuAdd',methods=['GET','POST'])
def MenuAdd():
    msg = ""
    rest= ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "增加菜品":
        rest = request.form['restaurant']#传递过去商家名
        return render_template('MenuAdd.html',rest=rest)
    elif request.form["action"] == "确认增加":

        dishname = request.form.get('dishname')
        rest = request.form.get('rest')
        dishinfo = request.form.get('dishinfo')
        price = request.form.get('price')
        numb = request.form.get('num')

        db = pymysql.connect(host="localhost", user="root", password='123456', database="appDB", charset='utf8')

        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql1 = "SELECT * FROM Dishes where Dishes.DishName = '{}' ".format(dishname)
        cursor.execute(sql1)
        db.commit()
        res1 = cursor.fetchall()
        num = 0
        for row in res1:
            num = num + 1
        # 如果已经存在该商家
        if num == 1:
            print("失败！该菜品已经添加过！")
            msg = "fail1"
        else:
            sql2 = "insert into Dishes(DishPrice,DishName,DishDescription,ShopID,Dishes.Quantity)  values ('{}','{}','{}',{}, {}) ".format(price,dishname,dishinfo,rest,numb)
            print(sql2)
            try:
                cursor.execute(sql2)
                db.commit()
                print("菜品添加成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("菜品添加失败")
                msg = "fail"
        return render_template('MenuAdd.html', messages=msg, username=username)


# 外卖员订单页面
@app.route('/DPIndex',methods=['GET','POST'])
def DPIndexPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        presql = "SELECT * FROM Orders WHERE DeliveryPersonID = '%s' AND Status = 3 order by PickupTime" % username
        cursor.execute(presql)
        res = cursor.fetchall()
        notFinishedNum = len(res)
        if len(res):
            msg = "done"
            print(msg)
            return render_template('DPIndex.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('DPIndex.html', username=username, messages=msg)

    elif request.method == 'POST' and request.form.get("action") == "订单送达":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        print("外卖员订单确认送达啦")
        orderID = request.form['orderID']
        print(orderID)

        try:
            cursor.callproc('dpConfirm', (orderID,))
            db.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.rollback()

        msg = "UpdateSucceed"
        return render_template('DPIndex.html', username=username, messages=msg)

    else:
        return render_template('DPIndex.html', username=username, messages=msg)


@app.route('/DPpersonal',methods=['GET','POST'])
def DPpersonalPage():
    if request.method == 'GET':
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        presql = "SELECT * FROM DeliveryPersons WHERE DeliveryPersonID = '%s'" % username
        cursor.execute(presql)
        res = cursor.fetchall()
        res = res[0][4]
        return render_template('DPpersonal.html', username=username, type=res)

    elif request.method == 'POST' and request.form.get("action") == "确定":
        if request.form.get("order") == "1":
            status = 1
        else:
            status = 0

        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        presql = "update DeliveryPersons set IsDeliveried = %d WHERE DeliveryPersonID = '%s'" %(status, username)
        cursor.execute(presql)
        db.commit()
        print(presql)
        return render_template('DPpersonal.html', username=username, type=status)

@app.route('/MerchantIndex')
def Merchantindexpage():
    return render_template('MerchantIndex.html')


# 个人中心页面
@app.route('/MerchantPersonal')
def MpersonalPage():
    return render_template('MerchantPersonal.html')



# 展示商家个人信息页面
@app.route('/MerchantViewPerInfo',methods=['GET', 'POST'])
def MerchantViewPerInfo():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT ShopID,ShopPassword,ShopAddress,ShopPhone,Shop.img_res,Shop.Turnover from Shop where ShopID = '{}'" .format(username)

        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('MerchantViewPerInfo.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantViewPerInfo.html', username=username, messages=msg)



# 修改个人信息页面
@app.route('/MerchantModifyPerInfo', methods=['GET', 'POST'])
def MerchantModifyPerInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPerInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
        f = request.files['imagesrc']
        filename = ''
		
        if f !='' and allowed_file(f.filename):
            filename = secure_filename(f.filename)
			
        if filename != '':
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename

        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
			
        if filename == '':	
            sql = "Update Shop SET ShopAddress = '{}', ShopPhone = '{}' where ShopID = '{}'".format(address, phonenum,
                                                                                        username)
        else:
            sql = "Update Shop SET ShopAddress = '{}', ShopPhone = '{}',img_res = '{}' where ShopID = '{}'".format(address, phonenum, imgsrc,
                                                                                        username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('MerchantModifyPerInfo.html', messages=msg, username=username)


# 修改密码页面
@app.route('/MerchantModifyPwd', methods=['GET', 'POST'])
def MerModifyPassword():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPwd.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            # 连接数据库，默认数据库用户名root，密码空
            db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "Update Shop SET ShopPassword = '{}' where ShopID = '{}'".format(psw1, username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)
        else:
            msg = "not equal"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)


# 商家查看订单
@app.route('/MerchantOrderPage', methods=['GET', 'POST'])
def MerchantOrderPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use test2")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        presql = "SELECT Orders.OrderID,Orders.UserID,Orders.ShopID,Orders.Status,OrderTotalPrice,Comments.Description,transactiontime FROM Orders join Comments on Comments.OrderID=Orders.OrderID WHERE Orders.ShopID = '%s' AND Orders.Status in(1) AND Comments.Description <> '' " % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT Orders.OrderID,Orders.UserID,Orders.ShopID,Orders.Status,OrderTotalPrice,Comments.Description,transactiontime FROM Orders join Comments on Comments.OrderID=Orders.OrderID WHERE Orders.ShopID = '%s' AND Orders.Status in(5,6,7,8)" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res1, finish=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY transactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)

    elif request.method == 'POST' and request.form["action"] == "确认接单":

        oid = request.form.get("orderID")
        db = pymysql.connect(host="localhost", user=user_name, password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "update Orders set Status = 2  where orderID = %s" % oid
        cursor.execute(sql)
        db.commit()

        try:
            cursor.callproc('deliveryAssignment', (oid,))
            db.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.rollback()

        presql = "SELECT Orders.OrderID,Orders.UserID,Orders.ShopID,Orders.Status,OrderTotalPrice,Comments.Description,transactiontime FROM Orders join Comments on Comments.OrderID=Orders.OrderID WHERE Orders.ShopID = '%s' AND Orders.Status in(1) AND Comments.Description <> '' " % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT Orders.OrderID,Orders.UserID,Orders.ShopID,Orders.Status,OrderTotalPrice,Comments.Description,transactiontime FROM Orders join Comments on Comments.OrderID=Orders.OrderID WHERE Orders.ShopID = '%s' AND Orders.Status in(5,6,7,8)" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res1, finish=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantOrderPage.html', username=username, messages=msg)

    else:
        return render_template('MerchantOrderPage.html', username=username, messages=msg)




def parse_args():
    """parse the command line args

    Returns:
        args: a namespace object including args
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--mysql_pwd',
        help='the mysql root password',
        default="11235813"
    )
    parser.add_argument(
        '--db_name',
        help='which database to use',
        default="appDB"
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    mysql_pwd = args.mysql_pwd
    db_name = args.db_name
    app.run(host='localhost', port='9090')
