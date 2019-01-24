from flask import Flask, redirect, url_for, get_flashed_messages, send_from_directory, session
from flask import request,render_template

from form import LoginForm, UploadForm, RichTextForm
import os
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key="secret string"
app.config['MAX_CONTENT_LENGTH'] = 3*1024*1024  #这个是3M 的大小，直接在这儿配置真是厉害。
app.config['UPLOAD_PATH']= os.path.join(app.root_path,'uploads')  #设置文件上传到的位置。
ckeditor = CKEditor(app)   #这个是用来初始化的对吧。
db=SQLAlchemy(app)   #都需要这样来初始化它的啊
app.config['CKEDITOR_SERVE_LOCAL']= True  #配置ckeditor
app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('DATABASE_URL','sqlite:///'+os.path.join(app.root_path,'data.db'))
#os.path.join  这个是找到这个下面的路径，SQLite 数据库的数量在win下是3个，在linux下是4个


@app.route('/')
def hello_world():
    # print(name)
    name= request.args.get("name")
    print(name)
    if name is None:
        name =request.cookies.get('name',"Human")
    return 'Hello World!'+name

@app.route('/upload',methods=['POST','GET'])   #这个主要是做映射还有提示文件提交成功的。
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f=form.photo.data
        # filename = random_filename(f.filename)  #如果不能确定文件来源安全的话，就需要这样的来设置。
        filename = f.filename
        print(filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'],filename))     #这样就是直接的文件保存的东西了。
        session['filenames']=filename   #直接通过session来传递。
        return redirect(url_for('showImage'))
    return render_template("uploadTest.html",form=form)


@app.route('/uploads/<path:filename>')   #用来做简单映射的东西
def get_file(filename):  #第一次这样用，通过这个来显示，相当于static的访问。
    print(send_from_directory(app.config['UPLOAD_PATH'],filename))   #访问不了这个静态文件的路径的东西。
    return send_from_directory(app.config['UPLOAD_PATH'],filename)

@app.route('/showImage')   #用来做简单映射的东西
def showImage():  #第一次这样用，通过这个来显示，相当于static的访问。
    filename= session['filenames']
    print(filename)
    return render_template("show.html",filename=filename)

# @app.before_request
# def doBefore():
#     print("hello world")

# @app.route('/showImage',methods=['POST','GET'])   #这个主要是做映射还有提示文件提交成功的。
# def showImagae(filename):  #第一次这样用，通过这个来显示，相当于static的访问。
#     # print(name)
#     print(send_from_directory(app.config['UPLOAD_PATH'],filename))   #访问不了这个静态文件的路径的东西。
#     return send_from_directory(app.config['UPLOAD_PATH'],filename)




@app.route('/result',methods=['GET','POST'])   #解决表单反复提交的方法是Post/Redirect/Get
def result():    #提交前提示和提交后提示都有了，这下。
    form = LoginForm()
    username="none"
    if form .validate_on_submit():
        username = form.username.data
        print("username:",username)
        return redirect(url_for("test"))  #对的话就变成了重定向到新的地方去。
    else:
        print("数据验证失败")  #不对的话最后就执行这个回去，然后返回错误的信息。Get
    return render_template("watchlist.html",form=form)


@app.route('/test')
def test():
    movie={
        "name":"zhengyiming",
        "desc":"django!"
    }
    form = LoginForm()
    return render_template('watchlist.html',movie=movie,form=form)

# 渲染有富文本的那个页面
@app.route("/ckeditor")
def ckeditor():
    form =RichTextForm()
    return render_template('ckeditor.html',form=form)

@app.route("/myCkeditor" ,methods=['POST'])
def myCkeditor():
    form =RichTextForm()
    if form.validate_on_submit():
        result = form.body.data
        print(result)
        return render_template("ckeditorResult.html", result=result)
    return "failed"

if __name__ == '__main__':
    app.run()
