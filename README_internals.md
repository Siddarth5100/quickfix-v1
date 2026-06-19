### B1 - Trace a Request End-to-End
### Step 3 - Error visibility

### developer mode 1
1         | Traceback (most recent call last):
15:56:59 web.1         |   File "apps/frappe/frappe/app.py", line 120, in application
15:56:59 web.1         |     response = frappe.api.handle(request)
15:56:59 web.1         |                ^^^^^^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/api/__init__.py", line 52, in handle
15:56:59 web.1         |     data = endpoint(**arguments)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/api/v1.py", line 40, in handle_rpc_call
15:56:59 web.1         |     return frappe.handler.handle()
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/handler.py", line 53, in handle
15:56:59 web.1         |     data = execute_cmd(cmd)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/handler.py", line 86, in execute_cmd
15:56:59 web.1         |     return frappe.call(method, **frappe.form_dict)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/__init__.py", line 1760, in call
15:56:59 web.1         |     return fn(*args, **newargs)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/utils/typing_validations.py", line 32, in wrapper
15:56:59 web.1         |     return func(*args, **kwargs)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/quickfix/quickfix/api.py", line 191, in test_error
15:56:59 web.1         |     raise Exception("Test Error")
15:56:59 web.1         | Exception: Test Error
15:56:59 web.1         | 

### developer mode 0
1         | Traceback (most recent call last):
15:56:59 web.1         |   File "apps/frappe/frappe/app.py", line 120, in application
15:56:59 web.1         |     response = frappe.api.handle(request)
15:56:59 web.1         |                ^^^^^^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/api/__init__.py", line 52, in handle
15:56:59 web.1         |     data = endpoint(**arguments)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/api/v1.py", line 40, in handle_rpc_call
15:56:59 web.1         |     return frappe.handler.handle()
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/handler.py", line 53, in handle
15:56:59 web.1         |     data = execute_cmd(cmd)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/handler.py", line 86, in execute_cmd
15:56:59 web.1         |     return frappe.call(method, **frappe.form_dict)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/__init__.py", line 1760, in call
15:56:59 web.1         |     return fn(*args, **newargs)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/frappe/frappe/utils/typing_validations.py", line 32, in wrapper
15:56:59 web.1         |     return func(*args, **kwargs)
15:56:59 web.1         |            ^^^^^^^^^^^^^^^^^^^^^
15:56:59 web.1         |   File "apps/quickfix/quickfix/api.py", line 191, in test_error
15:56:59 web.1         |     raise Exception("Test Error")
15:56:59 web.1         | Exception: Test Error
15:56:59 web.1         | 

### browser receives:
Full traceback shown in UI
File path: apps/quickfix/api.py
Exact exception message

### developer_mode
generic response
No full trace back shown in UI

### Que: Where do production errors go if they are hidden from the browser?

### Ans: save in 3 places
Error log, server logs, Bg failure logs(RQ)

### Step 4 - Permission check location:
### Que: In a whitelisted method, call frappe.get_doc("Job Card", name) WITHOUT ignore_permissions.

If user dont have permission will get the error,

User suresh@gmail.com does not have doctype access via role permission for document Job Card

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

def validate(self):
    self.total = sum(r.amount for r in self.items)

def on_submit(self):
    other = frappe.get_doc("Spare Part", self.part)
    other.stock_qty -= self.qty
    other.save()

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

### Que: Build cache-busting: explain what bench build --app quickfix does and why assets need cache-busting after JS changes

### Ans:

bench build --app, 
converts /public/js to /assets, bundles files, update changes happend in .js files for frontend. Because browser caches old JS file, changes maynot reflect.

cache busting: after changes
bench clear-cache
bench build
bench restart

app_include_js => Desk global JS
web_include_js => Website/ portal JS

doctype_js => Form level JS
doctype_list_js => List view JS
doctype_tree_js => Hierarichal Doctypes

### Jinja Hooks

### Que: Difference between a Jinja context available in Print Formats vs one available in Web Pages? Are they the same?

### Ans:
Both are different,

Print Format: document based context (doc already available)
(One record view) doc
Eg: {{ doc.customer }}, {{ doc.total_amount }}

