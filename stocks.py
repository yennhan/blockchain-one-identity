from flask import Flask, Blueprint, render_template
from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint
from receipt_generator import *
from smart_contract_case_study_2 import *
from supplier2 import *
from supplier1 import *
app = Flask(__name__)
Bootstrap(app)
stocks = Blueprint('stocks',__name__)


company_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/company/"
bank_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/Bank/"
owner_post='http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/owner/'
bank_loan_transaction= "http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/bank_loan_approval/"
land_title_link = "http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/LandTitle/"
loan_agreement= "http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/LoanAgreement/"
trade_house="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/TradeHouse/"
claim_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/company_claim/"
claim_expenses_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/claim_company_expenses"
token ='?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2'
receipt_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/receipt"
pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"
stock_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/stock"
request_stock_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/request_stock"

@stocks.route('/home_stocks',methods=['GET','POST'])
def stock_homepage():
    get_expenses = requests.get(stock_url+token)
    the_list = get_expenses.json()
    data_invoice = []
    request_restock = request_stock_url + "/" + token
    get_restock = requests.get(request_restock)
    the_restock = get_restock.json()
    for i in range(len(the_restock)):
        if the_restock[i]['restock_status'] == "Required_restock":
            data_invoice.append(the_restock[i])
    pprint.pprint(data_invoice)
    receipt_first = requests.get(receipt_url + token)
    the_receipt_id = receipt_first.json()
    data_receipt=[]
    for i in range(len(the_receipt_id)):
        word=(the_receipt_id[i]['receiptID'].split("b",1))
        if word[0]=="stock_receipt":
            data_receipt.append(the_receipt_id[i])
    return render_template('stocks.html',data=the_list,restock=data_invoice,pdf_reader=pdf_reader_link,receipts=data_receipt)

@stocks.route('/add_stocks',methods=['GET','POST'])
def add_stock():
    if request.method == 'POST':
        item_name=request.form.get('item_name')
        item_balance=request.form.get('stock_balance')
        item_standard=request.form.get('standard_level')
        item_price_per_unit=request.form.get('price_per_unit')
        company_name="resource:org.acme.model.company#company13"
        get_expenses = requests.get(stock_url + token)
        the_list = get_expenses.json()
        data1={}
        data1['stockID']="stock_"+str(len(the_list)+1)+"_company13"
        data1['companyID']=company_name
        data1['item_name']=item_name
        data1['stock_balance']=item_balance
        data1['standard_level']=item_standard
        data1['price_per_unit']=item_price_per_unit
        dump_data_to_stock(data1)
        return stock_homepage()

@stocks.route('/purchase_confirm',methods=['GET','POST'])
def purchase_stock():
    if request.method == 'POST':
        stock_id= request.form.get('stockid')
        stock_id=stock_id.replace("resource:org.acme.model.stock#","")
        supplier_id = request.form.get('supplier_id')
        supplier_id = supplier_id.replace("resource:org.acme.model.supplier#","")
        requeststock_id= request.form.get('requeststock_id')
        requeststock_id=requeststock_id.replace("resource:org.acme.model.request_stock#","")
        if supplier_id=="supplier2":
            purchased_supplier2(stock_id,requeststock_id)
        else:
            purchased_supplier1(stock_id,requeststock_id)
    return redirect(url_for('stocks.stock_homepage'))

@stocks.route('/delete_stocks',methods=['GET','POST'])
def delete_stock():
    if request.method == 'POST':
        item_id = request.form.get('delete_id')
        headers = {'Content-type': 'application/json'}
        claim_post = stock_url +'/'+item_id+ token
        response = requests.delete(claim_post,headers=headers)
        return stock_homepage()

def dump_data_to_stock(data):
    headers = {'Content-type': 'application/json'}
    claim_post = stock_url + token
    response = requests.post(claim_post, json=data, headers=headers)