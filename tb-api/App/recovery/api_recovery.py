# -*- encoding: utf-8 -*-
'''
    Create on
    @author:
    @summary: 数据恢复
'''
import json
import sys
from flask import Blueprint, g, request, Response
reload(sys)
sys.setdefaultencoding("utf8")

app = Blueprint(__name__ + "_app", __name__)


# 用户恢复
@app.route('/api/recovery/user', methods=['GET'])
def recovery_user():
    try:

        where = """where state = '0' """

        g.cursor.execute("""
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
                        %s""" % where)

        g.conn.commit()
        g.res = {
            "code":"200",
            "success": True,
            "msg": "用户恢复数据查询成功",
            "data": g.cursor.fetchall()
        }
    except Exception as e:
        print e
    return json.dumps(g.res, ensure_ascii=False)


# 销售数据恢复
@app.route('/api/recovery/sale', methods=['GET'])
def recovery_sale():
    try:

        where = """where state = '0' """

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
        print e
    return json.dumps(g.res, ensure_ascii=False)