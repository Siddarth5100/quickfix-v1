// want to check how to change color in UI
frappe.listview_settings["Job Card"] = {
    get_indicator(doc) {
        if (doc.status == "Ready for Delivery") {
            return ["Ready for Delivery", "blue"];
        } 

        if (doc.status == "Delivered") {
            return ["Delivered", "green"]
        }

        if (doc.status == "Pending Diagnosis") {
            return ["Pending Diagnosis", "Orange"]
        }
    }
}
