// Copyright (c) 2026, JC Siddarth and contributors
// For license information, please see license.txt

frappe.query_reports["Technician Performance"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
		},
		{
			fieldname: "technician",
			label: "Technician",
			fieldtype: "Link",
			options: "Technician"
		}
	],

	onload: function(report) {
		set_default_dates(report);
	},

	refresh: function(report) {
		set_default_dates(report);
	}
};

function set_default_dates(report) {
	let from_date = report.get_filter_value("from_date");
	let to_date = report.get_filter_value("to_date");

	if(!from_date && !to_date) {
		let today = frappe.datetime.get_today();

		let first_day = frappe.datetime.get_first_day(today);
		let last_day = frappe.datetime.get_last_day(today);

		report.set_filter_value("from_date", first_day);
		report.set_filter_value("to_date", last_day)
	}
}