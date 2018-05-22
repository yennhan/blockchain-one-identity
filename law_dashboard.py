#Leow Yenn Han
#leowyennhan@gmail.com

from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint


app = Flask(__name__)
Bootstrap(app)

law_dashboard= Blueprint('law',__name__)

law_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/Lawyer?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2"
token ='6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2'
"""
"$class": "org.acme.model.Lawyer",
    "lawfirmID": "lawfirm0",
    "lawyer_firm_id": "resource:org.acme.model.company#company20",
    "lawyer_id": "Rahayu_Partnership_lawyer_0",
    "company_lawyer_name": "Rahayu_Partnership"
"""

@law_dashboard.route('/law_homepage',methods=['GET','POST'])
def law_homepage():
    the_url = law_url
    get_law = requests.get(the_url)
    the_list = get_law.json()
    return render_template('law_dashboard.html',data=the_list)

@law_dashboard.route('/law_add_firm',methods=['GET','POST'])
def law_add_firm():
    if request.method == 'POST':
        the_firm = request.form.get('delete_id')
        get_firm = requests.get(the_firm)
        the_list = get_firm.json()
        return '<h1>The law firm list valid is</h1>' + str(the_list)

@law_dashboard.route('/delete_firm',methods=['GET','POST'])
def delete_firm():
    if request.method=='POST':
        the_firm = request.form.get('lawfirm_id')
        get_firm = requests.get(the_firm)
        the_list = get_firm.json()
        return '<h1>The owner list valid is</h1>'+str(the_list)

