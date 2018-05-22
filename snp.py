from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint

app = Flask(__name__)
Bootstrap(app)

tradehouse_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/TradeHouse"
bank_url = "http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/Bank/"
owner_post = 'http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/owner/'
token = '?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2'
bank_loan_transaction = "http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/bank_loan_approval/"
land_title_link = "http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/LandTitle/"
pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"


#register the blueprint
snp= Blueprint('snp',__name__)


@snp.route('/snp')
def transactions():
    return render_template('snp.html')

