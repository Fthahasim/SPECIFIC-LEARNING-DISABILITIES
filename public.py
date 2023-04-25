from flask import *
from database import *

public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template('index.html')

@public.route('/login',methods=['get','post'])
def login():
	if "login" in request.form:
		print("$$$$$$$$$$$$$$$$$$$")
		uname=request.form['un']
		pwd=request.form['pa']

		q="select * from login where username='%s' and password='%s'"%(uname,pwd)
		print(q)
		res=select(q)
		print(res)
		if res:
			session['lid']=res[0]['login_id']
			if res[0]['usertype']=="admin":
				flash("login successfully")
				return redirect(url_for('admin.adminhome'))

			elif res[0]['usertype']=="student":
				q1="select * from student where login_id='%s'"%(session['lid'])
				res1=select(q1)
				session['student_id']=res1[0]['student_id']
				flash("login successfully")
				return redirect(url_for('student.studenthome'))
			elif res[0]['usertype']=="teacher":
				q2="select * from teacher where login_id='%s'"%(session['lid'])
				res2=select(q2)
				session['teach_id']=res2[0]['teacher_id']
				flash("login successfully")
				return redirect(url_for('teacher.teacher_home'))
		
		else:
			flash("invaild username and password")
	return render_template('login.html')



@public.route('/studentregister',methods=['get','post'])
def studentregister():
	data={}
	if "register" in request.form:
	
		uname=request.form['un']
		pwd=request.form['pa']
		a=request.form['a']
		b=request.form['b']
		c=request.form['c']
		d=request.form['d']
		e=request.form['e']
		ff=request.form['f']
		# ff=request.form.getlist('f')
		# print(type(ff))
		# ff.remove('(')
		# print(ff)
		ql="insert into login values(null,'%s','%s','student')"%(uname,pwd)
		rl=insert(ql)
		print(ql)
		qs="insert into student values(null,'%s','%s','%s','%s','%s','%s','%s')"%(rl,a,b,e,c,d,ff)
		insert(qs)
		print(qs)
		flash("register successfully")
		return redirect(url_for('public.login'))
	
		
	return render_template('studentregister.html',data=data)