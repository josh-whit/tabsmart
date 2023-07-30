from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


def calc_total_bill(orders, tax_percent, tip_percent):
    """Calculates the total bill, taking orders (dict) and tax and tip (floats)
    as params and returning the total bill (float)"""
    total_amount = sum(orders.values())
    tax_amount = total_amount * (tax_percent / 100)
    tip_amount = total_amount * (tip_percent / 100)
    total_bill = total_amount + tax_amount + tip_amount
    return total_bill


def calc_individual_shares(orders, tax_percent, tip_percent):
    """Calculates each diner's share of the bill.
    Takes orders (dict), tax and tip (float) as params.
    Returns dict with diners as keys (str) and their share of the bill as value (float)"""
    total_bill = calc_total_bill(orders, tax_percent, tip_percent)
    individual_shares = {}
    total_order_value = sum(orders.values())

    for diner, order_value in orders.items():
        diner_share = (order_value / total_order_value) * total_bill
        individual_shares[diner] = diner_share

    return individual_shares


def main():
    num_diners = int(input("Enter the number in your party: "))
    orders = {}

    for i in range(num_diners):
        diner_name = input(f"Enter name {i + 1}: ")
        order_amount = input(f"Enter the order amounts for {diner_name} (separated by commas): ")
        order_values = [float(amount.strip()) for amount in order_amount.replace(",", " ").split()]
        orders[diner_name] = (sum(order_values))

    tax_percent = float(input(f"Enter the % tax (e.g. 8.5): "))
    tip_percent = float(input(f"Enter the % tip (e.g. 20): "))

    individual_shares = calc_individual_shares(orders, tax_percent, tip_percent)
    total_bill = calc_total_bill(orders, tax_percent, tip_percent)
    total_amount = sum(orders.values())
    tip_amount = total_amount * (tip_percent / 100)

    print(f"\nTip ({tip_percent}%): ${tip_amount:.2f}")
    print(f"Total bill: ${total_bill:.2f}")
    for diner, share in individual_shares.items():
        print(f"{diner} owes: ${share:.2f}")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'


# Route to handle party size form
@app.route('/', methods=['GET', 'POST'])
def index():
    class PartySizeForm(FlaskForm):
        num_diners = FloatField('Enter party size:', validators=[DataRequired()])
        submit = SubmitField('Next')

    form = PartySizeForm()
    if form.validate_on_submit():
        session['num_diners'] = int(form.num_diners.data)
        return redirect(url_for('get_names'))
    return render_template('index.html', form=form)


# Route to handle getting names of diners
@app.route('/get_names', methods=['GET', 'POST'])
def get_names():
    DinerNamesForm = type('DinerNamesForm', (FlaskForm,), {'submit': SubmitField('Next')})
    for i in range(session.get('num_diners')):
        setattr(DinerNamesForm, f'diner_{i + 1}', StringField(f'Name {i + 1}:', validators=[DataRequired()]))
    form = DinerNamesForm()
    if form.validate_on_submit():
        session['diner_names'] = {f"diner_{i + 1}": getattr(form, f"diner_{i + 1}").data for i in
                                  range(session.get('num_diners'))}
        return redirect(url_for('get_orders'))
    return render_template('names.html', form=form)


# Route to handle getting orders for each diner
@app.route('/get_orders', methods=['GET', 'POST'])
def get_orders():
    OrdersForm = type('OrdersForm', (FlaskForm,), {'submit': SubmitField('Next')})

    for i in range(session.get('num_diners')):
        diner_name = session["diner_names"][f"diner_{i + 1}"]
        setattr(OrdersForm, f'order_{i + 1}',
                FloatField(f'Enter order for {diner_name}:', validators=[DataRequired()]))

    form = OrdersForm()

    if form.validate_on_submit():
        session['orders'] = {session["diner_names"][f"diner_{i + 1}"]: getattr(form, f'order_{i + 1}').data for i in
                             range(session.get('num_diners'))}
        return redirect(url_for('get_tax_tip'))

    return render_template('orders.html', form=form)


# Route to handle getting tax and tip percentage
@app.route('/get_tax_tip', methods=['GET', 'POST'])
def get_tax_tip():
    class TaxTipForm(FlaskForm):
        tax_percent = FloatField('Enter the % tax (e.g. 8.5):', validators=[DataRequired()])
        tip_percent = FloatField('Enter the % tip (e.g. 20):', validators=[DataRequired()])
        submit = SubmitField('Next')

    form = TaxTipForm()
    if form.validate_on_submit():
        session['tax_percent'] = form.tax_percent.data
        session['tip_percent'] = form.tip_percent.data
        return redirect(url_for('show_result'))
    return render_template('tax_tip.html', form=form)


# Route to show the final result
@app.route('/show_result', methods=['GET', 'POST'])
def show_result():
    total_amount = sum(session['orders'].values())
    tax_amount = total_amount * (session['tax_percent'] / 100)
    tip_amount = total_amount * (session['tip_percent'] / 100)
    total_bill = total_amount + tax_amount + tip_amount
    individual_shares = {}
    total_order_value = sum(session['orders'].values())
    for diner, order_value in session['orders'].items():
        diner_share = (order_value / total_order_value) * total_bill
        individual_shares[diner] = diner_share

    return render_template('result.html', tax_percent=session['tax_percent'], tax_amount=tax_amount,
                           tip_percent=session['tip_percent'], tip_amount=tip_amount,
                           total_bill=total_bill, individual_shares=individual_shares)


if __name__ == "__main__":
    app.run(debug=True)
