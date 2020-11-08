# -*- encoding: utf-8 -*-
'''
    Create on
    @author:
    @summary: 销售数据管理
'''
import json
import sys
from flask import Blueprint, g, request, Response
reload(sys)
sys.setdefaultencoding("utf8")

app = Blueprint(__name__ + "_app", __name__)


# 销售数据查询
@app.route('/api/sale/info', methods=['POST'])
def sale_info():
    try:
        data_all = request.form
        behavior_type = data_all.get("behavior_type")   # 用户行为类型 取值为“1,2，3,4” 分别表示“点击、收藏、加入购物车、购买”
        item_id = data_all.get("item_id")               # 商品ID
        item_category = data_all.get("item_category")   # 商品类别ID
        start_time = data_all.get("start_time")         # 起始时间
        end_time = data_all.get("end_time")             # 结束时间

        where = """where state = '1' """

        if behavior_type:
            where = where + """ and behavior_type = '%s'""" % behavior_type
        if item_id:
            where = where + """ and item_id like '%%%s%%'""" % item_id
        if item_category:
            where = where + """ and item_category like '%%%s%%'""" % item_category
        if start_time:
            where = where + """ and date_format(r_time, '%%Y') >= '%s'""" % start_time
        if end_time:
            where = where + """ and date_format(r_time, '%%Y') < '%s'""" % end_time


        g.cursor.execute("""
                        SELECT "id",   -- 序号
                               user_id, -- 用户ID
                               item_id, -- 商品ID
                               case when behavior_type = '1' then '点击'
                                    when behavior_type = '2' then '收藏'
                                    when behavior_type = '3' then '加入购物车'
                                    when behavior_type = '4' then '购买'
                                end as behavior_type, -- 用户行为类型
                                longitude, -- 经度
                                latitude, -- 纬度
                                item_category, -- 商品类别ID
                                date_format(r_time, '%%Y-%%m-%%d %%H:%%m:%%s') as 'time' -- 注册时间
                        from sale_info
                        %s""" % where)

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "销售数据恢复查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 销售数据新增/修改
@app.route('/api/sale/add', methods=['POST'])
def sale_add():
    try:
        data_all = request.form
        _id = data_all.get("id")                   # 序号
        user_id = data_all.get("user_id")               # 用户ID
        behavior_type = data_all.get("behavior_type")   # 用户行为类型 取值为“1,2，3,4” 分别表示“点击、收藏、加入购物车、购买”
        item_id = data_all.get("item_id")               # 商品ID
        item_category = data_all.get("item_category")   # 商品类别ID
        longitude = data_all.get("longitude")           # 经度
        latitude = data_all.get("latitude")             # 纬度
        r_time = data_all.get("r_time")                 # 购买时间

        if _id:
            g.cursor.execute("""update sale_info 
                                set user_id = '%s',
                                    behavior_type = '%s',
                                    item_id = '%s',
                                    item_category = '%s',
                                    longitude = '%s',
                                    latitude = '%s',
                                    r_time = '%s'
                                where id = '%s'""" % (user_id, behavior_type, item_id,
                                                      item_category, longitude, latitude,
                                                      r_time, _id))
        else:
            g.cursor.execute("""insert into sale_info(user_id, behavior_type, item_id,
                                                      item_category, longitude, latitude,
                                                      r_time)
                                values('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (user_id, behavior_type, item_id,
                                                                                       item_category, longitude, latitude,
                                                                                       r_time))

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "操作成功"
        }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 删除销售信息
@app.route('/api/sale/delete', methods=['POST'])
def sale_delete():
    try:
        data_all = request.form
        ids = data_all.get("id").split(',')  # 序号 ,连接 如：1,2,3
        for i in ids:
            g.cursor.execute("""update sale_info set state = '0' where id = '%s'""" % i)
        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "删除用户成功"
        }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 商品下单走势图
@app.route('/api/sale/analysis', methods=['POST'])
def sale_analysis():
    try:
        data_all = request.form
        behavior_type = data_all.get("behavior_type")   # 用户行为类型 取值为“1,2，3,4” 分别表示“点击、收藏、加入购物车、购买”
        item_id = data_all.get("item_id")               # 商品ID
        item_category = data_all.get("item_category")   # 商品类别ID
        start_time = data_all.get("start_time")         # 起始时间
        end_time = data_all.get("end_time")             # 结束时间

        where = """where state = '1' """

        if behavior_type:
            where = where + """ and behavior_type = '%s'""" % behavior_type
        if item_id:
            where = where + """ and item_id like '%%%s%%'""" % item_id
        if item_category:
            where = where + """ and item_category like '%%%s%%'""" % item_category
        if start_time:
            where = where + """ and date_format(r_time, '%%Y') >= '%s'""" % start_time
        if end_time:
            where = where + """ and date_format(r_time, '%%Y') < '%s'""" % end_time

        g.cursor.execute("""select date_format(r_time,'%%Y-%%m-%%d') as name, count(1) as VALUE
                            from sale_info where state = '1' and behavior_type = '4'
                            GROUP BY date_format(r_time,'%%Y-%%m-%%d') order by date_format(r_time,'%%Y-%%m-%%d')""" % where)

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "商品下单走势图",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)

# 销售数据下载
@app.route('/api/sale/download', methods=['POST'])
def sale_download():
    try:
        data_all = request.form
        ids = data_all.get("id") # 序号 实例：1,2,3
        sql = """
                SELECT "id",   -- 序号
                        user_id, -- 用户ID
                        item_id, -- 商品ID
                        case when behavior_type = '1' then '点击'
                            when behavior_type = '2' then '收藏'
                            when behavior_type = '3' then '加入购物车'
                            when behavior_type = '4' then '购买'
                        end as behavior_type, -- 用户行为类型
                        longitude, -- 经度
                        latitude, -- 纬度
                        item_category, -- 商品类别ID
                        date_format(r_time, '%%Y-%%m-%%d %%H:%%m:%%s') as 'time' -- 注册时间
                from sale_info where id in (%s)
        """ % ids
        g.cursor.execute(sql)
        out = g.cursor.fetchall()

        _path = "./bak.csv"
        # 创建文件对象
        f = open(_path,'wb')
        # 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f)
        # 构建列表头
        csv_writer.writerow(["序号","用户ID","商品ID","用户行为类型", "经度", "纬度", "商品类别ID", "注册时间"])
        # 将数据结果存储到CSV文件
        for i in out:
            csv_writer.writerow([i["id"], i["user_id"], i["item_id"], i["behavior_type"], i["longitude"],
                                 i["latitude"], i["item_category"], i["time"]])
        response = make_response(send_file(_path))
        response.headers["Content-Disposition"] = "attachment; filename=%s;" % 'bak.csv'
        
    except Exception as e:
        g.res = {
            "code":"500",
            "success": False,
            "msg": "销售数据下载失败"
        }
        return response
