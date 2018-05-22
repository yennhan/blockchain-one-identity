#Leow Yenn Han
#leowyennhan@gmail.com

from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint

app = Flask(__name__)
Bootstrap(app)

company= Blueprint('company',__name__)

company_url="http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/company?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2"
token ='?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2'


@company.route('/company_homepage',methods=['GET','POST'])
def company_homepage():
    the_url = company_url
    get_company = requests.get(the_url)
    the_list = get_company.json()
    return render_template('company_dashboard.html',data=the_list)

@company.route('/add_company',methods=['GET','POST'])
def add_company():
    if request.method == 'POST':
        the_company_name= request.form.get('company_name')
        company_category=request.form.get('company_category')
        employee_id = request.form.get('employee_id')
        employee_id = "resource:org.acme.model.owner#"+employee_id
        data={}
        the_url = company_url
        get_company = requests.get(the_url)
        the_list = get_company.json()
        data['companyID'] = "company"+str(len(the_list))
        data['company_name']=the_company_name
        data['employee_in_this_company_ID']=[]
        data['employee_in_this_company_ID'].append(employee_id)
        data['company_category']=[]
        data['company_category'].append(company_category)
        dump_data_to_blockchain_company(data)
        return company_homepage()
@company.route('/delete_company',methods=['GET','POST'])
def delete_company():
    if request.method=='POST':
        the_firm = request.form.get('company_ID')
        get_firm = requests.get(the_firm)
        the_list = get_firm.json()
        return '<h1>The owner list valid is</h1>'+str(the_list)

def dump_data_to_blockchain_company(data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(company_url, json=data, headers=headers)
    pprint.pprint(response.json())