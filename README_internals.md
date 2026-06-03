

F3 - Asset, Jinja & Website Hooks

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
