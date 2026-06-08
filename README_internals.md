
### B2 - ORM Internals & Query Builder

Part A:
* Out[16]: (('tabJob Card',), ('tabScheduled Job Log',), ('tabScheduled Job Type',))

* payment_status, delivery_date, remarks, status, reason_for_rejection

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

### C1 - Device Type, Technician, Spare Part, QuickFix Settings
### Child Table Internals
* parent, parentfield, parenttype, idx
* tabPart Usage Entry
* idx value gets swapped to the next row, row 3 will become 2

### C3 - Part Usage Entry & Service Invoice
### Renaming task - write in README_internals.md:
* Once renamed it gets reflected in both original doctype and linke field. Track changes will follow the changes happened, if dint enable then also same rename works, but now the changes not gets tracked. We dont have any reference if anything goes wrong.

* unique constraints works on UI level, it will not allow to add duplicate from UI itself, using frappe.db.exists() in validate for backend db level constraints, sometimes we can bypass UI level but backend will gets blocked.

### D1 - Roles, Permission Matrix, Document Sharing
### In api.py, write a method that calls frappe.only_for("QF Manager") and explain what it does if a non-manager calls it

* If the user is manager will receive the success response
* If the user in non-manager will receive PermissionError

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

### I1 - Query Report with SQL Safety

### Que: Demonstrate and explain the issues and solutions with respect to f-string SQL and the parameterized pattern.

### Ans:
f-string : 
* Allows for SQL Injection, where we can bypass login easily
* Python evaluates the variables and convert to plain text SQL String before in send to Database

Parameterization:
* Use place holders instead Eg: %s, ?
* Parameterized pattern prevents SQL Injection by sending the SQL structure and the user data as two separate transmission to the Database

### Que: Add a EXPLAIN statement in bench console for your query - screenshot the result and identify if an index is being used on the status column

### Ans:

query:
frappe.db.sql(
    """
    EXPLAIN
    SELECT name, customer_name, device_type, status, assigned_technician, estimated_cost, creation
    FROM `tabJob Card`
    WHERE status NOT IN ('Delivered', 'Cancelled')
    """, as_dict- True
)
ouput:

[{'id': 1,
  'select_type': 'SIMPLE',
  'table': 'tabJob Card',
  'type': 'ALL',
  'possible_keys': None,
  'key': None,
  'key_len': None,
  'ref': None,
  'rows': '20',
  'Extra': 'Using where'}]

No index exists on the status column

### I5 - Report Builder & Custom Report
### Que: when is Report Builder appropriate? When must you use Script Report?

* If we want prepare immediate report with simple query, without code we can use Report builder, with single doctype

* If we want full control over the report we can use the script report, calculations, python logic, dynamic columns, multiple doctypes 