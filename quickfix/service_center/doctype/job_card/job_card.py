# Copyright (c) 2026, JC Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JobCard(Document):
	def validate(self):
		# F1: Test purpose
		# frappe.throw("Controller validate error")

		# validate phone number length
		if len(self.customer_phone) != 10:
			frappe.throw("Phone number should be exact 10 digits")
		
		# check technician assigned or not
		if self.status in ["In Repair", "Ready for Delivery", "Delivered", "Cancelled"]:
			if not self.assigned_technician:
				frappe.throw("Technician must assigned")

		# calculate parts usage
		final_total = 0
		for part in self.parts_used:
			part.total_price = part.unit_price * part.quantity
			final_total += part.total_price

		# sum of all rows
		self.parts_total = final_total
		
		# assign labour charge
		if not self.labour_charge:
			self.labour_charge = frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")

		# calculate final amount
		self.final_amount = self.parts_total + self.labour_charge
	
	def before_save(self):
		# Enqueue send_job_ready_email
		if self.status == "Ready for Delivery":
			frappe.enqueue(
				method= "quickfix.utils.send_job_ready_email",
				queue= "short",
				docname= self.name
			)

	def before_submit(self):
		# allow only if status = ready for delivery
		if self.status != "Ready for Delivery":
			frappe.throw("Status is not Ready for Delivery")
		
		# for each part in parts_used: check stock_qty >= quantity
		for part in self.parts_used:
			stock_avail = frappe.db.get_value("Spare Part", part.part, "stock_qty")
			if not stock_avail >= part.quantity:
				frappe.throw(f"Stock not available, Part Name: {part.part_name} & Balance Available: {stock_avail}")

	def on_submit(self):
		# deduct stock quantity
		for part in self.parts_used:
			stock_avail = frappe.db.get_value("Spare Part", part.part, "stock_qty")
			final_qty = stock_avail - part.quantity
		
			frappe.db.set_value("Spare Part", part.part, "stock_qty", final_qty)

		'''
		WHY ignore_permissions is acceptable here (system-initiated deduction, not 
		user-initiated)
		* Because this is done by system logic not by user manually editing 
		'''

		# auto create service invoice
		doc = frappe.get_doc({
			"doctype": "Service Invoice",
			"job_card": self.name,
			"invoice_date": self.delivery_date,
			"labour_charge": self.labour_charge,
			"parts_total": self.parts_total,
			"total_amount": self.final_amount,
			"payment_status": self.payment_status
		}).insert(ignore_permissions = True)
		
		# call publish realtime for job ready
		frappe.publish_realtime(
			'job_ready',
			{
				"job_card": self.name,
				"status": "Ready"
			},
			user= self.owner)
		
		# enqueue job ready email
		frappe.enqueue(
			"quickfix.utils.send_job_ready_email",
			job_card= self.name,
			queue= "short"
		)

		# L2 - Webhooks: Outgoing & Incoming
		# Task A - Outgoing Webhook:
		frappe.enqueue(
			"quickfix.utils.send_webhook",
			job_card_name= self.name,
			queue= "short",
			job_name= f"Webhook Test {self.name}"
		)

	def on_cancel(self):
		# Set status = "Cancelled"
		self.db_set("status", "Cancelled")

		# Restore stock_qty for all parts
		for part in self.parts_used:
			
			spare_part = frappe.get_doc("Spare Part", part.part)
			spare_part.stock_qty += part.quantity
			spare_part.save()
		
		# If Service Invoice exists, cancel it:
		if frappe.db.exists("Service Invoice", {"job_card": self.name}):
			invoice = frappe.db.get_value(
				"Service Invoice",
				{"job_card": self.name},
				"name"
			)

			doc = frappe.get_doc("Service Invoice", invoice)
			# doc.cancel()

	def on_trash(self):
		# prevent deletion of job cards with status != "Cancelled" & "Draft"
		if self.status not in ["Cancelled", "Draft"]:
			frappe.throw("Status should be either 'Cancelled' or 'Draft'")
	
	def on_update(self):
		# print("--------------------------On_update called")
		# self.save()
		pass

	def before_print(self, settings= None):
		self.print_summary = f"{self.customer_name} - {self.device_brand} {self.device_model}"
