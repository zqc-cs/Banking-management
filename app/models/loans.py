# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: accounts.py
@time: 2021/06/09
"""
from . import get_conn
import random
from .accounts import recive_loan


def look_loan(loan_id):
    conn = get_conn()
    cursor = conn.cursor()
    sql_str = "Select LoanID,OfferID, DATE_FORMAT(OfferDate, '%Y-%m-%d') as OfferDate,OfferSum from OfferMoney where LoanID='{0}'".format(loan_id)
    r = 0
    result = []
    success = False
    err_msg = ""
    try:
        r = cursor.execute(sql_str)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        err_msg = "发生未知错误"
        success = False
    else:
        if r == 0:
            success = True
            err_msg = "不存在记录"
        else:
            success = True
            err_msg = "查询成功"
    finally:
        cursor.close()
        conn.close()
        return result, success, err_msg

def search_loan(search_all=True, loan_id="", name=""):
    conn = get_conn()
    cursor = conn.cursor()
    sql_str = ""
    result = []
    err_msg = ""
    show_windows = False
    if search_all:
        # 全部查询
        sql_str = "Select BankName, AccountID, LoanID, LoanSum, LoanState from Loan"
    else:
        sql_str = ""
        if loan_id == "" and name == "":
            err_msg = "请输入查询条件"
            show_windows = True
            return result, err_msg, show_windows
        else:
            if loan_id is not None and loan_id != "":
                sql_str = "Select BankName, AccountID, LoanID, LoanSum, LoanState from Loan where LoanID='{0}'".format(loan_id)
            else:
                sql_str = "Select BankName, AccountID, LoanID, LoanSum, LoanState from Loan where BankName='{0}'".format(name)
    try:
        row = cursor.execute(sql_str)
        result = cursor.fetchall()
        print(result)
    except Exception as e:
        err_msg = "可能不存在对应贷款"
        show_windows = True
    else:
        if row == 0:
            show_windows = True
            err_msg = "贷款不存在"
        else:
            err_msg = "查询成功"
            show_windows = False
    finally:
        cursor.close()
        conn.close()
        return result, err_msg, show_windows


class Loan():
    def __init__(self, id=None, bank_name=None, account_id=None, loan_sum=None, loan_state = None):
        self.id = id
        self.bank_name = bank_name
        self.account_id = account_id
        self.loan_sum = loan_sum
        self.loan_state = loan_state
    
    def add_loan(self):
        conn = get_conn()
        cursor = conn.cursor()
        rand_id = random.sample('0123456789',9)
        rand_id = "".join(rand_id)
        print(rand_id)
        while True:
            r_num = cursor.execute("Select LoanID from Loan where LoanID={0}".format(rand_id))
            if r_num == 0:
                break
            rand_id = random.sample('0123456789',9)
        sql_str = 'Insert into Loan(BankName, AccountID, LoanID, LoanSum, LoanState, LoanDate) value("{0}","{1}","{2}","{3}", "0", Date(Now()))'.format(self.bank_name, self.account_id, rand_id, self.loan_sum)
        sql_str = sql_str.replace('"None"', "Null")
        sql_str = sql_str.replace('""', "Null")
        print(sql_str)
        r = 0
        success = True
        err_msg = "OK"
        try:
            r = cursor.execute(sql_str)
        except Exception as e:
            if r == 0:
                print(e)
                success = False
                err_msg = "账户号、银行可能不存在，金额可能不符合规则"
            else:
                success = False
                err_msg = "发生未知错误"
        else:
            if r == 0:
                success = False
                err_msg = "账户号、银行可能不存在，金额可能不符合规则"
            else:
                conn.commit()
                success = True
                err_msg = "添加成功"
        finally:
            cursor.close()
            conn.close()
            return success, err_msg
    
    def offer_loan(self, offer_date, offer_sum):
        conn = get_conn()
        cursor = conn.cursor()
        # 检查发放的金额是否小于还未支付的金额
        r = 0
        try:
            r = cursor.execute("Select sum(OfferSum) from OfferMoney where LoanID='{0}' group by LoanID".format(self.id))
            result = cursor.fetchall()
        except Exception as e:
            print(e)
            cursor.close()
            conn.close()
            return False, "发生未知错误"
        else:
            offered_sum = 0
            if r != 0:
                offered_sum = result[0][0]
            else:
                # 改变贷款状态
                cursor.execute("Update Loan set LoanState='1' where LoanID='{0}'".format(self.id))
            if float(self.loan_sum) < offered_sum + float(offer_sum):
                cursor.close()
                conn.close()
                return False, "超出贷款金额"
            elif float(self.loan_sum) == offered_sum + float(offer_sum):
                cursor.execute("Update Loan set LoanState='2' where LoanID='{0}'".format(self.id))
                
        rand_id = random.sample('0123456789',9)
        rand_id = "".join(rand_id)
        # print(rand_id)
        # print("awdawdawd")
        while True:
            r_num = cursor.execute("Select OfferID from OfferMoney where OfferID={0}".format(rand_id))
            if r_num == 0:
                break
            rand_id = random.sample('0123456789',9)
            rand_id = "".join(rand_id)
        sql_str = 'Insert into OfferMoney(LoanID, OfferID, OfferDate, OfferSum) value("{0}", "{1}", "{2}", "{3}")'.format(self.id, rand_id, offer_date, offer_sum)
        sql_str = sql_str.replace('"None"', "Null")
        sql_str = sql_str.replace('""', "Null")
        print(sql_str)
        r = 0
        success = True
        err_msg = "OK"
        receive_success = False
        receive_msg = ""
        try:
            r = cursor.execute(sql_str)
            receive_success, receive_msg = recive_loan(self.account_id, offer_sum)
        except Exception as e:
            if r == 0:
                print(e)
                success = False
                err_msg = "账户号可能重复或可能无此银行"
            else:
                success = False
                err_msg = "发生未知错误"
        else:
            if receive_success is not True:
                success = False
                err_msg = receive_msg
            elif r == 0:
                success = False
                err_msg = "发放失败"
            else:
                conn.commit()
                success = True
                err_msg = "发放成功"
        finally:
            cursor.close()
            conn.close()
            return success, err_msg
        
        
    def delete_loan(self):
        conn = get_conn()
        cursor = conn.cursor()
        sql_str = "Delete from Loan where LoanID='{0}'".format(self.id)
        r = 0
        err = False
        err_msg = ""
        try:
            cursor.execute("Delete from OfferMoney where LoanID='{0}'".format(self.id))    
            r = cursor.execute(sql_str)       
        except Exception as e:
            print(e)
            err = True
            err_msg = "发生未知错误"
        else:
            if r == 0:
                err = True
                err_msg = "删除失败，可能是账户号不存在"
            else:
                conn.commit()
                err = False
                err_msg = "删除成功"
        finally:
            return err, err_msg
