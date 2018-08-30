#! /usr/bin/env python
# -*- coding:utf-8 -*-

from flask import *
import os,sys
import logging
from flask_bootstrap import *
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
import codecs
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YZTC'
log = logging.getLogger(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://root:Ufsoft*123@172.20.17.4/devops_db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    num = 1
    text = TextAreaField('notice',validators=[DataRequired()])
    chicken_soup = StringField('chicken_soup',validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    names = FieldList(StringField(u'项目'),label='dd',min_entries=num)
    plus = SubmitField(label='pluss')
    dec = SubmitField('--')
    submit = SubmitField(u'提交')

class FileForm(FlaskForm):
    config_file  = FileField('file',validators=[DataRequired()])
    submit = SubmitField(u'提交1')

class Role(db.Model):

    __tablename__ = 'test'
    id = db.Column(db.Integer,primary_key=True)
    msg = db.Column(db.String(64))
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<Role %r>' % self.name


@app.route('/')
def index():
    log.info('ggg')
    Role.qurey.all()
    #return  redirect('static')
    return render_template('index.html',name='dd')

@app.route('/configfile',methods=['get',"post"])
def configfile():
    form = FileForm()
    if form.is_submitted():
        print form.config_file.data
        #form.config_file.data.save('D:/tt.txt')
        flash('上传成功','ok')
    return render_template('configfile.html',form=form,name='dd')

@app.route('/static')
def file():
    return send_file('static/pic.jpg')

@app.route('/watch')
def watchfile():
    return changefile(['qq','ww'],'soup','gongg')

@app.route('/form',methods=['GET','POST'])
def wtf():
    form = NameForm()
    name = None
    if form.is_submitted():
        text = form.text.data
        soup = form.chicken_soup.data
        title = form.title.data
        # sub = form.submit.label
        # print type(sub)
        # print sub
        name= changefile(text,soup,title)
    #     flash('meimei')
    #     flash('didi')
        #return redirect(url_for('wtf'))

    return render_template('form.html',form = form,name =name)


def changefile(details,chicken_soup,title):
    # print os.path.realpath('D:/pythons/form/static/test.txt')
    details_list = details.replace('\r','').replace('\n','').split(';')
    dic = {
        'notice': details_list,
        'sentence': chicken_soup,
        'title': title
    }
    jj = json.dumps(dic,ensure_ascii=False)

    with codecs.open('D:/pythons/form/static/test.txt','w+',encoding='utf-8') as text:
        text.write(jj)
        res = 'resss'
        #res=text.read()
        log.info('res'+res)
    return jj

if __name__ == '__main__':
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s - [%(asctime)s] - %(message)s'))
    texthandler = logging.FileHandler("./pylog.txt")
    texthandler.setLevel(logging.INFO)
    log.addHandler(handler)
    log.addHandler(texthandler)
    log.setLevel(logging.INFO)



    app.run(host='0.0.0.0',port='80')
