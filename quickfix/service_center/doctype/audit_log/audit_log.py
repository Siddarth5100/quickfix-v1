# Copyright (c) 2026, JC Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class AuditLog(Document):
	pass

# F1 - doc_events: Wildcard, Multiple Handlers, Order (5 pts)
# Task A - Wildcard handler:
def log_change(doc, method):
	# frappe.log_error(f"Wildcard triggered: {doc.doctype}-{method}")

	if doc.doctype == "Audit Log":
		return
	
	if doc.doctype not in ["Job Card", "Service Invoice", "Part Usage Entry", "Technician", "Device Type", "Spare Part", "Audit Log", "QuickFix Settings"]:
		return
	
	frappe.get_doc({
		"doctype": "Audit Log",
		"doctype_name": doc.doctype,
		"document_name": doc.name,
		"action": method,
		"user": frappe.session.user,
		"time_stamp": now_datetime()
	}).insert()

def log_validate(doc, method):
	# F1: Test purpose
	# frappe.throw("Doc Events validate error")
	# frappe.log_error("Job Card validate triggered")
	pass