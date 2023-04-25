from flask import *
from database import *
import uuid

student=Blueprint('student',__name__)

@student.route('studenthome')
def studenthome():
	return render_template('studenthome.html')



