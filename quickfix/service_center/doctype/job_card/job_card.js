// Copyright (c) 2026, JC Siddarth and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Job Card", {
// 	refresh(frm) {

// 	},
// });

// H1 - Job Card Form Script
// setup handler: assign technician based on the matching specilization
console.log("-----------Jobcard js loaded")

frappe.ui.form.on("Job Card", {
    setup(frm) {
        // filter technician
        frm.set_query("assigned_technician", function() {
            return {
                filters: {
                    status: "Active",
                    specialization: frm.doc.device_type
                }
            }
        });
    },

    assigned_technician: function(frm) {
        let tech = frm.doc.assigned_technician;
        let device = frm.doc.device_type;

        frappe.db.get_value("Technician", tech, "specialization")

        .then(r => {
            let specialization = r.message.specialization;

            if (specialization != device) {
                frappe.msgprint("There is no technician in this specialization")
            }
        });
    },

    refresh(frm) {
        // add color code indicator
        if (frm.doc.status == "Draft") {
            frm.dashboard.add_indicator("Draft", "gray")
        }

        if (frm.doc.status == "Pending") {
            frm.dashboard.add_indicator("Pending", "orange")
        }

        if (frm.doc.status == "Diagnosis") {
            frm.dashboard.add_indicator("Diagnosis", "blue")
        }

        if (frm.doc.status == "Awaiting Customer Approval") {
            frm.dashboard.add_indicator("Awaiting Customer Approval", "yellow")
        }

        if (frm.doc.status == "In Repair") {
            frm.dashboard.add_indicator("In Repair", "blue")
        }
        
        if (frm.doc.status == "Ready for Delivery") {
            frm.dashboard.add_indicator("Ready for Delivery", "green")
        }

        if (frm.doc.status == "Delivered") {
            frm.dashboard.add_indicator("Delivered", "green")
        }

        if (frm.doc.status == "Cancelled") {
            frm.dashboard.add_indicator("Cancelled", "red")
        }

        // add custom button ready for delivered
        if (frm.doc.status == "Ready for Delivery" && frm.doc.docstatus == 1) {
            frm.add_custom_button("Mark as Delivered", function() {
                
                frappe.call({
                    method: "frappe.client.set_value",
                    args: {
                        doctype: frm.doctype,
                        name: frm.docname,
                        fieldname: "status",
                        value: "Delivered"
                    },
                    callback:function () {
                        frm.reload_doc().then(() => {
                            frm.refresh();
                        });
                    }
                })
            });
        }

        let shop_name = frappe.boot.quickfix_shop_name;
        console.log(shop_name)

        if(shop_name) {
            frm.page.set_title(frappe.boot.quickfix_shop_name)
        }
    }
});