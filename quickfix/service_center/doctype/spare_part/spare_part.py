# Copyright (c) 2026, JC Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SparePart(Document):
	def validate(self):
	# Validate: selling_price > unit_cost always
		if not self.selling_price > self.unit_cost:
			frappe.throw("Selling price should be greater than unit cost")

	# create auto name on speare part
	def autoname(self):
		# convert to uppercase
		if not self.part_code:
			frappe.throw("Enter Part code Eg: PART-001")

		self.part_code = self.part_code.upper()

		# make autoname
		self.name = make_autoname("PART-.YYYY.-.####")

	def on_update(self):
		# doc = frappe.get_doc("QuickFix Settings", "QuickFix Settings")
		# threshold = doc.low_stock_threshold

		'''
		The above one will load full document, fields, metadata, 
		slower for simple value fetch
		'''
		threshold = frappe.db.get_value(
			"QuickFix Settings",
			None,
			"low_stock_threshold"
		)

		'''
		Fetches only one field which is required one, faster
		'''