Print format works on for a specific document, we can directly access the fields => document genric

Web Pages: system + session +dynamic data context
(Full website environment) not tied to single document
uses frappe.get_all, .db, .session
Eg: {{ frappe.session.user }}, {{ get_shop_name() }}

Web page is not related to any document => page/context

### F4 - override_whitelisted_methods Hook
### Que: confirm the override is called, confirm the original logic still returns the correct count, confirm no other app's calls to frappe.client.get_count are broken

### Ans:
Test in postman:

http://quickfix-dev.localhost:8002//api/method/frappe.client.get_count?doctype=Job Card

returns the count of total docs in the doctype, dint breack for others 

### Que: What happens if TWO apps both register override_whitelisted_methods for the same method? Write the answer.

### Ans:
Only one can work, based on the app loading order(apps.txt)
The later loaded app works(precedence)

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

### H1 - Job Card Form Script
### Que: Making a frappe.call inside the validate client event (before_save handler) - explain why this does not work

### Ans:
frappe.call({}) => works asynchronously, where as validate runs immediately, validate will not wait till callback receives

Eg: 
Save starts
Validate ends
Document may already save
Server response comes later
Callback runs later

### Que: Using onload or refresh for async data fetches
Because these events are for loading data into the UI, No save happens, No validation waiting,

Eg:
Open Job Card
Refresh runs
Frappe.call goes to server
Response comes back
Field gets updated

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

### Que: I4 - Prepared Report
### explain when you would use a Prepared Report vs a real-time Script Report. What are the staleness tradeoffs

### Ans
Prepared report,
If it is large dataset, will use Prepared report

Realtime script report.
If it is small data, will use relatime script report

Staleness trade offs,
As this is cached data, wil not be always upto date

Eg: 
Data is computed once in background
Stored in cache
UI shows cached result

Problem: If data changes after caching - user still sees old data

Script Report
Runs SQL every time user opens report
Always fresh data

### Que: Describe the caching risk: if underlying data changes between report preparations, what does the user see?

### Ans: 
Eg: 
Report generated => Total jobs = 100
New Job added => Total jobs becomes 120 in DB
User opens report => Still shows 100(cached)

This is the caching risk, report becomes inconsistent with real database state.

As the results are precomputed and stored in cache, any changes underlying database after report generated not immediately reflected. As a result users may see outdated or inconsistent data,
until the report is regenerated or refreshed.
 
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

### Que: Explain retry behavior: how many times does Frappe retry a failed background job by default?

### Ans:
When a bgjob fails, frappe logs the exception in Error log and marks it in RQ failed jobs. By deault, frappe retries a failed job 3 times using Redis queue, after exceeds job is marked permanently failed

### K2 - Scheduler Events & Cron
### Que: How do you disable the scheduler for a specific site? Why would you do this on a dev site?

### Ans:
cmd: bench --site site_name.local disable-scheduler
enable back : bench --site site_name.local enable-scheduler

To disable in dev site, 
* To avoid unwanted bg jobs, while testing
* To save system resources workers + cron jobs consume CPU + DB load
* Allowed controlled manual testing

### Que: Explain: what happens to scheduled jobs that were queued while the worker was down - do they run when the worker comes back up?

### Ans:
When workers down, scheduled jobs still get added to redis queue, but will not execute. When workers comes backup, worker starts reading Redis queue again

### K3 - Performance Engineering

### Task A - N+1 query detection and fix:
The following code has an N+1 query problem. Identify it and rewrite it:

### Ans:
raw sql(for reference)
SELECT T.technician_name, T.phone
FROM `tabJob card` AS JC
RIGHT JOIN `tabTechnician` AS T
ON JC.assigned_technician = T.name

result = frappe.db.sql("""
    SELECT
        t.technician_name,
        t.phone
    FROM `tabJob Card` jc
    RIGHT JOIN `tabTechnician` t
    ON jc.assigned_technician = t.name
"""), as-dict=True

N+1 query makes the DB performance makes slower.

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

### Task B - Token Authentication (API key + secret):
### Que: 
### Generate an API key and secret for your test user (User - API Access)

### Ans:
goto => user => open test user => settings => api access => generate keys
copy keys and use in the below format
token API key: API secret

