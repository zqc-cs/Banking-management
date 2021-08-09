# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: views.py
@time: 2021/06/06
"""
from . import customers
from flask import render_template, redirect, request, flash, url_for, get_flashed_messages, session
from ..models.customers import Customer, search_account
import json


@customers.route("/customers")
def customers_home():
    return render_template("customers/customers_index.html")


@customers.route("/customers/customer_show")
def customers_show():
    customer_id = request.args.get("ID")
    print(customer_id)
    if customer_id != "" and customer_id != None:
        result, err_msg, show_windows = Customer.search_customer(search_all=False, CustomerID=customer_id)
        has_err, account_result = search_account(customer_id)
        if show_windows != True and has_err != True:
            account_result = list(account_result)
            print(account_result)
            return render_template("customers/customers_show.html", row=len(account_result), customer=result[0], accounts=account_result)
        else:
            return redirect(url_for(".customers_other"))
    return redirect(url_for(".customers_other"))


@customers.route("/customers/add_customer", methods=['GET', 'POST'])
def add_customers():
    return render_template("customers/customers_add.html")

@customers.route("/customers/process_add_customer", methods=['POST'])
def process_add_customer():
    customer = Customer()
    customer.id = request.form.get('id')
    customer.staff_id = request.form.get('staff_id')
    customer.name = request.form.get('name')
    customer.phone = request.form.get('phone')
    customer.addr = request.form.get('address')
    customer.contact_name = request.form.get('contact_name')
    customer.contact_phone = request.form.get('contact_phone')
    customer.contact_mail = request.form.get('contact_mail')
    customer.contact_addr = request.form.get('contact_address')
    customer.relationship = request.form.get('relationship')
    add_success, add_msg = customer.add_customer()
    result = {}
    result["add_success"] = add_success
    result["add_msg"] = add_msg
    result = json.dumps(result)
    return result
    
@customers.route("/customers/search_customer", methods=['GET'])
def search_customers():
    way = request.args.get("search")
    customers = ()
    result = {}
    flash_msg=""
    show_windows=False
    if way == 'all':
        customers, flash_msg, show_windows = Customer.search_customer(search_all=True)
    elif way == "someone":
        CustomerID = request.args.get("id")
        CustomerName = request.args.get("name")
        customers, flash_msg, show_windows = Customer.search_customer(search_all=False, CustomerID=CustomerID, CustomerName=CustomerName)
    else:
        customers=()
        flash_msg="请求错误"
        show_windows=True
    customers = list(customers)
    result["search_msg"] = flash_msg
    result["show_windows"] = show_windows
    result["customers"] = customers
    customers = json.dumps(result)
    return customers

@customers.route("/customers/other_options", methods=['GET', 'POST'])
def customers_other():
    return render_template("customers/customers_search.html")


# @customers.route("/customers/customer_show", methods=['GET'])
# def customers_show():
#     ID=request.args.get("ID")
#     customers, flash_msg, show_windows = Customer.search_customer(search_all=False, CustomerID=ID)
#     return render_template("customers/customers_show.html", customer=customers[0])


@customers.route("/customers/customer_edit", methods=['POST'])
def customers_edit():
    ID = request.form.get("ID")
    flash(ID, category='edit')
    customers, flash_msg, show_windows = Customer.search_customer(search_all=False, CustomerID=ID)
    return render_template("customers/customers_edit.html", customer=customers[0], show_alert=False)


@customers.route("/customers/do_edit", methods=['Get', 'POST'])
def do_edit():
    if request.method == 'POST':
        old_ID = get_flashed_messages(category_filter=['edit'])
        customer = Customer()
        customer.id = request.form.get('ID')
        customer.staff_id = request.form.get('staff_id')
        customer.name = request.form.get('name')
        customer.phone = request.form.get('phone')
        customer.addr = request.form.get('address')
        customer.contact_name = request.form.get('contact_name')
        customer.contact_phone = request.form.get('contact_phone')
        customer.contact_mail = request.form.get('contact_mail')
        customer.contact_addr = request.form.get('contact_address')
        customer.relationship = request.form.get('relationship')
        err, err_msg = customer.edit_customer(old_ID=old_ID[0])
        if err is not True:
            return redirect(url_for('.do_edit'))
        else:
            return render_template("customers/customers_edit.html", customer=customer, show_alert=True, err_msg=err_msg)
    else:
        return render_template("customers/customers_search.html")



@customers.route("/customers/customer_delete", methods=['GET'])
def customers_delete():
    ID = request.args.get("ID")
    customer = Customer(id=ID)
    result = {}
    
    err, err_msg = customer.delete_customer()
    result["err"] = err
    result["err_msg"] = err_msg
    result = json.dumps(result)
    return result