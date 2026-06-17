// Copyright (c) 2026, JC Siddarth and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Job Card", {
// 	refresh(frm) {

// 	},
// });
console.log("-----------Jobcard js loaded")

// E1 - Complete Job Card Lifecycle
// on_submit():
// Call frappe.publish_realtime("job_ready", {...}, user=self.owner)
frappe.realtime.on("job_ready", function(data) {
        alert(`Job ${data.job_card} is ready`);
    });

// H1 - Job Card Form Script
// setup handler: assign technician based on the matching specilization
frappe.ui.form.on("Job Card", {
    // H1 - Job Card Form Script (Observation Task)
    // Making a frappe.call inside the validate client
    // validate(frm) {
    //     console.log("1. validate started")
    //     frappe.call({
    //         method: "quickfix.api.test_method",
    //         callback: function(r) {
    //             console.log("3. callback finishes")
    //         }
    //     });
    //     console.log("2. validate ended")
    // },

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
                    callback: function () {
                        frm.reload_doc().then(() => {
                            frm.refresh();
                        });
                    }
                })
            });
        }

        // display app name in the form header
        let shop_name = frappe.boot.quickfix_shop_name;
        if(shop_name) {
            frm.page.set_title(frappe.boot.quickfix_shop_name)
        }

        // H2 - Dialog, Prompt, Confirm
        // add custom button with dialog mandatory
        frm.add_custom_button("Reject Job", function() {
            let d = new frappe.ui.Dialog({
                title: "Reject Job",
                fields: [
                    {
                        label: "Rejection Reason",
                        fieldname: "reason",
                        fieldtype: "Small Text",
                        reqd: 1
                    }
                ],
                
                size: "small", 
                primary_action_label: "Submit",
                primary_action(values) {
                    console.log(values);
                    frm.set_value("reason_for_rejection", values.reason);
                    frm.set_value("status", "Cancelled")
                    frm.save();
                    d.hide();
                }
            });
            d.show()
        })

        // using prompt create button to transfer technician
        frm.add_custom_button("Transfer Technician", function() {
            frappe.prompt(
                [
                    {
                        fieldtype: "Link",
                        label: "Select Technician",
                        fieldname: "technician_name",
                        options: "Technician"
                    }
                ],
                function (values) {
                    frappe.confirm(
                        "Are you Sure want to transfer?",
                        () => {
                            frappe.call({
                                method: "quickfix.api.transfer_job",
                                args: {
                                    from_tech: frm.doc.assigned_technician,
                                    to_tech: values.technician_name
                                },
                                callback: function (r) {
                                    frappe.msgprint("Transferred job cards Successfully")
                                    frm.reload_doc()
                                    frm.trigger("assigned_technician")
                                }
                            })
                        }
                    )
                }
            )
        })
    },
});

// H1 - Job Card Form Script
// Field change handlers: In child table Part: quantity change - update total_price = qty × unit_price using
frappe.ui.form.on("Part Usage Entry", {
    part: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        let total = row.unit_price * row.quantity
        frappe.model.set_value(cdt, cdn, "total_price", total)
    },

    quantity: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "total_price", row.unit_price * row.quantity)
    }
})
