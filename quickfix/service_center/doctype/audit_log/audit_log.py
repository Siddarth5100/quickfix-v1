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
	if doc.doctype == "Audit Log":
		return
	
	frappe.get_doc({
		"doctype": "Audit Log",
		"doctype_name": doc.doctype,
		"document_name": doc.name,
		"action": method,
		"user": frappe.session.user,
		"timestamp": now_datetime()
	}).insert()