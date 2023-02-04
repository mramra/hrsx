# Copyright (c) 2023, hr and contributors
# For license information, please see license.txt
from datetime import datetime, timedelta,time

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, time_diff_in_hours, get_time


class Attendance(Document):
	start_time = frappe.db.sql(""" select value from `tabSingles` where doctype = 'Attendance Settings' AND field='start_time' """,as_dict=1)[0]['value']
	end_time = frappe.db.sql(""" select value from `tabSingles` where doctype = 'Attendance Settings' AND field='end_time' """,as_dict=1)[0]['value']
	working_hours_threshold_for_absent = frappe.db.sql(""" select value from `tabSingles` where doctype = 'Attendance Settings' AND field='working_hours_threshold_for_absent' """,as_dict=1)[0]['value']
	late_entry_grace_period = frappe.db.sql(""" select value from `tabSingles` where doctype = 'Attendance Settings' AND field='late_entry_grace_period' """,as_dict=1)[0]['value']
	early_exit_grace_period = frappe.db.sql(""" select value from `tabSingles` where doctype = 'Attendance Settings' AND field='early_exit_grace_period' """,as_dict=1)[0]['value']

	def validate(self):
		# Work Hours = Check Out - Check In
		self.add_value_Work_Hours()
		# Late Hours =  diff between (Check In , Start Time) and (Check Out , End Time )
		self.add_value_Late_Hours()

	def add_value_Work_Hours(self):
		x=timedelta(minutes=float(self.late_entry_grace_period))

		y=get_time(self.check_in)
		#start = datetime.strptime(x, "%H:%M:%S")
		#end = datetime.strptime(y, "%H:%M:%S")
		#z=x+y
		frappe.msgprint(str(x))

		#	self.work_hours = time_diff_in_hours(self.check_out, self.check_in)
	def add_value_Late_Hours(self):

		self.late_hours=time_diff_in_hours(self.check_out ,self.check_in)

