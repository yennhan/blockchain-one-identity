from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint
from receipt_generator import *
from smart_contract_case_study_2 import *
from profit_loss_pdf import *
app = Flask(__name__)
Bootstrap(app)
restaurant2 = Blueprint('restaurant2',__name__)


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
@restaurant2.route('/restaurant_2',methods=['GET','POST'])
def home_page():
    receipt = requests.get(receipt_url + token)
    the_receipt1 = receipt.json()
    data_receipt=[]
    for i in range(len(the_receipt1)):
        word = (the_receipt1[i]['receiptID'].split("b", 1))
        if word[0] != "stock_receipt":
            data_receipt.append(the_receipt1[i])
    pdf_name="jibbyco.pdf"
    company_name="Jibby&Co"
    company_address = "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
    #get receipt revenue
    revenue=0
    for i in range(len(the_receipt1)):
        word = (the_receipt1[i]['receiptID'].split("b", 1))
        if word[0] != "stock_receipt":
            revenue+=int(the_receipt1[i]['total_price'])
    cost_of_goods=0
    for i in range(len(the_receipt1)):
        word = (the_receipt1[i]['receiptID'].split("b", 1))
        if word[0] == "stock_receipt":
            cost_of_goods+=int(the_receipt1[i]['total_price'])
    total_salary = 10000
    rental = 5000
    office_supply = 100
    insurance = 3000
    utilities = 1500
    maintanence = 700
    telecommunication = 300
    profit_loss_pdf(pdf_name,company_name, company_address, revenue, cost_of_goods, total_salary, rental, office_supply,insurance, utilities, maintanence, telecommunication)
    s3_setup(pdf_name)
    silentremove(pdf_name)
    return render_template('restaurant_2.html', restaurant_data=data_receipt, pdf_reader=pdf_reader_link,pl_statement=pdf_name)


@restaurant2.route('/restaurant2_claim',methods=['GET','POST'])
def the_one_claiming():
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
        calculate_cost(chick_breakie,jibby_big_breakfast,casa_egg,trio_drips,para_break,cala_salad,rib_eye,beef_ribs,salmon_russian)
        return home_page()
    return home_page()