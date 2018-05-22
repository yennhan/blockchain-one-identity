#Leow Yenn Han
#leowyennhan@gmail.com
from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint


app = Flask(__name__)
Bootstrap(app)

banks= Blueprint('banks',__name__)

bank_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/Bank?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2"
token =' ?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2'


@banks.route('/bank_homepage',methods=['GET','POST'])
def bank_homepage():
    the_url = bank_url
    get_bank = requests.get(the_url)
    the_list = get_bank.json()
    return render_template('bank.html',data=the_list)

