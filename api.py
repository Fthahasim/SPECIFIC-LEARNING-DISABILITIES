from flask import *
from numpy import diff
from database import *

import demjson
import uuid


api=Blueprint('api',__name__)

@api.route('/login',methods=['get','post'])
def login():
	data={}
	
	username = request.args['username']
	password = request.args['password']
	q="SELECT * from login where username='%s' and password='%s'" % (username,password)
	res = select(q)
	if res :
		data['status']  = 'success'
		data['data'] = res
		data['method']='login'
	else:
		data['status']	= 'failed'
		data['method']='login'
	return  str(data)



@api.route('/Student_registration',methods=['get','post'])
def Student_registration():

    data={}

    fname=request.args['fname']
    age=request.args['age']
    relationship=request.args['relationship']
    companion=request.args['companion']
    phone=request.args['phone']
    difficulties=request.args['difficulties']
    username=request.args['username']
    password=request.args['password']
    
    q="SELECT * FROM `login` WHERE `username`='%s'"%(username)
    res=select(q)
    if res:
        data['status']='duplicate'
    else:
        q="INSERT INTO `login` VALUES(NULL,'%s','%s','student')"%(username,password)
        ids=insert(q)
        q="INSERT INTO `student` VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s')"%(ids,fname,age,relationship,companion,phone,difficulties)
        id=insert(q)
        if id>0:
            data['status'] = 'success'
        else:
            data['status'] = 'failed'
    data['method'] = 'Student_registration'
    return str(data)



@api.route('/Student_view_exam',methods=['get','post'])
def Student_view_exam():
	data = {}

	
	q="SELECT * FROM `question` GROUP BY `testtype` "
	result=select(q)
	if result:
		data['status'] = 'success'
		data['data'] = result
		
	else:
		data['status'] = 'failed'
	data['method'] = 'Student_view_exam'
	return str(data)



@api.route('/Student_view_questions',methods=['get','post'])
def Student_view_questions():
	data = {}

	testtypes=request.args['testtypes']
	roundtypes=request.args['roundtypes']

	
	q="SELECT * FROM `question`  WHERE `testtype`='%s' AND `roundtype`='%s' ORDER BY RAND() limit 10"%(testtypes,roundtypes)
	result=select(q)
	if result:
		data['status'] = 'success'
		data['data'] = result
		
	else:
		data['status'] = 'failed'
	data['method'] = 'Student_view_questions'
	return str(data)

@api.route('/Student_view_questions_options',methods=['get','post'])
def Student_view_questions_options():
	data={}

	question_ids=request.args['question_ids']
	
	q="SELECT * FROM `answer` WHERE `question_id`='%s'"%(question_ids)
	print(q)
	res=select(q)
	data['status'] = 'success'
	data['data']=res
	
	data['method'] = 'Student_view_questions_options'
	return str(data)






@api.route('/Student_mark_option',methods=['get','post'])
def Student_mark_option():
	data = {}

	question_ids=request.args['question_ids']
	log_id=request.args['log_id']
	answer_ids=request.args['answer_ids']
	answer_statuss=request.args['answers']
	q="INSERT INTO `attend` VALUES(NULL,'%s','%s',(SELECT `student_id` FROM `student` WHERE `login_id`='%s'),'%s')"%(question_ids,answer_ids,log_id,answer_statuss)
	print(q)
	result=insert(q)
	if result:
		data['status'] = 'success'
	
		
	else:
		data['status'] = 'failed'
	data['method'] = 'Student_mark_option'
	return str(data)


@api.route('/get_questions', methods=['get', 'post'])
def get_questions():
	data = {}

	tt = request.args['tt']
	rr = request.args['rr']

	q = "SELECT * FROM `question`INNER JOIN `answer` USING(`question_id`) WHERE testtype = '%s' and roundtype='%s'" %(tt,rr)
	res = select(q)
	if res:
		data['data'] = res
		data['status'] = 'success'
	else:
		data['status'] = 'failed'
	data['method'] = 'get_questions'
	return str(data)


