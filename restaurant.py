from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint
from receipt_generator import *
app = Flask(__name__)
Bootstrap(app)
restaurant = Blueprint('restaurant',__name__)


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

#add receipt and claims
@restaurant.route('/restaurant_one',methods=['GET','POST'])
def the_one_claiming():
    item=[]
    data={}
    get_expenses = requests.get(claim_expenses_url)
    receipt=requests.get(receipt_url+token)
    the_receipt1=receipt.json()
    the_list = get_expenses.json()
    if request.method == 'POST':
        chick_breakie = request.form.get('chick_breakie')
        jibby_big_breakfast= request.form.get("big_breakfast")
        casa_egg = request.form.get("casablanca_egg")
        trio_drips=request.form.get('trio_drips')
        para_break=request.form.get("paradise_breakie")
        cala_salad=request.form.get("calamari_salad")
        rib_eye=request.form.get("rib_eye_steak")
        beef_ribs=request.form.get("sticky_bbq_beef_ribs")
        salmon_russian=request.form.get("salmon_russian")
        if chick_breakie!='':
            data["qty"]=int(chick_breakie)
            data["unit_price"]=30
            data['description_of_item']="Chick Breakie"
            data['amount']= 30*int(chick_breakie)
            item.append(data)
            data={}
        if jibby_big_breakfast!="":
            data["qty"]=int(jibby_big_breakfast)
            data["unit_price"]=31
            data['description_of_item']="Jibby Big Breakfast"
            data['amount']=31*int(jibby_big_breakfast)
            item.append(data)
            data = {}
        if casa_egg!="":
            data["qty"] = int(casa_egg)
            data["unit_price"] = 28
            data['description_of_item'] = "Casabalanca Egg"
            data['amount'] = 28 * int(casa_egg)
            item.append(data)
            data = {}
        if trio_drips!="":
            data["qty"] = int(trio_drips)
            data["unit_price"] = 22
            data['description_of_item'] = "Jibby Trio Drips"
            data['amount'] = 22 * int(trio_drips)
            item.append(data)
            data = {}
        if para_break != "":
            data["qty"] = int(para_break)
            data["unit_price"] = 25
            data['description_of_item'] = "Paradise Breakie"
            data['amount'] = 25 * int(para_break)
            item.append(data)
            data = {}
        if cala_salad != "":
            data["qty"] = int(cala_salad)
            data["unit_price"] = 22
            data['description_of_item'] = "Crispy Calamari Salad"
            data['amount'] = 22 * int(cala_salad)
            item.append(data)
            data = {}
        if rib_eye != "":
            data["qty"] = int(rib_eye)
            data["unit_price"] = 72
            data['description_of_item'] = "300g Chilled Australian Rib Eye Steak"
            data['amount'] = 72 * int(rib_eye)
            item.append(data)
            data = {}
        if beef_ribs != "":
            data["qty"] = int(beef_ribs)
            data["unit_price"] = 65
            data['description_of_item'] = "Sticky BBQ Beef Ribs"
            data['amount'] = 65 * int(beef_ribs)
            item.append(data)
            data = {}
        if salmon_russian != "":
            data["qty"] = int(salmon_russian)
            data["unit_price"] = 23
            data['description_of_item'] = "Salmon Russian"
            data['amount'] = 23 * int(salmon_russian)
            item.append(data)
            data = {}
        claim_id=request.form.get("claim_id")
        if claim_id!="":
            get_expenses = requests.get(claim_url+claim_id+token)
            the_list = get_expenses.json()
            company=the_list['companyID']
            company = company.replace('resource:org.acme.model.company#','')
            get_company = requests.get(company_url+company+token)
            the_companies=get_company.json()
            company_claim=the_companies['company_name']
            owner=the_list['ownerID']
            the_new_word=owner.replace('resource:org.acme.model.owner#',"")
            new_id=requests.get(owner_post+the_new_word+token)
            the_list2=new_id.json()
            full_name=the_list2['firstName']+" "+the_list2['lastName']
            receipt_first=requests.get(receipt_url+token)
            the_receipt_id=receipt_first.json()
            data_value1=0
            for things in item:
                a=things['amount']
                data_value1+=a
            receipt={}
            receipt['receiptID']= "receipt_"+str(len(the_receipt_id))
            receipt['total_price']=data_value1
            receipt['companyID']="resource:org.acme.model.company#company13"
            receipt['total_cost'] = 0
            receipt['claim_tax_or_claim_company']='company_expenses'
            time1=time.asctime( time.localtime(time.time()))
            company_name='Jibby & Co'
            company_address= "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
            receipt_id=receipt['receiptID']
            logo="jibby.png"
            dumb_data_to_receipt_asset(receipt)
            claim_company_expenses(claim_id,receipt_id)
            receipt_pdf_generator(logo,receipt_id, company_name, company_address, full_name, time1, item, claim_id,company_claim)
            s3_setup(receipt_id + ".pdf")
            silentremove(receipt_id + ".pdf")
            update_claim(claim_id,data_value1)
            return rest_homepage()
        else:
            receipt_first = requests.get(receipt_url + token)
            the_receipt_id = receipt_first.json()
            data_value1 = 0
            for things in item:
                a = things['amount']
                data_value1 += a
            receipt = {}
            receipt['receiptID'] = "receipt_" + "company13_" + str(len(the_receipt_id))
            receipt['total_price'] = data_value1
            receipt['companyID'] = "resource:org.acme.model.company#company13"
            receipt['total_cost']=0
            receipt['claim_tax_or_claim_company'] = 'company_expenses'
            time1 = time.asctime(time.localtime(time.time()))
            company_name = 'Jibby & Co'
            company_address = "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
            receipt_id = receipt['receiptID']
            logo = "jibby.png"
            dumb_data_to_receipt_asset(receipt)
            claim_id = ""
            full_name = ""
            company_claim = ""
            receipt_pdf_generator(logo,receipt_id, company_name, company_address, full_name, time1, item, claim_id,
                                  company_claim)
            s3_setup(receipt_id + ".pdf")
            silentremove(receipt_id + ".pdf")
            return rest_homepage()
        return rest_homepage()
    return rest_homepage()

