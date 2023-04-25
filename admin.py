from flask import *
from database import *
import uuid

admin=Blueprint('admin',__name__)

@admin.route('adminhome')
def adminhome():
	return render_template('adminhome.html')



@admin.route('admin_view_student',methods=['get','post'])
def admin_view_student():
	data={}
	q="select * from student"
	res=select(q)
	if res:
		data['prin']=res
		print(res)
	return render_template('admin_view_student.html',data=data)

@admin.route('adminviewexamattend',methods=['get','post'])
def adminviewexamattend():
	data={}
	id=request.args['id']


	q="select * from attend inner join question using(question_id) where student_id='%s'"%(id)
	res=select(q)
	if res:
		data['fee']=res
		print(res)

	return render_template('adminviewexamattend.html',data=data)


# @admin.route('admin_add_question',methods=['get','post'])
# def admin_add_question():
# 	data={}
# 	if 'manage' in request.form:
# 		cs=request.form['cs']
# 		q="insert into question values(NULL,'%s',curdate())"%(cs)
# 		insert(q)
# 		flash("Added Successfully...!")
# 		return redirect(url_for('admin.admin_add_question'))

# 	q="select * from question"
# 	res=select(q)
# 	if res:
# 		data['fee']=res
# 		print(res)

# 	if 'action' in request.args:
# 		action=request.args['action']
# 		id=request.args['id']
# 	else:
# 		action=None

# 	if action=='delete':
# 		q="delete from question where question_id='%s'"%(id)
# 		delete(q)
# 		flash("deleted.....!")
# 		return redirect(url_for('admin.admin_add_course'))

# 	if action=='update':
# 		q="select * from question where question_id='%s'"%(id)
# 		data['dir']=select(q)

# 	if 'update' in request.form:
# 		cs=request.form['cs']
# 		q="update question set question='%s' where question_id='%s'"%(cs,id)
# 		update(q)
# 		flash("updated")
# 		return redirect(url_for('admin.admin_add_course'))
# 	return render_template('admin_add_question.html',data=data)


# @admin.route('/admin_addop',methods=['get','post'])
# def admin_addop():
# 	data={}
# 	q="select * from question"	
# 	res=select(q)
# 	l=len(res)
# 	if int(l)>=5:
# 		data["filled"]="hello"
# 	if 'submit' in request.form:
# 		quest=request.form['quest']
		
# 		q="insert into question values(NULL,'%s')"%(quest)
# 		insert(q)
# 		return redirect(url_for('admin.admin_addop'))
# 	q="select * from question"
# 	res=select(q)
# 	data['quest']=res
# 	if 'action' in request.args:
# 		action=request.args['action']
# 		qid=request.args['qid']
# 		quest=request.args['quest']
# 	else:
# 		action=None
# 	if action=='delete':
# 		q="delete from question where question_id='%s'"%(qid)
# 		delete(q)
# 		q="delete from answer where question_id='%s'"%(qid)
# 		delete(q)
# 		return redirect(url_for('admin.admin_addop'))
	# return render_template('admin_addop.html',data=data)



# @admin.route('/admin_addop',methods=['get','post'])
# def admin_addop():
	

	# quest=request.args['quest']
	# qid=request.args['qid']
	# if 'submit' in request.form:
	# 	option=request.form['option']
	# 	mark=request.form['mark'] 
	# 	q="insert into answer values(NULL,'%s','%s','%s')"%(qid,option,mark)
	# 	insert(q)
	# 	return redirect(url_for('admin.admin_addop',quest=quest,qid=qid))
	# q="select * from answer where question_id='%s'"%(qid)
	# res=select(q)
	# data['option']=res
	# l=[1,2,3,4,5]
	# mark=[]
	# if res:
	# 	for  i in res:
	# 		mark=mark+[i['mark']]
	# print(mark)
	# for i in mark:
	# 	i=int(i)
	# 	if i in l:
	# 		l.remove(i)
	# data['l']=l
	# print(l)
	# if 'action' in request.args:
	# 	oid=request.args['oid']
	# 	q="delete from answer where answer_id='%s'"%(oid)
	# 	delete(q)
	# 	return redirect(url_for('admin.admin_addop',quest=quest,qid=qid))
	# return render_template('admin_addop.html',quest=quest,qid=qid,data=data)
	# return render_template('admin_addop.html')