@api.route('/user_view_qstn', methods=['get', 'post'])
def user_view_qstn():
	data = {}

	tt = request.args['tt']
	rr = request.args['rr']
	lid = request.args['lid']

	q="SELECT * FROM `question` INNER JOIN `answer` USING(`question_id`) WHERE `question_id`  NOT IN(SELECT `question_id` FROM `attend` WHERE `student_id`=(SELECT `student_id` FROM `student` WHERE `login_id`='%s')) AND testtype = '%s' and roundtype='%s' ORDER BY RAND() LIMIT 1" %(lid,tt,rr)
	# q = "SELECT * FROM `question`INNER JOIN `answer` USING(`question_id`) WHERE testtype = '%s' and roundtype='%s'" %(tt,rr)
	print(q)
	res = select(q)
	if res:
		data['data'] = res
		data['status'] = 'success'
	else:
		data['status'] = 'Already Attend'
	data['method'] = 'user_view_qstn'
	return str(data)


@api.route('/user_view_options', methods=['get', 'post'])
def user_view_options():
	data = {}

	tt = request.args['tt']
	rr = request.args['rr']
	lid = request.args['lid']
	q_id = request.args['q_id']

	# $q1="SELECT * FROM `questions` INNER JOIN `qstnanswer` USING(`qstn_id`) WHERE `qstn_id`  NOT IN(SELECT `qstn_id` FROM `selected_answers` WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='$u_id')) AND `exam_id`='$ex_id'";

	q="SELECT * FROM `question` INNER JOIN `answer` USING(`question_id`) WHERE `question_id`  NOT IN(SELECT `question_id` FROM `attend` WHERE `student_id`=(SELECT `student_id` FROM `student` WHERE `login_id`='%s')) AND testtype = '%s' and roundtype='%s'" %(lid,tt,rr)
	# q = "SELECT * FROM `question`INNER JOIN `answer` USING(`question_id`) WHERE testtype = '%s' and roundtype='%s'" %(tt,rr)
	res = select(q)
	if res:
		q="SELECT COUNT(attend_id) as cids FROM `attend` INNER JOIN `question` USING (question_id) WHERE roundtype='%s' AND student_id=(SELECT `student_id` FROM `student` WHERE `login_id`='%s')" %(rr,lid)
		res6=select(q)
		print(res6[0]['cids'])
		if int(res6[0]['cids'])>15:
			data['status'] = 'Already Attend'
		else:
			q="SELECT * FROM `question` WHERE `question_id`='%s'" %(q_id)
			res1=select(q)
			data['data1']=res1
			if res1:
				q="SELECT * FROM `answer` WHERE `question_id`='%s'" %(q_id)
				res2=select(q)
				data['data2']=res2
			# data['data'] = res
				data['status'] = 'success'
			else:
				data['status']="failed"
	else:
		data['status'] = 'Already Attend'
	data['method'] = 'user_view_options'
	return str(data)



@api.route('/user_answer',methods=['get','post'])
def user_answer():
	data = {}
	tt = request.args['tt']
	rr = request.args['rr']
	if tt=="Dyslexia":
		ttt=1
	elif tt=="Dyscalculia":
		ttt=2
	elif tt=="Dysgraphia":
		ttt=3

	if rr=="Round1":
		rrr=1
	elif rr=="Round2":
		rrr=2

	
	q_id=request.args['q_id']
	qans_id=request.args['qans_id']
	mark=request.args['mark']
	timetaken=request.args['timetaken']

	if int(timetaken)>0  and int(timetaken)<=25:
		ttaken=20
	elif int(timetaken)>25  and int(timetaken)<=40:
		ttaken=35
	elif int(timetaken)>40  and int(timetaken)<=60:
		ttaken=55
	elif int(timetaken)>60  and int(timetaken)<=100:
		ttaken=60


	# timetaken=20

	# //////////////////////////////////////////////////////////////////////////
	import csv
	import os
	import pandas
	import numpy as np

	toappend=[]
	# //////////////////////////////////////////////////
	toappend.append(np.mean(ttt))
	toappend.append(np.mean(rrr))
	toappend.append(np.mean(1))
	toappend.append(np.mean(1))
	toappend.append(np.mean(int(q_id)))
	#toappend.append(np.mean(1))
	
	toappend.append(np.mean(int(qans_id)))
	toappend.append(np.mean(int(ttaken)))
	toappend.append(np.mean(int(mark)))

	# //////////////////////////////////////////////////
	lastsss=np.array([toappend])
	print(lastsss)
	# a = pandas.read_csv('C:/Users/DELL/OneDrive/Desktop/Disease/disease_detect/disease_detect/DyslexiaR1dataset.csv')
	a = pandas.read_csv('C:/Disease/disease_detect/disease_detect/DyslexiaR1dataset.csv')

	
	attributes = a.values[:, 0:8]
	label = a.values[:, 8]
	# labels = a.values[:, 8]

	# print(attributes)
	# print(label)

	from sklearn.model_selection import train_test_split

	X_train, X_test, y_train, y_test = train_test_split(attributes, label, test_size=0.1, random_state=42)
	# X_trains, X_test, y_trains, y_test = train_test_split(attributes, labels, test_size=0.1, random_state=42)
	print(X_test)
	from sklearn.tree import DecisionTreeClassifier

	a = DecisionTreeClassifier()
	# a1 = DecisionTreeClassifier()

	a.fit(X_train, y_train)
	# a1.fit(X_trains, y_trains)
	predictedresult = a.predict(lastsss)
	# predictedresult1 = a1.predict(lastsss)
	print(predictedresult)
	# print(predictedresult1)
	actualresult = y_test
	testdata = X_test

	l = len(testdata)

	from sklearn.metrics import accuracy_score

	# sc = accuracy_score(actualresult, predictedresult)
	# print(sc)
	# from sklearn.metrics import confusion_matrix
	# cc=confusion_matrix(actualresult, predictedresult)
	# print(cc)

