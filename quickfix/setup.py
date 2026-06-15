import frappe
from frappe.utils import now_datetime

def setup_quickfix():
    # default devices
    device_type = ["Mobile", "Laptop", "Tablet"]

    # create default
    for dt in device_type:
        if not frappe.db.exists("Device Type", dt):
            frappe.get_doc({
                "doctype": "Device Type",
                "device_type": dt
            }).insert(ignore_permissions= True)

    # create quickfix settings
    if not frappe.db.exists("QuickFix Settings", "QuickFix Settings"):
        frappe.get_doc({
            "doctype": "QuickFix Settings",
            "default_labour_charge": 500,
            "manager_email": "quickfix@gmail.com",
            "name": "QuickFix Settings",
            "shop_name": "QuickFix" 
        }).insert(ignore_permissions= True)
    
    frappe.msgprint("Created Device types, and basic settings")

# F2 - Install, Boot & Session Hooks
def before_uninstall():
    check_job_cards()

# Checks if any submitted Job Cards exist (before uninstall)
def check_job_cards():
    doc = frappe.get_all(
        "Job Card",
        {"docstatus": 1}
    )

    if doc:
        raise frappe.ValidationError("Submitted Job Cards exist")

# on_session_creation:
def session_creation_logs():
    user = frappe.session.user

    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": "Creation Log",
        "document_name": "Session Creation",
        "action": "on_session_creation",
        "user": user,
        "time_stamp": now_datetime()
    }).insert()

# on_logout:
def session_logout_logs():
    user = frappe.session.user

    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": "Logout Log",
        "document_name": "Session Logout",
        "action": "on_logout",
        "user": user,
        "time_stamp": now_datetime()
    }).insert()