@restaurant.route('/restaurant_homepage',methods=['GET','POST'])
def rest_homepage():
    get_expenses = requests.get(claim_expenses_url)
    receipt = requests.get(receipt_url + token)
    the_receipt1 = receipt.json()
    the_list = get_expenses.json()
    return render_template('restaurant.html', restaurant_data=the_receipt1, pdf_reader=pdf_reader_link)

def update_claim(claim_id,total_cost):
    claim2 = claim_url +claim_id+ token
    get_claim = requests.get(claim2)
    the_list = get_claim.json()
    value=the_list['claim_limit']
    the_list['claim_limit']=value-total_cost
    update_data(claim_id,the_list)


def claim_company_expenses(claim_id,receipt_id):
    data1={}
    data1['claimID']="resource:org.acme.model.company_claim#"+claim_id
    data1['receiptID']="resource:org.acme.model.receipt#"+receipt_id
    data1['claim_date_time']=time.asctime( time.localtime(time.time()))
    dumb_data_to_claim_transaction(data1)

def update_data(claim_id,data):
    headers = {'Content-type': 'application/json'}
    claim_post = claim_url +claim_id+ token
    response=requests.put(claim_post,json=data,headers=headers)


def dumb_data_to_claim_transaction(data1):
    headers = {'Content-type': 'application/json'}
    claim_post1=claim_expenses_url+token
    response = requests.post(claim_post1, json=data1, headers=headers)


def dumb_data_to_receipt_asset(data):
    headers = {'Content-type': 'application/json'}
    receipt_post=receipt_url+token
    response = requests.post(receipt_post, json=data, headers=headers)