# print(sc)


	# //////////////////////////////////////////////////////////////////////////

	lid=request.args['lid']

	q="INSERT INTO `attend` VALUES(NULL,'%s','%s',(SELECT `student_id` FROM `student` WHERE `login_id`='%s'),'%s','%s','%s')"%(q_id,qans_id,lid,mark,ttaken,predictedresult[0])
	result=insert(q)
	if result:
		data['status'] = 'success'
	
		
	else:
		data['status'] = 'failed'
	data['method'] = 'user_answer'
	return str(data)

@api.route('/Checkexamdetails',methods=['get','post'])
def Checkexamdetails():		
	data = {}

	lid=request.args['lid']
	ttt=request.args['ttt']


	
	q="select * from attend inner join question using(question_id) where testtype='%s' and roundtype='Round1' and student_id=(SELECT `student_id` FROM `student` WHERE `login_id`='%s')" %(ttt,lid)
	print(q)
	result=select(q)

	if result:
		q="select * from attend inner join question using(question_id) where testtype='%s' and roundtype='Round2' and student_id=(SELECT `student_id` FROM `student` WHERE `login_id`='%s')" %(ttt,lid)
		print(q)
		result1=select(q)
		if result1:

			data['status'] = 'success3'
			data['mark'] = result1[0]['mark']
			data['result'] = result1[0]['result']
		else:
			data['status']='success2'
			data['mark'] = result[0]['mark']
			data['result'] = result[0]['result']
		data['data'] = result

	else:
		data['mark'] = 0
		data['status'] = 'success1'
		data['result']=0
	data['method'] = 'Checkexamdetails'
	return str(data)


@api.route('/Student_view_predict',methods=['get','post'])
def Student_view_predict():
	data = {}

	lid=request.args['lid']
	tt = request.args['tt']
	rr = request.args['rr']

	
	q="SELECT COUNT(result) as ccc,result FROM attend INNER JOIN question USING(question_id) WHERE student_id=(SELECT `student_id` FROM `student` WHERE `login_id`='%s') AND `roundtype`='%s' AND `testtype`='%s' GROUP BY result ORDER BY COUNT(result) DESC"%(lid,rr,tt)
	result=select(q)
	print(result)
	if result:
		data['status'] = 'success'
		print(result[0]['result'])
		if int(result[0]['result']) < 3:
			data['out'] = "Disease Detected"
		elif int(result[0]['result']) >= 3:
			data['out'] = "No Disease Detected"
		
	else:
		data['status'] = 'failed'
	data['method'] = 'Student_view_predict'
	return str(data)




# @api.route('/user_book_vehicle',methods=['get','post'])
# def user_book_vehicle():

# 	data={}

# 	fdate=request.args['fdate']
# 	ftime=request.args['ftime']
# 	tdate=request.args['tdate']
# 	ttime=request.args['ttime']
# 	login_id=request.args['login_id']
# 	book_for_id=request.args['book_for_id']
# 	book_for_type=request.args['book_for_type']	
# 	print(book_for_type)
# 	qnty=request.args['qnty']

