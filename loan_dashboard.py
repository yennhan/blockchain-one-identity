#Leow Yenn Han
#leowyennhan@gmail.com

from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint

app = Flask(__name__)
Bootstrap(app)

loan_agreement="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/LoanAgreement"
token ='?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2'

loan= Blueprint('loan',__name__)
'''
{
    "$class": "org.acme.model.LoanAgreement",
    "loan_id": "loan_owner3",
    "owner": "resource:org.acme.model.owner#owner3",
    "bank": "resource:org.acme.model.Bank#bank2",
    "the_approval": "Yes",
    "loan_term": 30,
    "loan_amount": 30000,
    "interest_rate": 4.5,
    "blr_rate": 4,
    "lock_in_period_in_year": 5,
    "penalty": 0,
    "rgbt": ".",
    "flexi_loan": "YES"
}
'''

@loan.route('/loan_agreement_dashboard',methods=['GET','POST'])
def loan_dashboard():
    the_url = loan_agreement+token
    get_loan = requests.get(the_url)
    the_list = get_loan.json()
    return render_template('loan_agreement.html', data=the_list)