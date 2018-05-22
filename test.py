from flask import Flask, Blueprint, render_template
from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint
from receipt_generator import *
from smart_contract_case_study_2 import *
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

a=[
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_0_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Apple",
    "stock_balance": 300,
    "standard_level": 200,
    "price_per_unit": 2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_10_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Bacon",
    "stock_balance": 500,
    "standard_level": 150,
    "price_per_unit": 4
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_11_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Lettuce",
    "stock_balance": 300,
    "standard_level": 150,
    "price_per_unit": 2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_12_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Flour",
    "stock_balance": 300,
    "standard_level": 150,
    "price_per_unit": 3.5
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_13_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Mushroom",
    "stock_balance": 250,
    "standard_level": 50,
    "price_per_unit": 2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_14_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Chicken thigh",
    "stock_balance": 200,
    "standard_level": 100,
    "price_per_unit": 8
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_15_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Sweet_sauce",
    "stock_balance": 500,
    "standard_level": 150,
    "price_per_unit": 3
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_16_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Olive Oil",
    "stock_balance": 550,
    "standard_level": 150,
    "price_per_unit": 2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_17_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Salt",
    "stock_balance": 500,
    "standard_level": 150,
    "price_per_unit": 0.5
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_18_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Sugar",
    "stock_balance": 600,
    "standard_level": 100,
    "price_per_unit": 0.6
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_19_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Loaf_of_bread",
    "stock_balance": 400,
    "standard_level": 100,
    "price_per_unit": 2.5
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_1_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Chicken Breast",
    "stock_balance": 250,
    "standard_level": 100,
    "price_per_unit": 7
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_20_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Spaghetti",
    "stock_balance": 350,
    "standard_level": 100,
    "price_per_unit": 1.1
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_21_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Tomato",
    "stock_balance": 350,
    "standard_level": 100,
    "price_per_unit": 0.7
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_22_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Onion",
    "stock_balance": 300,
    "standard_level": 100,
    "price_per_unit": 1.2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_23_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Potato",
    "stock_balance": 250,
    "standard_level": 100,
    "price_per_unit": 0.4
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_2_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Egg",
    "stock_balance": 450,
    "standard_level": 100,
    "price_per_unit": 1
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_3_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Beef Sausage",
    "stock_balance": 250,
    "standard_level": 100,
    "price_per_unit": 3
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_4_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Chicken Sausage",
    "stock_balance": 250,
    "standard_level": 100,
    "price_per_unit": 2.5
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_5_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Rib Eye Cut",
    "stock_balance": 300,
    "standard_level": 50,
    "price_per_unit": 6
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_6_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Beef Ribs",
    "stock_balance": 300,
    "standard_level": 50,
    "price_per_unit": 7
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_7_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Salmon_250g",
    "stock_balance": 150,
    "standard_level": 100,
    "price_per_unit": 11
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_8_company13",
    "companyID": "resource:org.acme.model.company#company13",
    "item_name": "Squid",
    "stock_balance": 60,
    "standard_level": 20,
    "price_per_unit": 8
  }
]

def dump_data_to_stock(data):
    headers = {'Content-type': 'application/json'}
    claim_post = stock_url + token
    response = requests.post(claim_post, json=data, headers=headers)
    print(response)
#for i in range(len(a)):
  #dump_data_to_stock(a[i])

receipt_first = requests.get(receipt_url + token)
the_receipt_id = receipt_first.json()
print(the_receipt_id)
receipt_id="stock_receipt@_"
for item in the_receipt_id:
    b=item['receiptID'].split("@",1)
    if b[0]=="stock_receipt":
        print(b[0])
a=receipt_id.split("@",1)
if a[0]=="stock_receipt":
    print(a[0])
