#! /usr/bin/env python
# -*- coding:utf-8 -*-

from flask import *
import os,sys
import logging
from flask_bootstrap import *
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
import json
from flask_sqlalchemy import SQLAlchemy

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YZTC'
log = logging.getLogger(__name__)
mysql_host = os.environ.get("mysql_host",'10.3.15.207:3306')
mysql_db = os.environ.get("mysql_db",'yonyou_cloud_test')
mysql_user = os.environ.get("mysql_user",'root_admin')
mysql_password = os.environ.get("mysql_password",'root_admin_ufsoft*123')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://'+mysql_user+':'+mysql_password+'@'+mysql_host+'/'+mysql_db
    # 'mysql://root:Ufsoft*123@20.12.17.153/devops_db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    text = TextAreaField('notice')
    chicken_soup = StringField('chicken_soup')
    title = StringField('title')
    # plus = SubmitField(label='pluss')
    # dec = SubmitField('--')
    submit = SubmitField(u'提交')

class FileForm(FlaskForm):
    config_file  = FileField('file',validators=[DataRequired()])
    submit = SubmitField(u'提交1')

# class Role(db.Model):
#     __tablename__ = 'test'
#     id = db.Column(db.Integer,primary_key=True)
#     msg = db.Column(db.String(64))
#     name = db.Column(db.String(64))
#
#     def __repr__(self):
#         return '<Role %r>' % self.name

class Updates(db.Model):
    __tablename__ = 'fe_update_msg'
    id = db.Column(db.Integer,primary_key=True)
    msg = db.Column(db.String(1024))
    notice = db.Column(db.String(1024))
    chicken_soup = db.Column(db.String(256))
    title = db.Column(db.String(64))
    def __repr__(self):
        return '<Role %r>' % self.title

@app.route('/')
def index():
    log.info('index')

    return redirect('fe-update-msg/form')

@app.route('/configfile',methods=['get',"post"])
def configfile():
    form = FileForm()
    if form.is_submitted():
        print form.config_file.data
        #form.config_file.data.save('D:/tt.txt')
        flash('上传成功','ok')
    return render_template('configfile.html',form=form,name='dd')

# @app.route('/static')
# def file():
#     return send_file('static/pic.jpg')

@app.route('/fe-update-msg/getconfig')
def getconfig():
    config = Updates.query.get_or_404(1)
    result = {
        'notice':json.loads(config.notice),
        "sentence": config.chicken_soup,
        'title':config.title
    }
    result = json.dumps(result,ensure_ascii=False)
    log.info('get cofig:'+ result)
    return result
  #  return json.dumps(config.msg,ensure_ascii=False)
    # return jsonify(json.dumps(config.msg,ensure_ascii=False))


@app.route('/fe-update-msg/form',methods=['GET','POST'])
def form():
    form = NameForm()
    name = None
    if form.is_submitted():
        text = form.text.data
        soup = form.chicken_soup.data
        title = form.title.data
        print (text == '')
        print (soup == '')
        print (title == '')
        name= updates(text, soup, title)
        #return redirect(url_for('wtf'))

    return render_template('form.html',form = form,name =name)


def updates(details, chicken_soup, title):
    update = Updates.query.get_or_404(1)
    if chicken_soup != '':
        update.chicken_soup = chicken_soup
    if title != '':
        update.title = title
    details_list = ['']
    if details != '':
        details_list = details.replace('\r','').replace('\n','').split(u"；")
        print type(details_list)
        update.notice = json.dumps(details_list, ensure_ascii=False)
    # details_list = details.split(u"；")
    dic = {
        'notice': details_list,
        'sentence': chicken_soup,
        'title': title
    }
    msg = json.dumps(dic,ensure_ascii=False)

    update.msg = msg

    # with codecs.open('D:/pythons/form/static/test.txt','w+',encoding='utf-8') as text:
    #     text.write(jj)
    #     res = 'resss'
    #     #res=text.read()
    #     log.info('res'+res)
    return msg

if __name__ == '__main__':
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s - [%(asctime)s] - %(message)s'))
    texthandler = logging.FileHandler("./pylog.txt")
    texthandler.setLevel(logging.INFO)
    log.addHandler(handler)
    log.addHandler(texthandler)
    log.setLevel(logging.INFO)
    db.create_all()
    app.run(host='0.0.0.0',port='80')
