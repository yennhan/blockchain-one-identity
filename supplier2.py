from flask import *
from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint
from receipt_generator import *
from smart_contract_case_study_2 import *
from invoice_generator import *
from stocks import *
from receipt_generator import *
app = Flask(__name__)
Bootstrap(app)
supplier2 = Blueprint('supplier2',__name__)


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
invoice_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/invoice"
#meat supplier

@supplier2.route('/supplier2_homepage',methods=['GET','POST'])
def supplier_homepage():
    data_invoice = []
    request_restock = request_stock_url + "/" + token
    get_restock = requests.get(request_restock)
    the_restock = get_restock.json()
    for i in range(len(the_restock)):
        if (the_restock[i]['supplierID'] == "resource:org.acme.model.supplier#supplier2") and (
                the_restock[i]['restock_status'] == "Required_restock"):
            data_invoice.append(the_restock[i])
    return render_template('supplier2_dashboard.html', invoice=data_invoice)


@supplier2.route('/adding_invoice_supplier2',methods=['GET','POST'])
def adding_invoice_supplier2():
    data_invoice=[]
    request_restock = request_stock_url + "/" + token
    get_restock = requests.get(request_restock)
    the_restock = get_restock.json()
    for i in range(len(the_restock)):
        if (the_restock[i]['supplierID']=="resource:org.acme.model.supplier#supplier2") and (the_restock[i]['restock_status']=="Required_restock"):
            data_invoice.append(the_restock[i])
    return render_template('supplier2_dashboard.html', invoice=data_invoice)

@supplier2.route('/issue_invoice2',methods=['GET','POST'])
def issue_invoice2():
    if request.method == 'POST':
        invoice_id = request.form.get('issue_invoice')
        invoice_id = invoice_id.replace("resource:org.acme.model.stock#","")
        restock_id = request.form.get('request_stock_id')
        restock_id = restock_id.replace("resource:org.acme.model.request_stock#","")
        get_expenses = requests.get(stock_url +"/"+invoice_id+ token)
        the_list = get_expenses.json()
        invoice_id = "invoice_"+restock_id
        company_name="Kaishen"
        company_address="Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
        purchaser="Jibby & Co"
        time1=time.asctime( time.localtime(time.time()))
        the_items=[]
        data={}
        data['qty']=int((the_list['stock_balance'])*1.5)
        data['description_of_item']=the_list['item_name']
        data['unit_price']=the_list['price_per_unit']
        data['amount'] = data['qty']*data['unit_price']
        the_items.append(data)
        logo_im='kaishen.png'
        invoice_pdf_generator(logo_im,invoice_id, company_name, company_address, purchaser, time1, the_items)
        s3_setup(invoice_id + ".pdf")
        silentremove(invoice_id + ".pdf")
        return adding_invoice_supplier2()

@supplier2.route('/purchased',methods=['GET','POST'])
def purchased_supplier2(stock_id,request_stock_id):
    get_expenses = requests.get(stock_url +'/'+ stock_id + token)
    the_list = get_expenses.json()
    the_list['stock_balance']=int((the_list['standard_level']*1.5))
    item = {}
    item['qty'] =int((the_list['standard_level']*1.5))
    item['description_of_item'] = the_list['item_name']
    item['unit_price'] = the_list['price_per_unit']
    item['amount'] = item['qty'] * item['unit_price']
    update_data_stock(stock_id,the_list)
    get_2 = requests.get(request_stock_url + '/' + request_stock_id + token)
    the_list2 = get_2.json()
    the_list2['restock_status']="Completed"
    update_data_status(request_stock_id,the_list2)
    logo_im = 'kaishen.png'
    company_name = "Kaishen"
    company_address = "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
    purchaser = "Jibby & Co"
    account_id=""
    company_claim=""
    the_data=[]
    the_data.append(item)
    time1 = time.asctime(time.localtime(time.time()))
    receipt_first = requests.get(receipt_url + token)
    the_receipt_id = receipt_first.json()
    receipt_id="stock_receiptb_"+str(len(the_receipt_id))
    receipt = {}
    receipt['receiptID'] = receipt_id
    receipt['total_price'] = item['amount']
    receipt['companyID'] = "resource:org.acme.model.company#company20"
    receipt['total_cost'] = 0
    dumb_data_to_receipt_asset(receipt)
    a = receipt_id.split("b", 1)
    receipt_pdf_generator(logo_im, receipt_id, company_name, company_address, purchaser, time1, the_data, account_id,company_claim)
    s3_setup(receipt_id + ".pdf")
    silentremove(receipt_id + ".pdf")

def dumb_data_to_receipt_asset(data):
    headers = {'Content-type': 'application/json'}
    receipt_post=receipt_url+token
    response = requests.post(receipt_post, json=data, headers=headers)

def update_data_status(id,data):
    headers={'Content-type': 'application/json'}
    stock_post = request_stock_url + "/" + id + token
    response = requests.put(stock_post, json=data, headers=headers)

def update_data_stock(stock_id, data):
    headers = {'Content-type': 'application/json'}
    stock_post = stock_url +"/"+ stock_id + token
    response = requests.put(stock_post, json=data, headers=headers)

