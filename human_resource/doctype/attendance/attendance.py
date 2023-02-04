# Copyright (c) 2023, hr and contributors
# For license information, please see license.txt
from datetime import datetime, timedelta,time

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, time_diff_in_hours, get_time


class Attendance(Document):
	start_time = frappe.db.get_single_value("Attendance Settings", "start_time")
	end_time = frappe.db.get_single_value("Attendance Settings", "end_time")
	working_hours_threshold_for_absent = frappe.db.get_single_value("Attendance Settings", "working_hours_threshold_for_absent")
	late_entry_grace_period = frappe.db.get_single_value("Attendance Settings", "late_entry_grace_period")
	early_exit_grace_period = frappe.db.get_single_value("Attendance Settings", "early_exit_grace_period")

	def on_submit(self):
		self.add_value_Work_Hours()

	def add_value_Work_Hours(self):
		StartT = self.start_time + timedelta(minutes=self.late_entry_grace_period)
		EndT = self.end_time - timedelta(minutes=self.early_exit_grace_period)
		check_in = datetime.strptime(self.check_in, "%H:%M:%S")
		check_out = datetime.strptime(self.check_out, "%H:%M:%S")

		CheckStart = datetime.strptime(str(StartT), "%H:%M:%S")
		CheckEnd = datetime.strptime(str(EndT), "%H:%M:%S")

		CheckStartWork = datetime.strptime(str(self.start_time), "%H:%M:%S")
		CheckEndWork = datetime.strptime(str(self.end_time), "%H:%M:%S")

		work = time_diff_in_hours(CheckEndWork, CheckStartWork)

		if (check_in < CheckStartWork or check_out > CheckEndWork):
			check_in = CheckStartWork

		if (check_in >= CheckStartWork and check_in <= CheckStart and check_out <= CheckEndWork and check_out >= CheckEnd):
			check_in = CheckStartWork
			check_out = CheckEndWork
			work1 = time_diff_in_hours(check_out, check_in)
			self.work_hours = work1
			self.late_hours = work - work1

		elif check_in >= CheckStartWork and check_in >= CheckStart:
			check_in = check_in - timedelta(minutes=self.late_entry_grace_period)
			check_out = check_out + timedelta(minutes=self.early_exit_grace_period)
			work1 = time_diff_in_hours(check_out, check_in)
			self.work_hours = work1
			self.late_hours = work - work1
		elif check_out <= CheckEndWork and check_out <= CheckEnd:
			check_in = check_in - timedelta(minutes=self.late_entry_grace_period)
			check_out = check_out + timedelta(minutes=self.early_exit_grace_period)
			work1 = time_diff_in_hours(check_out, check_in)
			self.work_hours = work1
			self.late_hours = work - work1
		else:
			check_in = check_in - timedelta(minutes=self.late_entry_grace_period)
			check_out = check_out + timedelta(minutes=self.early_exit_grace_period)
			work1 = time_diff_in_hours(check_out, check_in)
			self.work_hours = work1
			self.late_hours = work - work1

		if self.work_hours <= self.working_hours_threshold_for_absent:
			self.status = 'Absent'
		else:
			self.status = 'Present'


