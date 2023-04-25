from flask import *
from database import *
import uuid

teacher=Blueprint('teacher',__name__)

@teacher.route('/teacher_home')
def teacher_home():
	
	return render_template('teacher_home.html')

# @teacher.route('/admin_addop',methods=['get','post'])
# def admin_addop():
# 	data={}
	
# 	if 'submit' in request.form:
# 		noofoption=request.form['noofoption']
# 		answersel=request.form['answersel']
# 		quest=request.form['quest']
# 		testtype=request.form['testtype']
# 		roundtype=request.form['roundtype']
# 		tn=request.form['tn']
# 		print(noofoption,answersel,quest,tn)
# 		print('hiiiisssssss')
# 		img=request.files['img']
# 		if img.filename=="":
# 			paths="static/"+str(uuid.uuid4())+img.filename
# 			img.save(paths)
# 			tt="image"
# 		else:
# 			paths="NA"
# 			tt="text"
# 		q="insert into question values(null,'%s',','%s','%s','%s','%s','%s',curdate(),'%s')" %(session['teach_id'],quest,paths,testtype,roundtype,tn,tt)
# 		qid=insert(q)
# 		j=1
		
# 		# if request.files:
# 		# 	print('hiiiisssssss')

# 			# img1=request.files['img1']
			
# 		for i in range(0,int(noofoption)):
# 			ss=request.files['img'+str(j)]
# 			# print("deg",ss.filename)
# 			if ss.filename=="":
# 				# print("deg",ss.filename)
# 				path=request.form['text'+str(j)]
# 				typesss="text"
# 			else:
# 				print("Haii")
# 				val=request.files['img'+str(j)]
# 				path="static/uploads/"+str(uuid.uuid4())+".jpg"
# 				val.save(path)
# 				typesss="image"
			
# 			if int(j)==int(answersel):
# 				status="Yes"
# 			else:
# 				status="No"
# 			q="insert into answer values(null,'%s','%s','%s','%s')" %(qid,path,status,typesss)
# 			print(q)
# 			insert(q)
# 			j=j+1
# 		# 	else:
# 		# 		for i in range(0,int(noofoption)):
# 		# 			val=request.form['text'+str(j)]
# 		# 			if int(j)==int(answersel):
# 		# 				status="Yes"
# 		# 			else:
# 		# 				status="No"
# 		# 			q="insert into answer values(null,'%s','%s','%s','text')" %(qid,val,status)
# 		# 			insert(q)
# 		# 			j=j+1


# 		# else:
# 		# 	print('hiiiiii')
# 		# 	q="insert into question values(null,'%s','NA','%s','%s','%s',curdate())" %(quest,testtype,roundtype,tn)
# 		# 	qid=insert(q)
# 		# 	j=1
# 		# 	for i in range(0,int(noofoption)):
# 		# 		val=request.form['text'+str(j)]
# 		# 		if int(j)==int(answersel):
# 		# 			status="Yes"
# 		# 		else:
# 		# 			status="No"
# 		# 		q="insert into answer values(null,'%s','%s','%s')" %(qid,val,status)
# 		# 		insert(q)
# 		# 		j=j+1

		


# 	# v="select *,concat(First_Name,Last_Name) as Name from exam INNER JOIN subject USING(Subject_id)INNER JOIN teacher using(Teacher_id) where Exam_id='%s' and exam.Subject_id='%s'"%(ide,ids)
# 	# q=select(v)
# 	# data['Viewsub']=q

# 	return render_template("admin_addop.html",data=data)

