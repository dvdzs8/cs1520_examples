# Building a client web app

Refer to the the example `fl11_api`. Modify `api_ex.py` to serve a client web
app on the `/` route. This web app should support the following functionality:

* Display all of the Todo items
* Provide a button to delete any Todo item
* Use `fetch` to poll for Todos from the server every 10s
* Provide a form for the user to enter new Todo items
* Use `fetch` to send these new Todo items to the server

We demo'd a React version of this app in lecture (sans delete). You should build
your web app as a single HTML template and JS script file(s). You should also
use `async` and `await` with your fetch calls instead of a chain of `.then()`
calls.
