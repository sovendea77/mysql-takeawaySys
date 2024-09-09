# import pymysql
#
# # 连接数据库
# db = pymysql.connect(host="localhost", user="root", password="0158", database="Test1", charset='utf8')
# # 创建一个游标对象
# cursor = db.cursor()
# try:
#     # 使用参数化查询防止 SQL 注入
#     sql = "SELECT phone FROM customer WHERE username = %s"
#     cursor.execute(sql, ("小张",))
#     # 获取查询结果
#     result = cursor.fetchone()
#     if result:
#         print(result[0])  # 打印查询到的 username
#     else:
#         print("没有找到对应的用户名")
# finally:
#     # 关闭游标和数据库连接
#     cursor.close()
#     db.close()



# 用户订单页面
@app.route('/OrderPage', methods=['GET', 'POST'])
def OrderPage():
    msg = ""
    global notFinished_num
    # 显示订单
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user="root", password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询未完成订单数量,status = 1 /2 /3 /4
        unfinished_sql = "SELECT * FROM orders WHERE userID = %s AND status in (1, 2, 3, 4)" % username
        cursor.execute(unfinished_sql)
        unfinished_res = cursor.fetchall()
        print(unfinished_res)
        notFinished_num = len(unfinished_res)
        print(f"未完成订单数量{notFinished_num}")

        # 查询已完成订单数量 status = 5 /7 /8
        finished_sql = "SELECT * FROM orders WHERE userID = %s AND status in (5, 7 ,8)" % username
        cursor.execute(finished_sql)
        finished_res = cursor.fetchall()
        print(finished_res)
        finished_num = len(finished_res)
        print(f"已完成订单数量{finished_num}")

        # 查询待退款订单数量 status = 6
        pending_refund_sql = "SELECT * FROM orders WHERE userID = %s AND status = 6" % username
        cursor.execute(pending_refund_sql)
        pending_refund_res = cursor.fetchall()
        print(pending_refund_res)
        pending_refund_num = len(pending_refund_res)
        print(f"待退款订单数量{pending_refund_num}")

        # 展示订单的菜品图片
        orderdishes_sql = "select od.* from orders o join ordersdishes od on o. OrderID = od.OrderNumber where o.UserID = %s" % username
        cursor.execute(orderdishes_sql)
        orderdishes_median = cursor.fetchall()
        print(orderdishes_median)
        orderdishes_res = []
        for od in orderdishes_median:
            od_list = list(od)
            od_list[2] = "static/images/" + od_list[2]
            orderdishes_res.append(od_list)
        print(f"订单菜品新列表：{orderdishes_res}")

        if len(unfinished_res) and len(finished_res) and len(pending_refund_res) and len(orderdishes_median):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   orderdishes_result=orderdishes_res,
                                   messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   orderdishes_result=orderdishes_res,
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

    # 确认收货
    elif request.form["action"] == "确认收货":
        db = pymysql.connect(host="localhost", user="root", password=pwd, database="appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
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
        unfinished_sql = "SELECT * FROM orders WHERE userID = %s AND status in (1, 2, 3, 4)" % username
        cursor.execute(unfinished_sql)
        unfinished_res = cursor.fetchall()
        print(unfinished_res)
        notFinished_num = len(unfinished_res)
        print(f"未完成订单数量{notFinished_num}")
        # 查询已完成订单数量
        finished_sql = "SELECT * FROM orders WHERE userID = %s AND status in (5, 7 ,8)" % username
        cursor.execute(finished_sql)
        finished_res = cursor.fetchall()
        print(finished_res)
        finished_num = len(finished_res)
        print(f"已完成订单数量{finished_num}")

        # 查询待退款订单数量
        pending_refund_sql = "SELECT * FROM orders WHERE userID = %s AND status = 6" % username
        cursor.execute(pending_refund_sql)
        pending_refund_res = cursor.fetchall()
        print(pending_refund_res)
        pending_refund_num = len(pending_refund_res)
        print(f"已完成订单数量{pending_refund_num}")

        # 展示订单的菜品图片
        orderdishes_sql = "select od.* from orders o join ordersdishes od on o. OrderID = od.OrderNumber where o.UserID = %s" % username
        cursor.execute(orderdishes_sql)
        orderdishes_median = cursor.fetchall()
        print(orderdishes_median)
        orderdishes_res = []
        for od in orderdishes_median:
            od_list = list(od)
            od_list[2] = "static/images/" + od_list[2]
            orderdishes_res.append(od_list)
        print(f"订单菜品新列表：{orderdishes_res}")

        if len(unfinished_res) and len(finished_res) and len(pending_refund_res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   orderdishes_result=orderdishes_res,
                                   messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   orderdishes_result=orderdishes_res,
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
            cursor.execute("use appDB")
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
        unfinished_sql = "SELECT * FROM orders WHERE userID = '%s' AND status in (1, 2, 3, 4)" % username
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

        # 展示订单的菜品图片
        orderdishes_sql = "select od.* from orders o join ordersdishes od on o. OrderID = od.OrderNumber where o.UserID = %s" % username
        cursor.execute(orderdishes_sql)
        orderdishes_median = cursor.fetchall()
        print(orderdishes_median)
        orderdishes_res = []
        for od in orderdishes_median:
            od_list = list(od)
            od_list[2] = "static/images/" + od_list[2]
            orderdishes_res.append(od_list)
        print(f"订单菜品新列表：{orderdishes_res}")

        if len(unfinished_res) and len(finished_res) and len(pending_refund_res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   orderdishes_result=orderdishes_res,
                                   messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username,
                                   unfinished_result=unfinished_res, finished_result=finished_res,
                                   pendingRefund_result=pending_refund_res, pendingRefundNum=pending_refund_num,
                                   notFinishedNum=notFinished_num, finishedNum=finished_num,
                                   orderdishes_result=orderdishes_res,
                                   messages=msg)

