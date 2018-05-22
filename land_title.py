from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
import requests
from s3_run import *



token ='?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2'

app = Flask(__name__)
Bootstrap(app)
land= Blueprint('land_title',__name__)


land_title_link = "http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/LandTitle?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2"

@land.route('/land_title',methods=['GET','POST'])
def land_title():
    get_bank = requests.get(land_title_link)
    the_list=get_bank.json()
    return render_template('land_title.html',data=the_list)

@land.route('/add_land',methods=['GET','POST'])
def add_land():
    if request.method=='POST':
        get_bank = requests.get(land_title_link)
        the_list = get_bank.json()
        the_owner = request.form.get('owner_id')
        owner_exist = "http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/owner/"+str(the_owner)+token
        r= requests.get(owner_exist)
        not_exist="Owner don't exist"
        if r.status_code == 404:
            return render_template('land_title.html',data=the_list,exist=not_exist)
        land_id = request.form.get('land_id')
        lot_no = request.form.get('lot_no')
        size_meter = request.form.get('size_meter')
        lembaran_piawai = request.form.get('lembaran_piawai')
        negeri = request.form.get('negeri')
        daerah = request.form.get('daerah')
        location_type = request.form.get('location')
        tanah = request.form.get('tanah')
        get_bank = requests.get(land_title_link)
        the_list = get_bank.json()
        return render_template('land_title.html', data=the_list)