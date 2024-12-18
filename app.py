from flask import Flask, render_template, redirect, request, jsonify
import stripe

app = Flask(__name__)

# Set your Stripe secret key
stripe.api_key = "sk_test_51QXOwlLwecxmSglFHD76yLuFj6IvkyuKksbaijIkDzFlRxPzUCX80YQP45zRJKtizB3QjUULzHb8H8fS5lrZBHRC00HGyqXcCN"  # Replace with your Stripe Secret Key

YOUR_DOMAIN = "http://localhost:5000"

@app.route('/')
def home():
    return render_template('GymRat.html')

@app.route('/membership')
def membership():
    return render_template('Membership.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Get the plan type from the form data
        plan = request.form.get('plan')  # Basic, Premium, or Elite

        # Map plan types to price IDs
        price_mapping = {
            "Basic": "price_1QXOzBLwecxmSglFQztesHlt",   # Replace with your actual Stripe price IDs
            "Premium": "price_1QXPNjLwecxmSglFAdBkCViE",
            "Elite": "price_1QXPOYLwecxmSglF0Hvkuw5v"
        }

        # Get the price ID based on the selected plan
        price_id = price_mapping.get(plan)

        if not price_id:
            return jsonify({"error": "Invalid plan selected"}), 400

        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',  # Use 'subscription' for recurring payments
            success_url=f"{YOUR_DOMAIN}/success",
            cancel_url=f"{YOUR_DOMAIN}/cancel",
        )

        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/success')
def success():
    return "<h1>Payment Successful</h1>"

@app.route('/cancel')
def cancel():
    return "<h1>Payment Cancelled</h1>"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
