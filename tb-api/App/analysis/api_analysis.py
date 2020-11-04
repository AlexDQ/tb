# -*- encoding: utf-8 -*-
'''
    Create on
    @author:
    @summary: 统计
'''
import json
import sys
from flask import Blueprint, g, request, Response
reload(sys)
sys.setdefaultencoding("utf8")

app = Blueprint(__name__ + "_app", __name__)


# 全国消费用户位置分析
@app.route('/api/analysis/country', methods=['POST'])
def analysis_country():
    try:
        data_all = request.form
        start_time = data_all.get("start_time") # 起始时间
        end_time = data_all.get("end_time")     # 结束时间

        where = """where state = '1' """
        if start_time:
            where = where + """ and date_format(r_time, '%%Y') >= '%s'""" % start_time
        if end_time:
            where = where + """ and date_format(r_time, '%%Y') < '%s'""" % end_time

        g.cursor.execute("""select city as name,
                                   longitude, -- 经度
                                   latitude, -- 纬度
                                   count(1) as VALUE
                            from sale_info
                            %s
                            group by name order by VALUE desc;""" % where)

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "全国消费用户位置分析查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        print e
    return json.dumps(g.res, ensure_ascii=False)


# 每日PV访问量分析
@app.route('/api/analysis/pv', methods=['POST'])
def analysis_pv():
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
                            from sale_info
                            %s
                            group by date_format(r_time,'%%Y-%%m-%%d') order by VALUE desc;""" % where)

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "每日PV访问量分析查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        print e
    return json.dumps(g.res, ensure_ascii=False)


# 每日UV(客户总数)分析
@app.route('/api/analysis/uv', methods=['POST'])
def analysis_uv():
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

        g.cursor.execute("""select date1 as name, count(1) as VALUE
                            from (select distinct user_id, date_format(r_time,'%%Y-%%m-%%d') as date1 from sale_info %s) a
                            GROUP BY date1 order by date1""" % where)

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "每日UV(客户总数)分析查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        print e
    return json.dumps(g.res, ensure_ascii=False)


# 客户总数
@app.route('/api/analysis/total', methods=['POST'])
def analysis_total():
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

        g.cursor.execute("""select date_format(r_time,'%%Y-%%m-%%d') as name, count(distinct user_id) as VALUE
                            from sale_info
                            %s
                            group by date_format(r_time,'%%Y-%%m-%%d') order by r_time desc;""" % where)

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "客户总数查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        print e
    return json.dumps(g.res, ensure_ascii=False)


# 每日购物人数及占比进行分析
@app.route('/api/analysis/shop', methods=['POST'])
def analysis_shop():
    try:
        data_all = request.form
        start_time = data_all.get("start_time") # 起始时间
        end_time = data_all.get("end_time")     # 结束时间

        where = """where state = '1' and behavior_type = '4' """
        if start_time:
            where = where + """ and date_format(r_time, '%%Y') >= '%s'""" % start_time
        if end_time:
            where = where + """ and date_format(r_time, '%%Y') < '%s'""" % end_time

        g.cursor.execute("""select s1.date1,
                                s1.b_person,
                                s2.uv,
                                concat(round(s1.b_person/s2.uv)*100, '%') as persent
                            from (
                                select t1.date1, count(1) as b_person from (select distinct user_id, date_format(r_time,'%%Y-%%m-%%d') as date1 from sale_info %s) t1
                                group by t1.date1
                            ) as s1,
                            (
                                select t1.date1, count(1) as uv from (select distinct user_id, date_format(r_time,'%%Y-%%m-%%d') as date1 from sale_info %s) t1
                                group by t1.date1
                            ) as s2
                            where s1.date1 = s2.date1""" % (where, where))

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "每日购物人数及占比进行分析查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 购买行为习惯分析
@app.route('/api/analysis/xg', methods=['POST'])
def analysis_xg():
    try:
        data_all = request.form
        start_time = data_all.get("start_time") # 起始时间
        end_time = data_all.get("end_time")     # 结束时间

        where = """where state = '1' and behavior_type = '4' """
        if start_time:
            where = where + """ and date_format(r_time, '%%Y') >= '%s'""" % start_time
        if end_time:
            where = where + """ and date_format(r_time, '%%Y') < '%s'""" % end_time

        g.cursor.execute("""select case when behavior_type = '1' then '点击'
                                                    when behavior_type = '2' then '收藏'
                                                    when behavior_type = '3' then '加入购物车'
                                                    when behavior_type = '4' then '购买' end as name,
                                        count(1) as value
                            from sale_info
                            %s
                            group by name order by VALUE desc;""" % where)

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "购买行为习惯分析查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)


# 基于时间维度行为习惯分析
@app.route('/api/analysis/sj', methods=['POST'])
def analysis_sj():
    try:
        data_all = request.form
        start_time = data_all.get("start_time") # 起始时间
        end_time = data_all.get("end_time")     # 结束时间

        where = """where state = '1' and behavior_type = '4' """
        if start_time:
            where = where + """ and date_format(r_time, '%%Y') >= '%s'""" % start_time
        if end_time:
            where = where + """ and date_format(r_time, '%%Y') < '%s'""" % end_time

        g.cursor.execute("""select date_format(r_time,'%%Y-%%m-%%d') as t, 
                                   case when behavior_type = '1' then '点击'
                                               when behavior_type = '2' then '收藏'
                                               when behavior_type = '3' then '加入购物车'
                                               when behavior_type = '4' then '购买' end as name,
                                   count(1) as value
                            from sale_info
                            %s
                            group by name, t order by t;""" % where)

        g.res = {
            "code":"200",
            "success": True,
            "msg": "基于时间维度行为习惯分析查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        return json.dumps(g.res, ensure_ascii=False)