# 	if book_for_type=="item":
# 		q="INSERT INTO `booking` VALUES(NULL,'%s','%s',(SELECT `user_id` FROM `users` WHERE `login_id`='%s'),'%s','%s','%s','%s','%s','NA','Pending',NOW(),'NA')"%(book_for_id,book_for_type,login_id,fdate,ftime,tdate,ttime,qnty)
# 		print(q)
# 		id=insert(q)
# 		if id>0:
# 			data['status'] = 'success'
# 		else:
# 			data['status'] = 'failed'
# 	elif book_for_type=="vehicle":
# 		q="INSERT INTO `booking` VALUES(NULL,'%s','%s',(SELECT `user_id` FROM `users` WHERE `login_id`='%s'),'%s','%s','%s','%s','NA','NA','Pending',NOW(),'NA')"%(book_for_id,book_for_type,login_id,fdate,ftime,tdate,ttime)
# 		print(q)
# 		id=insert(q)
# 		if id>0:
# 			data['status'] = 'success'
# 		else:
# 			data['status'] = 'failed'
# 	data['method'] = 'user_book_vehicle'
# 	return str(data)


# @api.route('/user_view_bookings',methods=['get','post'])
# def user_view_bookings():
# 	data = {}

# 	login_id=request.args['login_id']

	
# 	q="SELECT * FROM `booking` INNER JOIN `vehicles` on vehicles.vehicle_id=booking.book_for_id  WHERE `booking`.`user_id`=(SELECT `user_id` FROM users WHERE `login_id`='%s') and booking.book_for_type='vehicle'"%(login_id)
# 	result=select(q)
# 	if result:
# 		data['status'] = 'success'
# 		data['data'] = result
		
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = 'user_view_bookings'
# 	return str(data)


# @api.route('/user_view_bookings_items',methods=['get','post'])
# def user_view_bookings_items():
# 	data = {}

# 	login_id=request.args['login_id']

	
# 	q="SELECT * FROM `booking` INNER JOIN `items` on items.item_id=booking.book_for_id  WHERE `booking`.`user_id`=(SELECT `user_id` FROM users WHERE `login_id`='%s') and booking.book_for_type='item'"%(login_id)
# 	result=select(q)
# 	if result:
# 		data['status'] = 'success'
# 		data['data'] = result
		
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = 'user_view_bookings_items'
# 	return str(data)


# @api.route('/user_view_vehicle_details',methods=['get','post'])
# def user_view_vehicle_details():
# 	data = {}

# 	vhid=request.args['vhid']

	
# 	q="SELECT * FROM `vehicles` WHERE `vehicle_id`='%s'"%(vhid)
# 	result=select(q)
# 	if result:
# 		data['status'] = 'success'
# 		data['data'] = result
		
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = 'user_view_vehicle_details'
# 	return str(data)




# @api.route('/user_payment',methods=['get','post'])
# def user_payment():
# 	data={}

# 	booking_id=request.args['booking_id']
# 	action=request.args['action']
# 	amount=request.args['amount']
	
	
# 	if action=="Advance":
# 		q="INSERT INTO `payment` VALUES(NULL,'%s','%s','%s',NOW())"%(action,booking_id,amount)
# 		print(q)
# 		insert(q)
# 		q="UPDATE `booking` SET `booking_status`='%s',balance_amount='%s' WHERE `booking_id`='%s'"%(action,amount,booking_id)
# 		print(q)
# 		update(q)
# 	else:
# 		q="UPDATE `booking` SET `booking_status`='returned',balance_amount='0' WHERE `booking_id`='%s'"%(booking_id)
# 		update(q)
# 		q="UPDATE `payment` SET `amount`=`amount`+'%s',`payment_type`='%s' WHERE `booking_id`='%s'"%(amount,action,booking_id)
# 		update(q)
	
# 	data['status'] = 'success'

# 	data['method'] = 'user_payment'
# 	return str(data)


# @api.route('/user_send_return_req',methods=['get','post'])
# def user_send_return_req():
# 	data={}

# 	booking_id=request.args['booking_id']
	
# 	q="UPDATE `booking` SET `booking_status`='Return Req',returned_date=curdate() WHERE `booking_id`='%s'"%(booking_id)
# 	id=insert(q)
# 	if id>0:
# 		data['status'] = 'success'
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = 'user_send_return_req'
# 	return str(data)



# @api.route('/user_send_feedback',methods=['get','post'])
# def user_send_feedback():

