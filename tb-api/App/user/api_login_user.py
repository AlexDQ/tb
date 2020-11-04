# -*- coding: utf-8 -*-

'''
    Create on
    @author:
    @summary: 注册、登录
'''
import json
import sys
from flask import Blueprint, g, request, Response
reload(sys)
sys.setdefaultencoding("utf8")

app = Blueprint(__name__ + "_app", __name__)


# 用户登录接口
@app.route('/api/login', methods=['POST'])
def person_login():
    # try:
        # 传入参数
        
        data_all = request.form
        passwd = data_all.get("password") # 密码
        username = data_all.get("email")  # 邮箱 
                                          # 验证码前端随便搞一个就行
        sql_sel = """
            SELECT login_id "id", role, username "name", tel "phone", address, email, sex, age
            from login_info
            where email = '%s' and passwd = '%s' and state = '1'
        """ % (username, passwd)
        print sql_sel

        '''用户名和密码查询'''
        g.cursor.execute(sql_sel)
        sql_name = g.cursor.fetchone()
        # 返回结果
        if sql_name is None:
            g.res = {
                "code":"500",
                "success": False,
                "msg": "登录失败"
            }
        else:
            g.res = {
                "code": 200,
                "success":True,
                "msg": "登录成功",
                "obj": {
                    "userid": sql_name["id"]
                }
            }
    # except Exception as e:
    #     print e
        return json.dumps({"data": g.res, "status": 'success'}, ensure_ascii=False)


# 用户注册接口
@app.route('/api/register', methods=['POST'])
def person_register():
    try:
        # 参数
        data_all = request.form
        username = data_all.get("name")   # 用户名
        sex = data_all.get("sex")         # 性别 取值 male female
        age = data_all.get("age")         # 年龄
        address = data_all.get("address") # 地址
        email = data_all.get("email")     # 邮箱
        call = data_all.get("call")       # 联系方式
        password = data_all.get('password')
        # sql查询
        sql_sel = """
            SELECT username
            FROM login_info
            where (username = '%s' or email = '%s') and state = '1'
        """ % (username, email)
        g.cursor.execute(sql_sel)
        sql_name = g.cursor.fetchall()
        print sql_name
        '''查询到数据后判断为用户名已存在'''
        if len(sql_name) > 0 and sql_name[0]['username'] is not None:
            g.res = {
                "code":"500",
                "success": False,
                "msg": "用户名或邮箱已存在"
            }
        else:
            sql_insert = """
                INSERT INTO login_info(
                        username, passwd, address, email, tel, state, r_time, sex, age)
                VALUES ('%s', '%s', '%s', '%s', '%s', '1', now(), '%s', '%s')
            """ % (username, password, address, email, call, sex, age)

            # 数据录入
            g.cursor.execute(sql_insert)
            g.conn.commit()
            g.res = {
                "code": 200,
                "success":True,
                "msg": "注册成功"
            }
    except Exception as e:
        print e
    return json.dumps(g.res, ensure_ascii=False)


# 修改密码
@app.route('/api/password', methods=['POST'])
def user_updatePass():
    try:
        data_all = request.form
        email = data_all.get("email", "")
        oldpasswd = data_all.get("oldpasswd", "")
        passwd = data_all.get("password", "")
        again = data_all.get("againPassword", "")

        if passwd != again:
            g.res = {
                "code":"500",
                "success": False,
                "msg": "两次密码输入不一致"
            }
        else:
            g.cursor.execute("""select count(1) from login_info where state = '1' and email = '%s' and passwd =  '%s'""" % (email, oldpasswd))
            if not g.cursor.fetchone():
                 return json.dumps(g.res, ensure_ascii=False)
 
            sql = """
                update login_info
                set passwd =  '%s'
                where email = '%s'
            """ % (passwd, email)

            g.cursor.execute(sql)
            g.conn.commit()
            g.res = {
                "code":"200",
                "success": True,
                "msg": "修改密码成功"
            }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 忘记密码
@app.route('/api/forget', methods=['POST'])
def user_forget():
    try:
        data_all = request.form
        email = data_all.get("email", "")
        passwd = data_all.get("password", "")
        again = data_all.get("againPassword", "")

        if passwd != again:
            g.res = {
                "code":"500",
                "success": False,
                "msg": "两次密码输入不一致"
            }
        else:
            sql = """
                update login_info
                set passwd =  '%s'
                where email = '%s'
            """ % (passwd, email)

            g.cursor.execute(sql)
            g.conn.commit()
            g.res = {
                "code":"200",
                "success": True,
                "msg": "修改密码成功"
            }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)