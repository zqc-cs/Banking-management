# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: views.py
@time: 2021/06/09
"""
from decimal import Decimal

from . import accounts
from flask import render_template, redirect, request, session, url_for, flash, get_flashed_messages
from ..models.accounts import Saving_Account, Checking_Account, Account, search_account as search, bind, search_customer_for_account, cancel_bind, search_loan_for_account
import json

import datetime


@accounts.route("/accounts")
def index():
    return render_template("accounts/accounts_index.html")


@accounts.route("/accounts/show_account")
def accounts_show():
    account_id = request.args.get("ID")
    account_type = request.args.get("type")
    customer_result = []
    if account_id != "" and account_type != "" and account_id != None and account_type != None:
        customer_result, success, err_msg = search_customer_for_account(account_id, account_type)
        account_result, _, has_err = search(search_all=False, account_id=account_id)
        loan_result, loan_success, loan_err_msg = search_loan_for_account(account_id)
        if success == False or has_err == True or loan_success == False:
            return redirect(url_for(".other_options"))
        else:
            customer_result = list(customer_result)
            account_result = list(account_result)
            loan_result = list(loan_result)
            return render_template("accounts/accounts_show.html", account=account_result[0], row_customer=len(customer_result),customers=customer_result, row_loan=len(loan_result), loans=loan_result)
    return redirect(url_for(".other_options"))


@accounts.route("/accounts/bind_account", methods=['POST'])
def accounts_bind():
    account_id = request.form.get("ID")
    bank_name = request.form.get("bank_name")
    account_type = request.form.get("type")
    return render_template("accounts/accounts_bind.html", account_id=account_id, bank_name=bank_name, account_type=account_type)

@accounts.route("/accounts/cancel_bind", methods=['GET'])
def accounts_cancel_bind():
    account_id = request.args.get("account_id")
    customer_id = request.args.get("customer_id")
    account_type = request.args.get("account_type")
    result = {}
    if account_id != "" and customer_id != "" and account_id != None and customer_id != None:
        success, err_msg = cancel_bind(account_id, customer_id, account_type)
        result["success"] = success
        result["err_msg"] = err_msg
    else:
        result["success"] = False
        result["err_msg"] = "请检查用户号和账户号"
    result = json.dumps(result)
    return result


@accounts.route("/accounts/do_bind", methods=['POST'])
def do_bind():
    customer_id = request.form.get("customer_id")
    account_id = request.form.get("id")
    bank_name = request.form.get("bank_name")
    account_type = request.form.get("type")
    result = {}
    if customer_id != "" and account_id != "" and bank_name != "" and account_type != "" and customer_id != None and account_id != None and bank_name != None and account_type != None:
        success, err_msg = bind(customer_id, bank_name, account_id, account_type)
        result["success"] = success
        result["err_msg"] = err_msg
    else:
        result["success"] = False
        result["err_msg"] = "输入不正确"
    result = json.dumps(result)
    return result


@accounts.route("/accounts/add_account/<int:saving_type>")
def add_account(saving_type):
    if saving_type == 1:
        return render_template("accounts/accounts_add_saving.html")
    else:
        return render_template("accounts/accounts_add_checking.html")


@accounts.route("/accounts/do_add", methods=['POST'])
def do_add():
    result = {}
    type = request.form.get('type')
    if type == 'saving_account':
        saving_account = Saving_Account()
        # saving_account.id = request.form.get('id')
        saving_account.name = request.form.get('bank_name')
        saving_account.balance = request.form.get('balance')
        saving_account.rate = request.form.get('rate')
        saving_account.currency_type = request.form.get('currency_type')
        saving_account.open_date = datetime.datetime.now().strftime('%Y-%m-%d')
        success, err_msg = saving_account.add_account()
        result["success"] = success
        result["err_msg"] = err_msg
    elif type == 'checking_account':
        checking_account = Checking_Account()
        # checking_account.id = request.form.get('id')
        checking_account.name = request.form.get('bank_name')
        checking_account.balance = request.form.get('balance')
        checking_account.overdraft = request.form.get('overdraft')
        checking_account.open_date = datetime.datetime.now().strftime('%Y-%m-%d')
        success, err_msg = checking_account.add_account()
        result["success"] = success
        result["err_msg"] = err_msg
    else:
        result["success"] = False
        result["err_msg"] = "请输入注册信息"
    result = json.dumps(result)
    return result
        

@accounts.route("/accounts/other_options")
def other_options():
    return render_template("accounts/accounts_search.html")


@accounts.route("/accounts/search_account")
def search_accounts():
    result = {}
    account_list = []
    err_msg = ""
    show_windows = False
    search_way = request.args.get("search")
    if search_way == 'all':
        account_list, err_msg, show_windows = search(search_all=True)
    elif search_way == 'someone':
        account_id = request.args.get("id")
        account_name = request.args.get("name")
        account_list, err_msg, show_windows = search(search_all=False, account_id=account_id, name=account_name)
    else:
        account_list = []
        err_msg = "请正确选择查询条件"
        show_windows = True
    result["accounts"] = list(account_list)
    result["search_msg"] = err_msg
    result["show_windows"] = show_windows
    result = json.dumps(result)
    # print(result)
    return result


@accounts.route("/accounts/accounts_edit", methods=["POST"])
def accounts_edit():
    account_id = request.form.get("ID")
    accounts, flash_msg, show_windows = search(search_all=False, account_id=account_id)
    if len(accounts) == 0:
        return redirect(".other_options")
    if accounts[0][6] is None:
        return render_template("accounts/accounts_edit_saving.html", account=accounts[0], show_alert=False)
    else:
        return render_template("accounts/accounts_edit_checking.html", account=accounts[0], show_alert=False)
    


@accounts.route("/accounts/do_edit", methods=["POST"])
def do_edit():
    account_type = request.form.get("type")
    result = {}
    if account_type == "saving_account":
        saving_account = Saving_Account()
        saving_account.id = request.form.get('id')
        saving_account.name = request.form.get('bank_name')
        saving_account.balance = request.form.get('balance')
        saving_account.rate = request.form.get('rate')
        saving_account.currency_type = request.form.get('currency_type')
        saving_account.open_date = request.form.get('open_date')
        success, err_msg = saving_account.edit_account()
        result["success"] = success
        result["err_msg"] = err_msg
    elif account_type == "checking_account":
        checking_account = Checking_Account()
        checking_account.id = request.form.get('id')
        checking_account.name = request.form.get('bank_name')
        checking_account.balance = request.form.get('balance')
        checking_account.overdraft = request.form.get('over_draft')
        checking_account.open_date = request.form.get('open_date')
        success, err_msg = checking_account.edit_account()
        result["success"] = success
        result["err_msg"] = err_msg
    else:
        result["success"] = False
        result["err_msg"] = "请确定账户类型"
    result = json.dumps(result)
    return result

@accounts.route("/accounts/accounts_delete")
def accounts_delete():
    account_id = request.args.get("ID")
    account = Account(id=account_id)    
    result = {}
    
    err, err_msg = account.delete_account()
    result["err"] = err
    result["err_msg"] = err_msg
    result = json.dumps(result)
    return result