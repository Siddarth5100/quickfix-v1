import frappe

def create_device():
    pass

def extend_bootinfo(bootinfo):
    settings = frappe.get_single("QuickFix Settings")
    
    bootinfo.quickfix_shop_name = settings.shop_name
    bootinfo.quickfix_manager_email = settings.manager_email