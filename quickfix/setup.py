import frappe

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