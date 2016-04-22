#paypal-flask-demo

A demo repository that shows how easy it is to integrate PayPal's RESTful API with Python's Flask microframework.

Something like this exists for the `python-paypal` SOAP wrapper module [here](https://github.com/jdiez17/flask-paypal), but not for the `paypalrestsdk` RESTful API wrapper, which I preferred and is still actively supported by PayPal.

I spent the best part of a Friday mucking around with all of it, and I thought it'd be good to upload a concise version of how to get this done. 

Take particular note of:
- the url_for external URL argument
- how the SDK returns payment status (inside the original object)

Happy coding!
