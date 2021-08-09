# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: views.py
@time: 2021/06/09
"""
from decimal import Decimal

from . import loans
from flask import render_template, redirect, request, session, url_for, flash, get_flashed_messages
from ..models.loans import Loan, search_loan as search, look_loan
from ..models.accounts import look_account_type
import json

import datetime


@loans.route("/loans")
def index():
    return render_template("loans/loans_index.html")


@loans.route("/loans/add_loan")
def add_loan():
    return render_template("loans/loans_add.html")

@loans.route("/loans/do_add", methods=['POST'])
def do_add():
    result = {}
    loan = Loan()
    loan.account_id = request.form.get('account_id')
    loan.bank_name = request.form.get('bank_name')
    loan.loan_sum = request.form.get('loan_sum')
    success, err_msg = loan.add_loan()
    result["success"] = success
    result["err_msg"] = err_msg
    result = json.dumps(result)
    return result
        

@loans.route("/loans/other_options")
def other_options():
    return render_template("loans/loans_search.html")


@loans.route("/loans/search_loan")
def search_loans():
    result = {}
    loan_list = []
    err_msg = ""
    show_windows = False
    search_way = request.args.get("search")
    if search_way == 'all':
        loan_list, err_msg, show_windows = search(search_all=True)
    elif search_way == 'someone':
        loan_id = request.args.get("id")
        loan_name = request.args.get("name")
        loan_list, err_msg, show_windows = search(search_all=False, loan_id=loan_id, name=loan_name)
    else:
        loan_list = []
        err_msg = "请正确选择查询条件"
        show_windows = True
    result["loans"] = list(loan_list)
    result["search_msg"] = err_msg
    result["show_windows"] = show_windows
    result = json.dumps(result)
    # print(result)
    return result


@loans.route("/loans/loans_show")
def loans_show():
    loan_id = request.args.get("ID")
    account_id = request.args.get("account_id")
    account_type, success = look_account_type(account_id)
    offer_result = []
    if loan_id != "" and account_id != "" and loan_id != None and account_id != None and success == True:
        offer_result, success, err_msg = look_loan(loan_id)
        result, search_err_msg, show_windows = search(search_all=False, loan_id=loan_id)
        if success == True and show_windows == False:
            offer_result = list(offer_result)
            return render_template("loans/loans_show.html", loan=result[0], row=len(offer_result), offers=offer_result, account_id=account_id, account_type=account_type)
        else:
            return redirect(url_for(".other_options"))
    return redirect(url_for(".other_options"))


@loans.route("/loans/loans_edit", methods=["POST"])
def loans_offer():
    loan_id = request.form.get("ID")
    loans, flash_msg, show_windows = search(search_all=False, loan_id=loan_id)
    if len(loans) == 0 or show_windows is True:
        return redirect(".other_options")
    else:
        return render_template("loans/loans_offer.html", loan=loans[0], show_alert=False)
    


@loans.route("/loans/do_edit", methods=["POST"])
def do_offer():
    result = {}
    loan = Loan()
    loan.id = request.form.get("loan_id")
    loan.account_id = request.form.get("account_id")
    loan.loan_sum = request.form.get("loan_sum")
    loan.loan_state = request.form.get("loan_state")
    offer_date = request.form.get("offer_date")
    offer_money = request.form.get("offer_sum")
    if loan.id != None and loan.id != "":
        success, err_msg = loan.offer_loan(offer_date, offer_money)
        result["success"] = success
        result["err_msg"] = err_msg
    else:
        result["success"] = False
        result["err_msg"] = "请确定贷款号"
    result = json.dumps(result)
    return result

@loans.route("/loans/loans_delete")
def loans_delete():
    loan_id = request.args.get("ID")
    loan = Loan(id=loan_id)    
    result = {}
    
    err, err_msg = loan.delete_loan()
    result["err"] = err
    result["err_msg"] = err_msg
    result = json.dumps(result)
    return result