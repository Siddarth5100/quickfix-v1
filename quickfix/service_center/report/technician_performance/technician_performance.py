# Copyright (c) 2026, JC Siddarth and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_columns(filters):
	columns = [
		{
			"label": "Technician",
			"fieldtype": "Link",
			"fieldname": "technician",
			"options": "Technician",
			"width": 120
		},
		{
			"label": "Total Jobs",
			"fieldtype": "Int",
			"fieldname": "total_jobs",
			"width": 120
		},
		{
			"label": "Completed",
			"fieldtype": "Int",
			"fieldname": "completed",
			"width": 120
		},
		{
			"label": "Avg Turnaround Days",
			"fieldtype": "Float",
			"fieldname": "avg_turnaround_days",
			"width": 120
		},
		{
			"label": "Revenue",
			"fieldtype": "Currency",
			"fieldname": "revenue",
			"width": 120
		},
		{
			"label": "Completion Rate",
			"fieldtype": "Float",
			"fieldname": "completion_rate",
			"width": 120
		}
	]
	
	# get all the documents
	device_type = frappe.get_all("Device Type", fields = ['name'])
	
	# to add dynamic column
	for dt in device_type:
		columns.append({
			"label": dt["name"],
			"fieldname": dt["name"].lower().replace(" ", "_"),
			"fieldtype": "Int"
		})
	return columns

def get_data(filters):
	data = []

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	technician = filters.get("technician")
	print("-------------", from_date, to_date, technician)

	return data