from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint
owner_post='http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/owner?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2'
token =' ?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2'

app = Flask(__name__)
Bootstrap(app)
owner_port= Blueprint('owner_port',__name__)

@owner_port.route('/delete_owner',methods=['GET','POST'])
def delete_owner():
    if request.method=='POST':
        the_owner=request.form.get('delete_id')
        get_bank = requests.get(owner_post)
        the_list = get_bank.json()
        return '<h1>The owner list valid is</h1>'+str(the_owner)


@owner_port.route('/add_owner',methods=['GET','POST'])
def add_owner():
    if request.method=='POST':
        the_owner=request.form.get('owner_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        nric = request.form.get('nric')
        email = request.form.get('email')
        occupation = request.form.get('occupation')
        bank_balance = request.form.get('bank_balance')
        ccris = request.form.get('ccris')
        ctos = request.form.get('ctos')
        return '<h1>The owner list valid is</h1>'+str(the_owner)


@owner_port.route('/owner',methods=['GET','POST'])
def owner_homepage():
    get_bank = requests.get(owner_post)
    the_list = get_bank.json()
    return render_template('table_owner.html',data=the_list)

