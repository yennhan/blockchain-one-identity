from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint

app = Flask(__name__)
Bootstrap(app)
claim = Blueprint('claim',__name__)
company_claim1 = "http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/company_claim"
expenses_transaction_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/claim_company_expenses"
token = "?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2"
pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"

@claim.route('/company_claim',methods=['POST','GET'])
def company_claim():
    claim2=company_claim1+token
    get_expenses = requests.get(claim2)
    the_list = get_expenses.json()
    expense=expenses_transaction_url+token
    get_exp_receipt=requests.get(expense)
    the_list2=get_exp_receipt.json()
    return render_template('company_claim.html',data=the_list,transactions=the_list2,pdf_reader=pdf_reader_link)

@claim.route('/register_company',methods=['POST','GET'])
def register_claim_company():
    if request.method == 'POST':
        global employee_claim_id, company_id, claim_person_id, claim_limit
        employee_claim_id=request.form.get('employee_claim_id')
        company_id = "company18"
        claim_person_id= request.form.get('claim_person_id')
        claim_limit = request.form.get('claim_limit')
        claim1 = company_claim1+token              #company18 - Exxon Mobile
        data={}
        data['employee_claimID'] = employee_claim_id
        data['companyID'] = "resource:org.acme.model.company#" + company_id
        data['ownerID'] = "resource:org.acme.model.owner#" + claim_person_id
        data['from_companyID'] = "resource:org.acme.model.company#" + company_id
        data['claim_limit'] = int(claim_limit)
        dumb_data_to_claim_asset(data)
        get_expenses = requests.get(claim1)
        the_list = get_expenses.json()
        return render_template('company_claim.html',data=the_list,pdf_reader=pdf_reader_link)


def dumb_data_to_claim_asset(data):
    headers = {'Content-type': 'application/json'}
    claim_post= company_claim1+token
    response = requests.post(claim_post, json=data, headers=headers)
    pprint.pprint(response.json())


