
### B2 - ORM Internals & Query Builder

Part A:
* Out[16]: (('tabJob Card',), ('tabScheduled Job Log',), ('tabScheduled Job Type',))

* payment_status, delivery_date, remarks, status, reason_for_rejection

### C1 - Device Type, Technician, Spare Part, QuickFix Settings
### Child Table Internals
* parent, parentfield, parenttype, idx
* tabPart Usage Entry
* idx value gets swapped to the next row, row 3 will become 2

### C3 - Part Usage Entry & Service Invoice
### Renaming task - write in README_internals.md:
* Once renamed it gets reflected in both original doctype and linke field. Track changes will follow the changes happened, if dint enable then also same rename works, but now the changes not gets tracked. We dont have any reference if anything goes wrong.

* unique constraints works on UI level, it will not allow to add duplicate from UI itself, using frappe.db.exists() in validate for backend db level constraints, sometimes we can bypass UI level but backend will gets blocked.

### Part D - DocStatus transitions
* 0 1 2(0 => draft, 1 => submitted, 2 => Cancelled)
* 
doc.save() on a submitted document
Will gets block or succeeds silenty
Eg: In [3]: doc = frappe.get_doc("Job Card", "JC-2026-00007")
In [4]: doc.save()
Out[4]: <CustomJobCard: JC-2026-00007 docstatus=1>

doc.submit() on a cancelled one:
ValidationError: Cannot edit cancelled document

### Part E - Dangerous patterns

* validate is part of save process, cause recursion error, validate only validate
* Updating another document on validate, again it is not validating

### F3 - Asset, Jinja & Website Hooks

### Asset Hooks

### Que: what is the difference? When would you use each?
(app_include_js & web_include_js)
### Ans:
* App will load in desk, 
* Logged in by system users(Eg: employee login)

* Web will load in portal, website etc
* Logged in by public visitors(Eg: for registering)
 
### Que: doctype_tree_js: not applicable here - explain in README what DocType would use a tree view and why

### Ans:
* Job card is not tree type, it is submittable doctype where tree type will not support  

### Jinja Hooks

### Que: Difference between a Jinja context available in Print Formats vs one available in Web Pages? Are they the same?

### Ans:
Both are different,

Print format works on for a specific document, we can directly access the fields => document genric

Web page is not related to any document => page/context
