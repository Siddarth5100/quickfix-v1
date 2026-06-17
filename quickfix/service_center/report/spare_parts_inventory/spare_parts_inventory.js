// Copyright (c) 2026, JC Siddarth and contributors
// For license information, please see license.txt

frappe.query_reports["Spare Parts Inventory"] = {
	formatter: function(value, row, column, data, default_formatter) {
		
		let formatted_value = default_formatter(value, row, column, data);
		console.log("Test color", data.stock_qty, data.reorder_level)
		if (data && data.stock_qty <= data.reorder_level) {
			formatted_value =  `<div style= "background-color:red; color:white;">
				${formatted_value}	
			</div>`;
		}

		return formatted_value;
	},
};
