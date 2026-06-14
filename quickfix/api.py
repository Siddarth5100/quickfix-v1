import frappe
from frappe.utils import nowdate, add_days, now_datetime
from frappe.query_builder import DocType

# Part B - frappe.qb Query Builder
# Write a function get_overdue_jobs() using frappe.qb
@frappe.whitelist()
def get_overdue_jobs():
    JC = DocType("Job Card")
    cutoff_date = add_days(now_datetime(), -7)

    overdue_jobs = (
        frappe.qb.from_(JC)
        .select(JC.name, JC.customer_name, JC.assigned_technician, JC.creation)
        .where(
            JC.status.isin(["Pending Diagnosis", "In Repair"])
            & (JC.creation < cutoff_date)
        )
        .orderby(JC.creation)
    ).run(as_dict= True)

    return overdue_jobs    

# Part C - Transactions & commit behavior
# Write a function transfer_job(from_tech, to_tech) that reassigns all open Job Cards
@frappe.whitelist()
def transfer_job(from_tech, to_tech):
    try:
        frappe.db.sql(
            """
            UPDATE `tabJob Card`
            SET assigned_technician = %s
            WHERE assigned_technician = %s
            AND status NOT IN (%s, %s)
            """,
            (to_tech, from_tech, "Delivered", "Cancelled")
        )
        frappe.db.commit()

        return {
            "message": f"Open Jobs transferred from {from_tech} to {to_tech}" 
        }
    
    except Exception as e:
        frappe.db.rollback()

        frappe.log_error(
            frappe.get_traceback(),
            "Job Transfer Failed"
        )
        raise

# D1 - Roles, Permission Matrix, Document Sharing
# Demonstrate frappe.share: write a whitelisted method
# share_job_card(job_card_name, user_email)
@frappe.whitelist()
def share_job_card(job_card_name, user_email):
    frappe.share.add("Job Card", job_card_name, user_email, read=1)
    frappe.db.commit()

    return "Shared successfully"

# In api.py, write a method that calls frappe.only_for("QF Manager")
@frappe.whitelist()
def manager_call():
	frappe.only_for("QF Manager")
	return "Successful"

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

# L1 - REST Resource API & Custom API
# Task C - Custom whitelisted method design:
@frappe.whitelist()
def get_job_summary():
    job_card_name = frappe.form_dict.get("job_card_name")

    if not job_card_name:
        return{
            "error": "Required job_card_name"
        }

    if not frappe.db.exists("Job Card", job_card_name):
        return {
            "error": "Job Card not found",
        }

    doc = frappe.get_doc("Job Card", job_card_name)

    return {
        "name": doc.name,
        "status": doc.status,
        "customer_name": doc.customer_name,
        "assigned_technician": doc.assigned_technician,
        "device_type": doc.device_type
    }