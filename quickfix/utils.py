import frappe

def create_device():
    pass

def extend_bootinfo(bootinfo):
    settings = frappe.get_single("QuickFix Settings")
    
    bootinfo.quickfix_shop_name = settings.shop_name
    bootinfo.quickfix_manager_email = settings.manager_email


# f3 jinja hooks: method to get_shop_name()
def get_shop_name():
    name = frappe.get_single("QuickFix Settings")
    return name.shop_name 

# f3 jinja hooks: method to format_job_id()
def format_job_id(job_id):
    prefix_str = "JOB#"
    return prefix_str + job_id