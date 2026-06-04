import frappe

# F4 - override_whitelisted_methods Hook
@frappe.whitelist()
def custom_get_count(doctype, filters = None, debug = False, cache = False):
    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": doctype,
        "action": "count_queried",
        "user": frappe.session.user
    }).insert(ignore_permissions = True)

    from frappe.client import get_count
    return get_count(doctype, filters, debug, cache)

@frappe.whitelist()
def add_rejection_update():
    # want to add logic here
    pass    