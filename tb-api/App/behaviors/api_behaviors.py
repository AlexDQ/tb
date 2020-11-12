# -*- encoding: utf-8 -*-
'''
    Create on
    @author:
    @summary: 用户行为类型管理
'''
import json
import sys
from flask import Blueprint, g, request, Response
reload(sys)
sys.setdefaultencoding("utf8")

app = Blueprint(__name__ + "_app", __name__)


# 用户行为类型占比
@app.route('/api/behaviors/ana', methods=['GET'])
def behaviors_ana():
    try:
        g.cursor.execute("""select name, count(1) as value from behavior_info where state = '1'
                            group by name""")

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "用户行为类型占比查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        print e
    return json.dumps(g.res, ensure_ascii=False)


# 用户行为类型信息
@app.route('/api/behaviors/info', methods=['POST'])
def behaviors_info():
    try:
        data_all = request.form
        name = data_all.get("name")   # 用户行为类型 取值为“1,2，3,4” 分别表示“点击、收藏、加入购物车、购买”

        where = """where a.state = '1' """

        if name:
            where = where + """ and name like '%%%s%%'""" % name
        g.cursor.execute("""SELECT a.id,   -- 序号
                                   a.name,  -- 类别
                                   b.username, -- 添加人
                                   date_format(a.r_time, '%%Y-%%m-%%d %%H:%%m:%%s') as 'time' -- 注册时间
                            from behavior_info a
                            left join login_info b on a.login_id = b.login_id
                            %s""" % where)
        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "用户行为类型信息查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        print e
    return json.dumps(g.res, ensure_ascii=False)


# 销售数据新增/修改
@app.route('/api/behaviors/add', methods=['POST'])
def behaviors_add():
    # try:
        data_all = request.form
        _id = data_all.get("id")             # 序号
        login_id = data_all.get("login_id")  # 用户ID
        name = data_all.get("name")          # 类别名称
        if _id:
            g.cursor.execute("""update behavior_info 
                                set name = '%s'
                                where id = '%s'""" % (name, _id))
        else:
            g.cursor.execute("""insert into behavior_info(login_id, name,  r_time, state)
                                values('%s', '%s', now(), 1)""" % (login_id, name))

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "操作成功"
        }
    # except Exception as e:
    #     print e
        return json.dumps(g.res, ensure_ascii=False)



# 删除销售信息
@app.route('/api/behaviors/delete', methods=['POST'])
def behaviors_delete():
    # try:
        data_all = request.form
        print data_all.get("id")
        ids = data_all.get("id").split(',')  # 序号 ,连接 如：1,2,3
        for i in ids:
            g.cursor.execute("""update behavior_info set state = '0' where id = '%s'""" % i)
        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "删除用户成功"
        }
    # except Exception as e:
    #     print e
        return json.dumps(g.res, ensure_ascii=False)


# 用户行为类型数据下载
@app.route('/api/behaviors/download', methods=['POST'])
def behaviors_download():
    try:
        data_all = request.form
        ids = data_all.get("id") # 序号 实例：1,2,3
        sql = """
                SELECT a."id",   -- 序号
                       a.name,  -- 类别
                       b.username, -- 添加人
                       date_format(a.r_time, '%%Y-%%m-%%d %%H:%%m:%%s') as 'time' -- 注册时间
                from behavior_info a
                left join login_info b on a.login_id = b.login_id
                where a.id in (%s)
        """ % ids
        g.cursor.execute(sql)
        out = g.cursor.fetchall()

        _path = "./bak.csv"
        # 创建文件对象
        f = open(_path,'wb')
        # 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f)
        # 构建列表头
        csv_writer.writerow(["序号","类别","添加人", "添加时间"])
        # 将数据结果存储到CSV文件
        for i in out:
            csv_writer.writerow([i["id"], i["name"], i["username"], i["time"]])
        response = make_response(send_file(_path))
        response.headers["Content-Disposition"] = "attachment; filename=%s;" % 'bak.csv'
        
    except Exception as e:
        g.res = {
            "code":"500",
            "success": False,
            "msg": "用户行为类型数据下载失败"
        }
        print e
    return response