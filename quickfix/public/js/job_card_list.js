console.log("doctype_list_js ------------ loaded")

// want to check how to change color in UI
frappe.listview_settings["Job Card"] = {
    get_indicator(doc) {
        console.log(doc.status)

        if (doc.status == "Ready for Delivery") {
            return ["Ready for Delivery", "blue"];
        } 

        if (doc.status == "Delivered") {
            return ["Delivered", "green"]
        }

        if (doc.status == "Pending Diagnosis") {
            return["Pending Diagnosis", "green"]
        }
    }
}
