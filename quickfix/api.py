import frappe
from frappe.utils import nowdate, add_days
from frappe.query_builder import DocType

# Part B - frappe.qb Query Builder
# Write a function get_overdue_jobs() using frappe.qb
def get_overdue_jobs():
    JC = DocType("Job Card")

    cutoff_date = add_days(nowdate(), -7)

    overdue_jobs = (
        frappe.qb.from_(JC)
        .select(JC.name, JC.customer_name, JC.assigned_technician, JC.creation)
        .where(
            JC.status.isin(["Pending Diagnosis", "In Repair"])
            & (JC.creation < cutoff_date)
        )
        .orderby(JC.creation.asc())
    ).run(as_dict= True)

    return overdue_jobs    

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