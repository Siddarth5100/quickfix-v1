
### B2 - ORM Internals & Query Builder

Part A:
* Out[16]: (('tabJob Card',), ('tabScheduled Job Log',), ('tabScheduled Job Type',))

tab prefix is the tableTable_name AS Eg:tabjob Card

* payment_status, delivery_date, remarks, status, reason_for_rejection

### Part D - DocStatus transitions
* 0 1 2(0 => draft, 1 => submitted, 2 => Cancelled)
* 
doc.save() on a submitted document
Will gets block or succeeds silently
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

### E1 - Complete Job Card Lifecycle
### on_update() - demonstrate the recursion pitfall:
### Call self.save() inside on_update and see to the issues of it and explain

* Calling self.save() inside on_update causes recursion

save() triggers on_update(),
if on_update() calls save() again, the document enter in infinite loop of save and update

correct pattern self.db_set() or self.db.set_value()

error : 22:12:46 web.1         | RecursionError: maximum recursion depth exceeded

### E2 - autoname & Renaming
### Que: In a utility function, call frappe.rename_doc("Technician", old_name, new_name, merge=False) and show how linked fields (assigned_technician on Job Cards) are updated automatically

### Ans:
frappe.rename_doc() automatically updates all link fields to the renamed document

### Que: when would merge=True be dangerous?

### Ans:
* merge+True is dangerous because 2 records become one record,
which can lead to accidental data mixing or loss

### E3 - Standard Controller Pattern & override_doctype_class
### Part B - Upgrade friction analysis:
### Que: Assume the Frappe core updates Job Card's validate() to add a new check. If you override_doctype_class and forget to update super() - what breaks?

### Ans:
* If we forgot to add super(), core we have some validations that will not happen, only the current file will run

Eg:
class CustomJobCard(JobCard):
    def validate(self):
        self._check_urgent_unassigned()
    
    def _check_urgent_unassigned(self):
        if self.priority == "Urgent" and not self.assigned_technician:
            settings = frappe.get_single("QuickFix Settings")
            frappe.enqueue(
                "quickfix.utils.send_urgent_alert",
                job_card = self.name,
                manager= settings.manager_email    
            )

here i created a file to override jobcard and i dint add super(), but i have some other important validations in core, while running frappe sees hooks file and there will be path to this method, so that will excute only this. 

### Que:
### Explain in README_internals.md: why is doc_events safer than override_doctype_class for most use cases?

### Ans:
Docevents is safer because it only adds extra behaviour on top of existing Doctype events (Eg: validate, on_submit) without changing the original core logic.

Override doctype class is riskier because it replace or extends the full class. If core doctype change and forgot to call super(), core validations may skipped

### F1 - doc_events: Wildcard, Multiple Handlers, Order
### Task B - Multiple handler conflict:
### Que: Register TWO validate handlers on Job Card - one in your main controller and one in doc_events.

### Ans: 
Main controller runs 1st then doc events runs, if both raise validation error, controller throws error and docevents also throws error, 
Executioin stops at 1st error, second handler never runs

### Que: Demonstrate: what happens when you register "*" AND a specific DocType handler for the same event? Do both run?

### Ans:
Both runs, 
"*" handler runs (Audit log)
"Job Card" handler runs (validate / custom logic)

wildcard runs for every doctype, specific hook runs only for Job Card

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

### F5 - Fixtures & Property Setters in Install
### Que: Explain fieldname collision risk: what happens if your Custom Field has the same fieldname as a field added by a future Frappe update?

### Ans:
Eg: custom field = "status" ; future frappe update adds "status" field

then, field definition conflict, UI behave unexpectedly, 
data mismatch or overwrite risk, migration error happens during
update/patch 

### Que: Explain patching order: if Patch 1 creates a Custom Field and Patch 2 reads it, why must they be separate entries in patches.txt and never merged?

### Ans:
Patch = is a python script designed to execute exactly once during database migrations

Developers use patches to update database schema, migrate existing data or fix inconsistencies across live sites without breaking production data.

