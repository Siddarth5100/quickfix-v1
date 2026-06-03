import frappe
from quickfix.service_center.doctype.job_card.job_card import JobCard

class CustomJobCard(JobCard):
    def validate(self):
        super().validate()
        self._check_urgent_unassigned()
    
    def _check_urgent_unassigned(self):
        if self.priority == "Urgent" and not self.assigned_technician:
            settings = frappe.get_single("QuickFix Settings")
            frappe.enqueue(
                "quickfix.utils.send_urgent_alert",
                job_card = self.name,
                manager= settings.manager_email    
            )

# MRO => method resolution order
'''
* It is the order in which way code runs, if super() dint call here
in the custom one, validation written in core will not run
only what written here will happen
* When we want the core and custom one to happen we want to add super() 
'''