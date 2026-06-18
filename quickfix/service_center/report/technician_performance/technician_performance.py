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
			"fieldtype": "Int",
			"width": 100
		})
	return columns

def get_data(filters):
	data = []

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	tech_id = filters.get("technician")

	for tech in get_technician_name():
		if tech == tech_id:
			job_cards = frappe.get_list(
				'Job Card', 
				fields=["assigned_technician", "diagnosis_date", "docstatus", "status", "final_amount", "device_type"])

			total_jobs = 0
			completed = 0
			revenue = 0
			tablet = 0
			laptop = 0
			smartphone = 0

			for job in job_cards:
				print("---------------------------", job)
				if job["assigned_technician"] == tech:
					total_jobs += 1
				
				if job.docstatus == 1 and job.status == "Delivered":
					completed += 1
					revenue += job.final_amount
				
					if job.device_type == "Tablet":
						tablet += 1
					elif job.device_type == "Laptop":
						laptop +=1
					elif job.device_type == "Smartphone":
						smartphone += 1

			row = {
				"technician": tech,
				"total_jobs": total_jobs,
				"completed": completed,
				"revenue": revenue,
				"tablet": tablet,
				"laptop": laptop,
				"smartphone": smartphone
			}
			
			data.append(row)

	# total_count = frappe.db.count("Job Card", {filters: {"assigned_technician": tech_id}})

	return data


def get_technician_name():

	all_techs = []

	technician = frappe.get_all(
		"Technician", "name"
	)
	for tech in technician:
		all_techs.append(tech["name"])

	return all_techs
	