Patch 1 = creates custom field
Patch 2 = uses that field

if we merge both run in one go, run one by one 

### H3 - List View & Tree View
### Que: Describe what a Tree DocType is (example: Account,Employee hierarchy). What is doctype_tree_js used for and what extra fields does a tree DocType require (parent_field, is_group)?

### Ans:
Tree doctype, modified tree order traversal. Interlinked in an organised way
extra fields => lft, rgt, is_group, parent_account

Eg: 
Account
	Bank_1
		User_1
			Primary Account
			Secondary Account
		User_2
			primary Account
	Bank_2
		Primary Account

Organisation
	Location_1
		HR
		Devloper
			Employee_1
	Location_2

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

### K1 - Background Jobs: Queues, Timeouts, Progress
### Task A - Queue names:
### Que: Explain the 3 queue names (default, long, short) and when to use each

### Ans:
3 queues are default, long, short
* short 300 sec: if it is small work like notifications, confirmantions not time taking process will add in short
* long 1500 sec: if it is time taking work like employees salary update will add it in long queue
* default 300 sec: this is for normal not less or time taking process

### L1 - REST Resource API & Custom API
### Task A - Resource API
* GET /api/resource/Job Card - list Job Cards (use session cookie from browser)
method: GET
url: http://quickfix-dev.localhost:8002/api/resource/Job Card
headers
key => Cookie
(session cookie => open job card list => console(fn+f12) => network => refresh
=> click on any request =>  Request header => Cookie)
value => sid=827a6ebea4093e2150086ed90554acc805efe3013c544162e93ebd5a
key => Content Type
value => application/json 
body => raw json

request: http://quickfix-dev.localhost:8002/api/resource/Job Card

response: 
{
    "data": [
        {
            "name": "JC-2026-00002"
        },
    ]
}

* GET /api/resource/Job Card/JC-0001
key: X-Frappe-CSRF-Token value: 15a4de1fa0233c9f71db2b0c1c4e0fcd54d9027c81daa598ceeb54b6
 
request: http://quickfix-dev.localhost:8002/api/resource/Job Card/JC-2026-00029

response: --

for post, put, delete : if get basic authentication is fine, but if it is put, post, delete we want to csrf token

* POST /api/resource/Spare Part
key: X-Frappe-CSRF-Token 
value: 15a4de1fa0233c9f71db2b0c1c4e0fcd54d9027c81daa598ceeb54b6

request: http://quickfix-dev.localhost:8002/api/resource/Spare Part

response:
{
    "part_name": "Head set",
    "part_code": "PART-035",
    "compatible_device_type": "Tablet",
    "unit_cost" : 2000,
    "selling_price": 3000,
    "stock_qty": 30
}

* PUT /api/resource/Spare Part/PART-0001
key: X-Frappe-CSRF-Token (Headers)
value: 15a4de1fa0233c9f71db2b0c1c4e0fcd54d9027c81daa598ceeb54b6

request: http://quickfix-dev.localhost:8002/api/resource/Spare Part/PART-2026-0002
{
    "selling_price": 3000
}

response:
{
    "data": {
        "name": "PART-2026-0002",
        "owner": "Administrator",
        "creation": "2026-06-10 18:57:24.471575",
        "modified": "2026-06-10 23:21:49.484067",
        "modified_by": "Administrator",
        "docstatus": 0,
        "idx": 0,
        "part_name": "Head set",
        "part_code": "PART-035",
        "compatible_device_type": "Tablet",
        "unit_cost": 2000.0,
        "selling_price": 3000.0,
        "stock_qty": 30.0,
        "reorder_level": 5.0,
        "is_active": 1,
        "doctype": "Spare Part"
    }
}

* DELETE /api/resource/Spare Part/PART-0001
key: X-Frappe-CSRF-Token (Headers)
value: 15a4de1fa0233c9f71db2b0c1c4e0fcd54d9027c81daa598ceeb54b6

request:
http://quickfix-dev.localhost:8002/api/resource/Spare Part/ags3nqjfrf

response:
{
    "data": "ok"
}

