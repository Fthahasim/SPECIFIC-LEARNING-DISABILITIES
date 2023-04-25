from flask import Flask
from public import public
from student import student
from admin import admin
from teacher import teacher
from api import api


app=Flask(__name__)

app.secret_key="abc"

app.register_blueprint(public)
app.register_blueprint(student,url_prefix='/student')
app.register_blueprint(api,url_prefix='/api')
app.register_blueprint(teacher,url_prefix='/teacher')
app.register_blueprint(admin,url_prefix='/admin')


app.run(debug=True,port=5526,host="0.0.0.0")
	# classincharge


