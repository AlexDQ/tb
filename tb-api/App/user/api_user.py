# -*- coding: utf-8 -*-

'''
    Create on
    @author:
    @summary: 用户信息
'''
import json
import sys
from flask import Blueprint, g, request, Response
reload(sys)
sys.setdefaultencoding("utf8")

app = Blueprint(__name__ + "_app", __name__)


# 获取当前用户信息接口
@app.route('/api/currentUser', methods=['GET'])
def currentUser():
    try:
        # 传入参数
        userid = request.args.get("login_id", "")  # 序号
        sql_sel = """  
            SELECT login_id,   -- 序号
                   username as name, -- 用户名
                   age,              -- 年龄
                   case when sex = 'male' then '男'
                        when sex = 'female' then '女'  
                   end as sex,      -- 性别
                   address,         -- 地址
                   email,           -- 邮箱
                   case when role = 'admin' then '管理员'
                        when role = 'user'  then '用户'
                   end as role,     -- 角色
                   tel as 'call',   -- 联系方式 
                   date_format(r_time, '%%Y-%%m-%%d %%H:%%m:%%s') as 'time' -- 注册时间
            from login_info
            where login_id = '%s'
        """ % (userid, )

        '''用户名和密码查询'''
        g.cursor.execute(sql_sel)
        sql_name = g.cursor.fetchone()
        # 返回结果
        if sql_name is None:
            g.res = {
                "code":"500",
                "success": False,
                "msg": "获取用户信息失败"
            }
        else:
            g.res = {
                "code": 200,
                "success":True,
                "msg": "获取用户信息成功",
                "obj": {
                    "name": sql_name["username"],
                    "userid": sql_name["login_id"],
                    "email": sql_name["email"],
                    "authority": [
                        sql_name["role"]
                    ]
                }
            }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 获取用户列表接口
@app.route('/api/useinfo/list', methods=['GET'])
def useinfo_list():
    try:
        # 传入参数
        name = request.args.get("name", "")  # 用户名
        source = request.args.get("pageNo")
        pageSize = int(request.args.get("pageSize"))
        pageNo = (int(request.args.get("pageNo")) - 1) * pageSize

        where = "where state = '1' "
        if name:
            where = where + "and username = '%s' " % name

        sql_sel = """
            SELECT login_id,   -- 序号
                   username as name, -- 用户名
                   age,              -- 年龄
                   case when sex = 'male' then '男'
                        when sex = 'female' then '女'  
                   end as sex,      -- 性别
                   address,         -- 地址
                   email,           -- 邮箱
                   case when role = 'admin' then '管理员'
                        when role = 'user'  then '用户'
                   end as role,     -- 角色
                   tel as 'call',   -- 联系方式 
                   date_format(r_time, '%%Y-%%m-%%d %%H:%%m:%%s') as 'time' -- 注册时间
            from login_info
            %s
            limit %s offset %s 
        """ % (where, pageSize, pageNo)

        # 基础信息查询
        g.cursor.execute(sql_sel)
        sql_name = g.cursor.fetchall()

        # 计数查询
        g.cursor.execute("""select count(1) as num from login_info %s""" % (where, ))
        count = g.cursor.fetchone()["num"]


        if sql_name is None:
            g.res = {
                "code":"500",
                "success": False,
                "msg": "获取用户信息失败"
            }
        else:
            g.res = {
                "code": 200,
                "success":True,
                "msg": "获取用户信息成功",
                "obj": {
                    "totalPage": count / pageSize + 1,
                    "totalCount": count,
                    "pageSize": pageSize,
                    "pageNo": int(source),
                    "result": sql_name
                }
            }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 获取用户详情
@app.route('/api/userinfo/details', methods=['GET'])
def useinfo_details():
    try:
        # 传入参数
        userid = request.args.get("login_id")

        sql_sel = """
            SELECT login_id,   -- 序号
                   username as name, -- 用户名
                   age,              -- 年龄
                   case when sex = 'male' then '男'
                        when sex = 'female' then '女'  
                   end as sex,      -- 性别
                   address,         -- 地址
                   email,           -- 邮箱
                   case when role = 'admin' then '管理员'
                        when role = 'user'  then '用户'
                   end as role,     -- 角色
                   tel as 'call',   -- 联系方式 
                   date_format(r_time, '%%Y-%%m-%%d %%H:%%m:%%s') as 'time' -- 注册时间
            from login_info
            where state = '1' and login_id = '%s'
        """ % (userid)

        '''用户名和密码查询'''
        g.cursor.execute(sql_sel)
        sql_name = g.cursor.fetchone()

        if sql_name is None:
            g.res = {
                "code":"500",
                "success": False,
                "msg": "获取用户详情失败"
            }
        else:
            g.res = {
                "code": 200,
                "success":True,
                "msg": "获取用户详情成功",
                "obj": sql_name
            }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 新增/修改用户
@app.route('/api/userinfo/add', methods=['POST'])
def useinfo_add():
    try:
        # 传入参数
        data_all = request.form
        userid = data_all.get("login_id", "") # 序号 有序号则修改 没有序号新增
        username = data_all.get("name", "")   # 用户名
        sex =  data_all.get("sex", "")        # 性别
        age = data_all.get("age", "")         # 年龄
        address = data_all.get("address", "") # 地址
        email = data_all.get("email", "")     # 邮箱
        call = data_all.get("call", "")       # 电话

        if userid:
            sql_sel = """
                update login_info
                set username = '%s',
                    email = '%s',
                    age = '%s',
                    sex = '%s',
                    address = '%s',
                    tel = '%s'
                where login_id = '%s'
            """ % (username, email, age, sex, address, call, userid)
            g.cursor.execute(sql_sel)
            g.conn.commit()
            g.res = {
                "code": 200,
                "success":True,
                "msg": "修改用户信息成功",
            }

        else:
            # 新增用户时 判断用户名是否存在
            sql_sel = """
                SELECT username
                FROM login_info
                where username = '%s' and state = '1'
            """ % (username)
            g.cursor.execute(sql_sel)
            sql_name = g.cursor.fetchall()

            '''查询到数据后判断为用户名已存在'''
            if len(sql_name) > 0:
                g.res = {
                    "code":"500",
                    "success": False,
                    "msg": "用户名已存在"
                }
            else:
                sql_sel = """insert into login_info(username, passwd, email, age, sex, address, role, state, tel, r_time)
                             values('%s', '%s', '%s', '%s', '%s', '%s', 'user', '1', '%s', now())""" % (username, email, email, age, sex, address, call)
                g.cursor.execute(sql_sel)
                g.conn.commit()
                g.res = {
                    "code": 200,
                    "success":True,
                    "msg": "新增用户成功",
                }

    except Exception as e:
        g.res = {
            "code":"500",
            "success": False,
            "msg": "获取用户详情失败"
        }
        return json.dumps(g.res, ensure_ascii=False)


# 删除用户
@app.route('/api/userinfo/delete', methods=['POST'])
def user_delete():
    try:
        data_all = request.form
        ids = data_all.get("id").split(',')  # 序号 ,连接 如：1,2,3
        for i in ids:
            g.cursor.execute("""update login_info set state = '0' where login_id = '%s'""" % i)
        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "删除用户成功"
        }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 用户密码重置
@app.route('/api/userinfo/resetPassword', methods=['POST'])
def resetPassword():
    try:
        data_all = request.form
        _id = data_all.get("login_id")
        g.cursor.execute("""update login_info set passwd = email where login_id = '%s'""" % _id)
        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "重置用户密码成功"
        }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)