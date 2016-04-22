from flask import Flask, url_for, redirect, request, jsonify

app = Flask(__name__)

import paypalrestsdk

#Configure the REST SDK
paypalrestsdk.configure({
	"mode": "sandbox",
	"client_id": "AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd",
	"client_secret":"EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX"
	});


@app.route("/")
def index():
	return """
	<a href="%s">Pay with paypal</a>
	""" % (url_for('paypal_approval'))

@app.route("/paypal/approve")
def paypal_approval():
	payment = paypalrestsdk.Payment({
		"intent": "sale",
		"payer": {
			"payment_method": "paypal"
		},
		"transactions": [
			{
				"amount": {
					"total": "12",
					"currency": "USD"
				},
				"description": "Creating a payment"
			}
		],
		"redirect_urls": {
			"return_url": url_for('paypal_return', _external=True),
			"cancel_url": url_for('paypal_cancel', _external=True) 
		}
	})
	payment_result = payment.create()
	#Check if not successful
	if not payment_result:
		return paypal_generate_failed_template(payment.error)
	return """
		Was successful: %s
		<a href="%s">Click here for approval</a>
		%s
	""" % (payment_result, [x.href for x in payment.links if x.rel=='approval_url'][0], payment)

@app.route("/paypal/return")
def paypal_return():
	#Process payment variables and actually make charge here
	payment_id = request.args.get('paymentId')
	payer_id = request.args.get('PayerID')

	payment_to_execute = paypalrestsdk.Payment.find(payment_id)
	payment_to_execute.execute({ "payer_id": payer_id })
	return """
		Your payment was successful and should have gone through!
	"""

@app.route("/paypal/cancel")
def paypal_cancel():
	return """
		Your payment was cancelled!
	"""

def paypal_generate_failed_template(error_object):
	return """
		Your payment was not successful. See below for the stack trace.
		%s
	""" % (error_object)



if __name__ == '__main__': 
    app.run(host='127.0.0.1', port=8338, debug=True)