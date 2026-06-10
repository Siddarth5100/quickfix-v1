import frappe

def create_device():
    pass

def extend_bootinfo(bootinfo):
    settings = frappe.get_single("QuickFix Settings")
    
    bootinfo.quickfix_shop_name = settings.shop_name
    bootinfo.quickfix_manager_email = settings.manager_email

# E1 - Complete Job Card Lifecycle
# on_submit(): Enqueue send_job_ready_email
def send_job_ready_email(job_card):
    doc = frappe.get_doc("Job Card", job_card)
    
    frappe.sendmail(
        recipients= [doc.customer_email],
        subject= f"Device Status: {doc.status}",
        message= f"Hi {doc.customer_name}, your device: {doc.device_type} current status: {doc.status}"
    )

# F3 jinja hooks: method to get_shop_name()
def get_shop_name():
    name = frappe.get_single("QuickFix Settings")
    return name.shop_name

# get manager email
def get_manager_email():
    email = frappe.get_single("QuickFix Settings")
    return email.manager_email  

# F3 jinja hooks: method to format_job_id()
def format_job_id(job_id):
    prefix_str = "JOB#"
    return prefix_str + job_id

# F5 - Fixtures & Property Setters in Install
def after_install():
    frappe.make_property_setter(
        {
            "doctype": "Job Card",
            "fieldname": "remarks",
            "bold": 1
        }
    )

# K1 - Background Jobs: Queues, Timeouts, Progress
# Task A - Queue names:
# Enqueue send_job_ready_email on "short" queue
def send_job_ready_email(docname):
    doc = frappe.get_doc("Job Card", docname)

    frappe.sendmail(
        recipients= doc.customer_email,
        subject= f"Device: {doc.device_type} status from QuickFix Service center",
        message= f"Hi {doc.customer_name}, you device: {doc.device_type}"
    )