@admin.route('/admin_addop',methods=['get','post'])
def admin_addop():
	data={}
	
	if 'submit' in request.form:
		noofoption=request.form['noofoption']
		answersel=request.form['answersel']
		quest=request.form['quest']
		testtype=request.form['testtype']
		roundtype=request.form['roundtype']
		tn=request.form['tn']
		print(noofoption,answersel,quest,tn)
		print('hiiiisssssss')
		image=request.files['image']

		
		if image.filename!="":
			paths="static/"+str(uuid.uuid4())+image.filename
			image.save(paths)
			tt="image"
		else:
			paths="NA"
			tt="text"
		print("///////////////",image)
		q="insert into question values(null,'%s','%s','%s','%s','%s',curdate(),'%s','pending')" %(quest,paths,testtype,roundtype,tn,tt)
		qid=insert(q)
		j=1
		
		# if request.files:
		# 	print('hiiiisssssss')

			# img1=request.files['img1']
			
		for i in range(0,int(noofoption)):
			ss=request.files['img'+str(j)]
			# print("deg",ss.filename)
			if ss.filename=="":
				# print("deg",ss.filename)
				path=request.form['text'+str(j)]
				typesss="text"
			else:
				print("Haii")
				val=request.files['img'+str(j)]
				path="static/uploads/"+str(uuid.uuid4())+".jpg"
				val.save(path)
				typesss="image"
			
			if int(j)==int(answersel):
				status="Yes"
			else:
				status="No"
			q="insert into answer values(null,'%s','%s','%s','%s')" %(qid,path,status,typesss)
			print(q)
			insert(q)
			j=j+1
		# 	else:
		# 		for i in range(0,int(noofoption)):
		# 			val=request.form['text'+str(j)]
		# 			if int(j)==int(answersel):
		# 				status="Yes"
		# 			else:
		# 				status="No"
		# 			q="insert into answer values(null,'%s','%s','%s','text')" %(qid,val,status)
		# 			insert(q)
		# 			j=j+1


		# else:
		# 	print('hiiiiii')
		# 	q="insert into question values(null,'%s','NA','%s','%s','%s',curdate())" %(quest,testtype,roundtype,tn)
		# 	qid=insert(q)
		# 	j=1
		# 	for i in range(0,int(noofoption)):
		# 		val=request.form['text'+str(j)]
		# 		if int(j)==int(answersel):
		# 			status="Yes"
		# 		else:
		# 			status="No"
		# 		q="insert into answer values(null,'%s','%s','%s')" %(qid,val,status)
		# 		insert(q)
		# 		j=j+1

		


	# v="select *,concat(First_Name,Last_Name) as Name from exam INNER JOIN subject USING(Subject_id)INNER JOIN teacher using(Teacher_id) where Exam_id='%s' and exam.Subject_id='%s'"%(ide,ids)
	# q=select(v)
	# data['Viewsub']=q

	return render_template("admin_addop.html",data=data)










@admin.route('adminviewanswer',methods=['get','post'])
def adminviewanswer():
	data={}
	id=request.args['id']


	q="select * from answer where question_id='%s'"%(id)
	res=select(q)
	if res:
		data['fee']=res
		print(res)

	return render_template('adminviewanswer.html',data=data)

@admin.route('/admin_manage_teacher',methods=['get','post'])
def admin_manage_teacher():
	data={}

	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		username=request.form['username']
		password=request.form['password']

		q="INSERT INTO `login` VALUES(NULL,'%s','%s','teacher')"%(username,password)
		res=insert(q)
		qr="INSERT INTO `teacher` VALUES(NULL,'%s','%s','%s','%s','%s','%s')"%(res,fname,lname,place,phone,email)
		insert(qr)
		flash('sucessfully added')


	if 'action' in request.args:
		action=request.args['action']
		log_id=request.args['log_id']
		teach_id=request.args['teach_id']
	else:
		action=None

	if action=='remove':
		q="DELETE FROM `teacher` WHERE `teacher_id`='%s'"%(teach_id)
		delete(q)
		q="DELETE FROM `login` WHERE `login_id`='%s'"%(log_id)
		delete(q)
		flash('"Are you sure to delete?"')
		return redirect(url_for('admin.admin_manage_teacher'))

	q="SELECT * FROM `teacher`"
	res=select(q)
	data['view']=res
	return render_template('admin_manage_teacher.html',data=data)
