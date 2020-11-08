# -*- encoding: utf-8 -*-

import pymysql
import config
from flask import Flask, g

app = Flask(__name__)

'''加载路由列表，进行接口预处理，导入相关文件'''

from App.user.api_login_user import app as api_login_user
app.register_blueprint(api_login_user)

from App.user.api_user import app as api_user
app.register_blueprint(api_user)

from App.analysis.api_analysis import app as api_analysis
app.register_blueprint(api_analysis)

from App.recovery.api_recovery import app as api_recovery
app.register_blueprint(api_recovery)

from App.sale.api_sale import app as api_sale
app.register_blueprint(api_recovery)

from App.behaviors.api_behaviors import app as api_sale
app.register_blueprint(api_sale)

@app.before_request
def setupdb():
    '''每次请求都经过数据库进行数据预处理'''
    g.conn = pymysql.connect(host='39.96.57.39', port=3306, user='root', password='123456', db='behavior_data', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    g.cursor = g.conn.cursor()
    g.res = dict(status='error',data='服务接口异常')


@app.teardown_request
def unsetdb(exception=None):
    '''每次请求都经过数据库进行关闭'''
    if g.cursor:
       g.cursor.close()
       g.cursor = None
    if g.conn:
        g.conn.close()
        g.conn = None
    if g.res:
        g.res = None


@app.errorhandler(404)
def err_notfound(e):
    return '{"error":true, "msg":"请求的资源不存在"}', 404


@app.errorhandler(500)
def err_exception(e):
    return '{"error":true, "msg":"服务器内部出现异常"}', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9234, debug=True)
