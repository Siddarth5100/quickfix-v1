# Copyright (c) 2026, JC Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
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
	
	def before_submit(self):
		# allow only if status = ready for delivery
		if self.status != "Ready for Delivery":
			frappe.throw("Status is not Ready for Delivery")
		
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
		
		# enqueue job ready email

	def on_cancel(self):
		self.status = "Cancelled"

	def on_trash(self):
		# if self.status != "Cancelled" or self.status != "Draft":
		# 	frappe.throw("Status should be either 'Cancelled' or 'Draft'")
		pass