# 	data={}

# 	booking_id=request.args['booking_id']
# 	rating=request.args['rating']
# 	review=request.args['review']

# 	q="SELECT * FROM `feedback` WHERE `booking_id`='%s'"%(booking_id)
# 	res=select(q)
# 	if res:

# 		q="UPDATE `feedback` SET `rating`='%s',`description`='%s',`datetime`=NOW() WHERE `booking_id`='%s'"%(rating,review,booking_id)
# 		update(q)
# 		data['method'] = 'user_send_feedback'
# 		data['status'] = 'success'
# 	else:
# 		q="INSERT INTO `feedback` VALUES(NULL,'%s','%s','%s',NOW())"%(booking_id,rating,review)
# 		id=insert(q)
# 		if id:
# 			data['status'] = 'success'
# 			data['method'] = 'user_send_feedback'
# 		else:
# 			data['status'] = 'failed'
# 			data['method'] = 'user_send_feedback'
# 	return str(data)



# @api.route('/user_view_rated',methods=['get','post'])
# def user_view_rated():
# 	data = {}

# 	booking_id=request.args['booking_id']
	
# 	q="SELECT * FROM `feedback` WHERE `booking_id`='%s'"%(booking_id)
# 	print(q)
# 	result=select(q)
# 	if result:
# 		data['status'] = 'success'
# 		data['data'] = result[0]['rating']
# 		data['data1'] = result[0]['description']
		
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = 'user_view_rated'
# 	return str(data)




# @api.route('/view_item',methods=['get','post'])
# def view_item():
# 	data = {}

	
# 	q="SELECT * FROM `items` "
# 	result=select(q)
# 	if result:
# 		data['status'] = 'success'
# 		data['data'] = result
		
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = 'view_item'
# 	return str(data)

# @api.route('/srch_view_item',methods=['get','post'])
# def srch_view_item():
# 	data = {}

# 	srch="%"+request.args['srch']+"%"
# 	q="SELECT * FROM `items` WHERE  `item_name` LIKE '%s'"%(srch)
# 	result=select(q)
# 	if result:
# 		data['status'] = 'success'
# 		data['data'] = result
		
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = 'view_item'
# 	return str(data)



# @api.route('/View_app_rating',methods=['get','post'])
# def View_app_rating():
# 	data = {}

# 	loginid=request.args['loginid']
	
	
# 	q="SELECT * FROM `app_rating` WHERE `user_id`=(SELECT `user_id` FROM `users` WHERE `login_id`='%s')"%(loginid)
# 	print(q)
# 	result=select(q)
# 	if result:
# 		data['status'] = 'success'
# 		data['data'] = result[0]['rating']
# 		data['data1'] = result[0]['review']
		
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = 'View_app_rating'
# 	return str(data)





# @api.route('/App_rating',methods=['get','post'])
# def App_rating():

# 	data={}

# 	ratings=request.args['rating']
# 	review=request.args['review']
# 	loginid=request.args['loginid']

# 	q="SELECT * FROM `app_rating` WHERE `user_id`=(SELECT `user_id` FROM `users` WHERE `login_id`='%s')"%(loginid)
# 	res=select(q)
# 	if res:

# 		q="UPDATE `app_rating` SET `rating`='%s',`review`='%s',`date`=CURDATE() WHERE `user_id`=(SELECT `user_id` FROM `users` WHERE `login_id`='%s')"%(review,ratings,loginid)
# 		update(q)
# 		data['method'] = 'App_rating'
# 	else:
# 		q="INSERT INTO `app_rating` VALUES(NULL,(SELECT `user_id` FROM `users` WHERE `login_id`='%s'),'%s','%s',CURDATE())"%(loginid,ratings,review)
# 		print(q)
# 		id=insert(q)
# 		if id>0:
# 			data['status'] = 'success'
			
# 		else:
# 			data['status'] = 'failed'
# 		data['method'] = 'App_rating'
# 	return str(data)


# @api.route('/User_view_more_images',methods=['get','post'])
# def User_view_more_images():
# 	data = {}

# 	vehicle_ids=request.args['vehicle_ids']
# 	q="SELECT * FROM `images` WHERE `vehicle_id`='%s'"%(vehicle_ids)
# 	result=select(q)
# 	if result:
# 		data['status'] = 'success'
# 		data['data'] = result
		
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = 'User_view_more_images'
# 	return str(data)