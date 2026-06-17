### Quickfix

App for Service center

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit

### A2 - Multi-Site & Configuration

### Que: explain in 4 sentences: what each config file is for, and what breaks if you accidentally put a secret in common_site_config.json

### Ans:
common_site_config:
* Configurations affects commonly to all the sites available in that bench
* Does/Should not contain/add important information 

site config:
* Configurations affects specifically only to that site
* Will store db infos etc as it is site specific

if we put anything in common site config it shows to all and any can mis use it, so any important info eg: pwd etc store site specific


### Que: list the 4 processes bench start launches (web, worker, scheduler, socketio) and explain what happens to background jobs if the worker process crashes.

### Ans:
redis(cache/queue)
web
socketio
worker

If worker gets crashed jobs will get queue when the worker resumes bg job will gets started

### B1 - Trace a Request End-to-End

### Step 1 - Routing
### Que: When a browser hits /api/method/quickfix.api.get_job_summary - what Python function handles this request and how does Frappe find it?

### Ans:
when browser hits the url, this will call the function get_job_summary & this will handle the request, we will mention the path in the hooks file, so frappe checks first is hooks file and navigate to the path, and call that fn

### Que: When a browser hits /api/resource/Job Card/JC-2024-0001 - what happens differently compared to /api/method/?

### Ans:
this will use the inbuilt CRUD method

### Que: When a browser hits /track-job - which file/function handles it and why?

### Ans:
this will handle by web form/page, hooks file will handle and website_route_rules function will handle it

### Step 2 - Session & CSRF
### Que: Open your Frappe site in browser devtools. Find the X-Frappe-CSRF-Token in aPOST request.

### Ans: 

open doctype => enter details => save/submit => open dev tool
=> network => headers => request headers 

Eg: X-Frappe-CSRF-Token b3e88415c935b88df9060953c0b6576f8b065cb866dba041e942185f 

it comes from, server generation, client exposure, request interception

if we omit, frappe will reject request

### Que: In bench console, run: import frappe; frappe.session.data and describe what it contains

### Ans:
In [1]: import frappe

In [2]: frappe.session.user
Out[2]: 'Administrator'

It contains the current logged in user

### L1 - REST Resource API & Custom API
### Task B - Token Authentication
### Que: Explain in README: what is the difference between session cookie auth and token auth Which is appropriate for browser use and which for server-to-server?

### Ans:
* session cookie does not have more permission, only we can get the details already exist
* where token auth have more authorization where we can do all the methods(get, put, post, delete)

* for browser use session cookie and for server to server use token