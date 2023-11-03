from flask import Blueprint, request, jsonify
from models.account import AccountInformation
from models.customer import CustomerInformation
from models.automatic_payment import AutomaticPayments
from models import db
from helpers.middleware import is_authenticated, account_owner
from helpers.helpers import create_automatic_payment_entry, delete_automatic_payment_entry, create_transaction_history_entry
from decimal import Decimal
from datetime import datetime
import pandas
import pytz

automaticPayment = Blueprint('automatic_payment', __name__)


# setting up automatic payment
# note: flask can't take datetime representation of date, so needs to be
# converted to datetime from string
# pandas parses datetime from string in format YYYY-MM-DD
@automaticPayment.route('/automaticPayment/<int:account_id>/<float:amount>/<string:date>',
                        methods=['PATCH'])
@is_authenticated
@account_owner
def automatic_payment(account_id, amount, date):

    account = AccountInformation.query.get(account_id)
    if not account:
        return f'Bank Account with account_id {account_id} not found', 404
    if account.status == 'I':
        return (f'Bank Account with account_id {account_id} is inactive',
                404)

    # check valid amount
    if Decimal(amount) <= 0:
        return f'Payment amount must be positive', 404
    elif Decimal(amount) > account.balance:
        return f'Payment may not exceed balance', 404

    # take datetime
    date_time = pandas.to_datetime(date).to_pydatetime()

    # take timezone & create local time
    local_date = date_time.astimezone()

    # convert local time to utc for storage
    utc_date = local_date.astimezone(pytz.utc)

    # check that date is in future
    if utc_date < datetime.now().astimezone(pytz.utc):
        return f'Date must not be in past', 404

    if request.method == 'PATCH':
        create_automatic_payment_entry(account.customer_id, account_id,
                                       Decimal(amount), utc_date)
        return (f'Payment of ${Decimal(amount)} successfully scheduled for Bank '
                f'Account with account_id {account_id} and date {date}')


@automaticPayment.route('/cancelAutomaticPayment/<int:payment_id>', methods=['PATCH'])
@is_authenticated
def cancel_automatic_payment(payment_id):
    customer_id = request.currentUser
    payment = AutomaticPayments.query.filter(
        AutomaticPayments.payment_id == payment_id,
        AutomaticPayments.customer_id == customer_id
    ).first()

    if payment:
        db.session.delete(payment)  # Delete the record
        db.session.commit()  # Commit the transaction
        return jsonify(message=f'Automatic payment with the payment id: {payment_id} was successfully cancelled'), 200
    else:
        return jsonify(message=f'No automatic payment with the payment id: {payment_id} was found.'), 404


# upcoming automatic payments
@automaticPayment.route('/getUpcomingPayments/<int:number>', methods=['GET'])
@is_authenticated
def get_upcoming_payments(number):
    customer_id = request.currentUser
    if number < 0:
        return f'Query number must be positive', 404
    customer = CustomerInformation.query.get(customer_id)
    if not customer:
        return (f'Customer Account with customer_id {customer_id} not found',
                404)
    if customer.status == 'I':
        return (f'Customer Account with customer_id {customer_id} is '
                f'inactive', 404)
    if request.method == 'GET':
        upcoming = []
        if number == 0:
            upcoming = (AutomaticPayments.query.filter
                        (AutomaticPayments.customer_id == customer_id))
        else:
            upcoming = (AutomaticPayments.query.filter
                        (AutomaticPayments.customer_id == customer_id)).limit(
                number)
        upcoming_payments = []
        for payment in upcoming:
            upcoming_payments.append(payment.serialize())
        return jsonify(upcoming_payments)
