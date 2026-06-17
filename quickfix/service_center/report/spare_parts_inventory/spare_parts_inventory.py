# Copyright (c) 2026, JC Siddarth and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = get_columns(filters)
	data, report_summary = get_data(filters)

	return columns, data, report_summary

def get_columns(filters):
	columns = [
		{
			"label": "Part Name",
			"fieldname": "part_name",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": "Part Code",
			"fieldname": "part_code",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": "Device Type",
			"fieldname": "device_type",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": "Stock Qty",
			"fieldname": "stock_qty",
			"fieldtype": "Int",
			"width": 120
		},
		{
			"label": "Reorder Level",
			"fieldname": "reorder_level",
			"fieldtype": "Int",
			"width": 120
		},
		{
			"label": "Unit Cost",
			"fieldname": "unit_cost",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": "Selling Price",
			"fieldname": "selling_price",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": "Margin %",
			"fieldname": "margin",
			"fieldtype": "Percent",
			"width": 120
		},
	]

	return columns

def get_data(filters):
	
	data = []
	total_parts = 0
	below_reorder = 0
	total_value = 0

	total_stock_qty = 0

	doc = frappe.get_all("Spare Part", fields= ["part_name", "part_code", "compatible_device_type", "unit_cost", "selling_price", "stock_qty", "reorder_level"])
			
	for d in doc:
		total_parts += 1

		if d.stock_qty <= d.reorder_level:
			below_reorder += 1

		total_value += d.stock_qty * d.unit_cost

		total_stock_qty += d.stock_qty

		profit_per_item = d.selling_price - d.unit_cost
		margin = (profit_per_item / d.unit_cost) * 100
		
		row = {
			"part_name": d.part_name,
			"part_code": d.part_code,
			"device_type": d.compatible_device_type,
			"stock_qty": d.stock_qty,
			"reorder_level": d.reorder_level,
			"unit_cost": d.unit_cost,
			"selling_price": d.selling_price,
			"margin": margin
		}

		data.append(row)

	report_summary = [
		{
			"label": "Total Parts", 
			"value": total_parts
		},
		{
			"label": "Below Reorder",
			"value": below_reorder
		},
		{
			"label": "Total Inventory Value",
			"value": total_value
		}
	]

	total_row = {
		"part_name": "Total",
		"stock_qty": total_stock_qty,
		"unit_cost": "",
		"selling_price": ""
	}

	data.append(total_row)

	return data, report_summary