import frappe
from frappe.utils import today, now_datetime
from quickfix.setup import setup_quickfix
import requests, json
from datetime import timedelta

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

# E3 - Standard Controller Pattern & override_doctype_class
# Part A - Override your own DocType
def send_urgent_alert(job_card, manager):
    frappe.sendmail(
        recipients= [manager],
        subject= "Urgent Job Card Alert",
        message= f"Job card {job_card} is marked urgent" 
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
    setup_quickfix()
    make_field_bold()

# after_install, call frappe.make_property_setter to make the remarks field bold on 
# Job Card
def make_field_bold():
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

# Task B - Idempotency:
def check_low_stock():
    last_run = frappe.db.get_value("Audit Log", {
        "action": "Low stock check",
        "creation": ("like", today() + "%")
    }, "name")

    if last_run:
        return

    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": "Spare Part",
        "document_name" : "Daily Low stock Check",
        "action": "Low stock check",
        "user": "Admin",
        "time_stamp": now_datetime()
    }).insert()

# Task C - Long-running job with progress updates:
def generate_monthly_revenue_report(year):
    months = range(1, 13)
    for i, month in enumerate(months, 1):
        frappe.publish_progress(
            percent = round(i/12* 100),
            title = "Generating Revenue Report",
            description = f"Processing moth {month}"
        )
    
def enqueue_monthly_report():
    frappe.enqueue(
        "quickfix.utils.generate_monthly_revenue_report",
        queue= "long",
        timeout= 600,
        year= 2026
    )

# L2 - Webhooks: Outgoing & Incoming
# Task A - Outgoing Webhook:
def send_webhook(job_card_name, retry_count=0):
    settings = frappe.get_single("QuickFix Settings")

    if not settings.webhook_url:
        return

    doc = frappe.get_doc("Job Card", job_card_name)
    payload = {
        "event": "job_submitted",
        "job_card": doc.name,
        "amount": doc.final_amount
    }

    if retry_count >= 3:
        return {
            "error": "count exceeds"
        }

    try:
        r = requests.post(settings.webhook_url, json=payload, timeout=5)
        r.raise_for_status()

    except Exception as e:
        retry_count += 1

        frappe.enqueue(
            "quickfix.utils.send_webhook",
            job_card_name = job_card_name,
            retry_count = retry_count
        )
        
        frappe.log_error(f"Webhook failed: {e}", "Webhook Error")