### Que:
### Make a curl request with: Authorization: token api_key:api_secret

### Ans:
goto postman, choose method, enter url, in headers use 
key: Authorization
Value: token API key value:API secret key value

### L2 - Webhooks: Outgoing & Incoming
### Task B - Incoming Webhook Endpoint:

### Que:
### why must you use hmac.compare_digest instead of == for signature comparison? (Timing attack prevention)

### Ans:
* == is normal comparison Eg: a == b
Python compares character by character, it stop early when mismatch is found. 
This creates time difference, correct part takes longer
wrong early returns faster, where hackers can measure this time
this is called timing attack(measures exactly how long a system takes to process a specific input)

* hmac.compare_digest(a, b)
compares in fixed time, always checks full string, no early exit

signature = security proof so we want to use hmac.compare_digest

### Que:
### Explain the deduplication strategy: what happens if the payment gateway sends the same event twice?

### Ans:
* without deduplication
Payment gateway may send same webhook twice,
Payment success (PAY-001) => mark invoice PAID
sent to frappe
Sent again (retry/ network issue) => again mark PAID / create duplicate entry

This causes; duplicate invoices, double updates, wrong accounting

* with deduplication
Before processing, checks in db is there any log, if already exists process will not happen again, if not will proceed the process

### M1 - Server Script DocType
### Que: What Python functions/modules are blocked in the Server Script sandbox?

### Ans:
server scripts run in a restricted environment

commonly blocked;
import os, subprocess, socket, requests
open(), eval(), exec(), __import__() 

and many other unsafe modules, functions. To prevent file, system, network access etc.

Error:
"exception": "ImportError: __import__ not found",
"exc_type": "ImportError",

### Que: List 3 things you CANNOT do in a Server Script that you can do in app code.

### Ans:
Import packages, functions, accessing files in system, app hooks etc

app code, we can controll fully using python

### Que: Give 2 scenarios where Server Scripts are acceptable, and 2 where you should insist on app code instead

### Ans:
* Server scripts are acceptable in small conditions, buisness rules configure quickly without deploying app code
* Simple data fetch, field updates, validations

App code,
* If we want full control over the files will use app code
* If we want to import libraries, do complex buisness logics, integrations, proper version control etc

### Que: What is the governance/maintainability risk of Server Scripts?

### ans:
Server scripts are powerful as they allow buisness logic, to be added directly without touching the code, where the risk is it is not code based, it stores only in DB. Not tracked in Git.   

### M2 - Caching, Redis & Cache Invalidation
### Task A - What Frappe caches (bench console exploration):

bootinfo = data loaded when desk starts, frappe caches it doesn't rebuild every request

### Que: Run: frappe.cache.get_value("bootinfo") - what does it contain?

frappe.cache().get_keys("*boot*")/ frappe.cache().redis_client.keys("*boot*")
=> to get keys actually exist in site

out: [b'_38dc3d6fcdc6ed6c|bootinfo']

### Ans:
bootinfo contains the data required to initialize the frappe desk when user logs in.
It includes info, permisssions, defaults etc

### Que: Run: frappe.cache.get_value("quickfix:translations") or similar - find where translations are cached

### Ans:
In [6]: frappe.cache().get_keys("*translation*")
out:
[b'_38dc3d6fcdc6ed6c|merged_translations',
 b'_38dc3d6fcdc6ed6c|lang_user_translations']

### Que: Run frappe.clear_cache() and observe what changes in the browser

### Ans:
clears frappe's cached data from redis, 
user opens desk, frappe redis cached bootinfo, metadata, permissions etc

after, cache entries are removed, next request rebuilds them, stores them back in cache

### Que: Frappe caches in Redis (bootinfo, DocType metadata/meta, website context, translations, user permissions)

### Ans:
Frappe caches:
Boot info
Doctype Metadata
Translations
User Permissions
Website context

Inspected Redis cache using 
frape.cache().get_keys(), frappe.clear_cache() followed by browser refresh 

### Task C - Debugging stale UI:

### Que: After making a JS change, the browser shows old JS. Explain: what command clears the asset cache? What role does bench build --app quickfix play?

### Ans: