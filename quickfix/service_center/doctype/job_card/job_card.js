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
    }
});