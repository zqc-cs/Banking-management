# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: accounts.py
@time: 2021/06/09
"""
from . import get_conn
import random


def search_loan_for_account(account_id):
    conn = get_conn()
    cursor = conn.cursor()
    success = True
    err_msg = ""
    sql_str = ""
    result = []
    r = 0
    sql_str = "Select BankName, AccountID, LoanID, LoanSum, LoanState From Loan where AccountID='{0}'".format(account_id)
    print(sql_str)
    try:
        r = cursor.execute(sql_str)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        success = False
        err_msg = "出现了未知错误"
    else:
        if r == 0:
            success = True
            err_msg = "暂无记录"
        else:
            success = True
            err_msg = "成功"
    finally:
            cursor.close()
            conn.close()
            return result, success, err_msg


def look_account_type(account_id):
    conn = get_conn()
    cursor = conn.cursor()
    r = 0
    success = False
    result = "储蓄账户"
    sql_str_saving = "Select AccountID from SavingAccount where AccountID='{0}'".format(account_id)
    try:
        r = cursor.execute(sql_str_saving)
    except Exception as e:
        print(e)
        success = False
    else:
        success = True
        if r == 0:
            result = "支票账户"
        else:
            result = "储蓄账户"
    finally:
        return result, success

def search_customer_for_account(account_id, account_type):
    conn = get_conn()
    cursor = conn.cursor()
    success = True
    err_msg = ""
    sql_str = ""
    result = []
    r = 0
    if account_type == "储蓄账户":
        sql_str = "Select CustomerName, CustomerID From Customer where CustomerID IN (Select CustomerID from SavingAccountConstraint where AccountID='{0}')".format(account_id)
    else:
        sql_str = "Select CustomerName, CustomerID From Customer where CustomerID IN (Select CustomerID from CheckingAccountConstraint where AccountID='{0}')".format(account_id)
    print(sql_str)
    try:
        r = cursor.execute(sql_str)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        success = False
        err_msg = "出现了未知错误"
    else:
        if r == 0:
            success = True
            err_msg = "暂无记录"
        else:
            success = True
            err_msg = "成功"
    finally:
            cursor.close()
            conn.close()
            return result, success, err_msg
    

def bind(customer_id, bank_name, account_id, account_type):
    conn = get_conn()
    cursor = conn.cursor()
    success = True
    err_msg = ""
    sql_str = ""
    r = 0
    if account_type == "储蓄账户":
        sql_str = "Insert into SavingAccountConstraint(CustomerID, BankName, AccountID) value ('{0}', '{1}', '{2}')".format(customer_id, bank_name, account_id)
    else:
        sql_str = "Insert into CheckingAccountConstraint(CustomerID, BankName, AccountID) value ('{0}', '{1}', '{2}')".format(customer_id, bank_name, account_id)
    print(sql_str)
    try:
        r = cursor.execute(sql_str)
    except Exception as e:
        print(e)
        success = False
        err_msg = "该客户在这个银行可能拥有多个同类型账户或客户不存在"
    else:
        if r == 0:
            success = False
            err_msg = "该客户在这个银行可能拥有多个同类型账户"
        else:
            conn.commit()
            success = True
            err_msg = "绑定成功"
    return success, err_msg
    

def cancel_bind(account_id, customer_id, account_type):
    conn = get_conn()
    cursor = conn.cursor()
    r = 0
    success = True
    err_msg = ""
    if account_type == "储蓄账户":
        sql_str = "Delete From SavingAccountConstraint where CustomerID='{0}' and AccountID='{1}'".format(customer_id, account_id)
    else:
        sql_str = "Delete From CheckingAccountConstraint where CustomerID='{0}' and AccountID='{1}'".format(customer_id, account_id)
    try:
        r = cursor.execute(sql_str)
    except Exception as e:
        success = False
        err_msg = "解除绑定失败，发生未知错误"
    else:
        if r == 0:
            success = False
            err_msg = "解除绑定失败"
        else:
            success = True
            err_msg = "解除绑定成功"
            conn.commit()
    finally:
        cursor.close()
        conn.close()
        return success, err_msg



def recive_loan(account_id, offer_sum):
    conn = get_conn()
    cursor = conn.cursor()
    sql_str_saving = 'Update SavingAccount set Balance=Balance + "{0}" where AccountID="{1}"'.format(offer_sum, account_id)
    sql_str_checking = 'Update CheckAccount set Balance=Balance + "{0}" where AccountID="{1}"'.format(offer_sum, account_id)
    r_saving = 0
    r_checking = 0
    success = True
    err_msg = "OK"
    try:
        r_saving = cursor.execute(sql_str_saving)
        r_checking = cursor.execute(sql_str_checking)
    except Exception as e:
        if r_saving + r_checking == 0:
            print(e)
            success = False
            err_msg = "付款钱数不正确或未知错误"
        else:
            success = False
            err_msg = "发生未知错误"
    else:
        if r_saving + r_checking == 0:
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

def search_account(search_all=True, account_id="", name=""):
    conn = get_conn()
    cursor = conn.cursor()
    sql_str = ""
    result = []
    err_msg = ""
    show_windows = False
    if search_all:
        # 全部查询
        sql_str = "Select AccountID, BankName, Balance, DATE_FORMAT(OpenDate, '%Y-%m-%d') as OpenDate, Rate, CurrencyType, Null as OverDraft from SavingAccount Union "
        sql_str = sql_str +  "Select AccountID, BankName, Balance, DATE_FORMAT(OpenDate, '%Y-%m-%d') as OpenDate, Null as Rate, Null as CurrencyType, OverDraft from CheckAccount"
    else:
        sql_str = ""
        if account_id == "" and name == "":
            err_msg = "请输入查询条件"
            show_windows = True
            return result, err_msg, show_windows
        else:
            if account_id is not None and account_id != "":
                sql_str = "Select AccountID, BankName, Balance, DATE_FORMAT(OpenDate, '%Y-%m-%d') as OpenDate, Rate, CurrencyType, Null as OverDraft from SavingAccount where {0}='{1}'  \
                    Union Select AccountID, BankName, Balance, DATE_FORMAT(OpenDate, '%Y-%m-%d') as OpenDate, Null as Rate, Null as CurrencyType, OverDraft from CheckAccount Where {2}='{3}'".format("AccountID", account_id, "AccountID", account_id)
            else:
                sql_str = "Select AccountID, BankName, Balance, DATE_FORMAT(OpenDate, '%Y-%m-%d') as OpenDate, Rate, CurrencyType, Null as OverDraft from SavingAccount where {0}='{1}'  \
                    Union Select AccountID, BankName, Balance, DATE_FORMAT(OpenDate, '%Y-%m-%d') as OpenDate, Null as Rate, Null as CurrencyType, OverDraft from CheckAccount Where {2}='{3}'".format("BankName", name, "BankName", name)
    try:
        row = cursor.execute(sql_str)
        result = cursor.fetchall()
        # print(result)
    except Exception as e:
        err_msg = "可能不存在对应账户"
        show_windows = True
    else:
        if row == 0:
            show_windows = True
            err_msg = "账户不存在"
        else:
            err_msg = "查询成功"
            show_windows = False
    finally:
        cursor.close()
        conn.close()
        return result, err_msg, show_windows


class Account():
    def __init__(self, id=None, name=None, balance=None, open_date=None):
        self.id = id
        self.name = name
        self.balance = balance
        self.open_date = open_date
    
    def delete_account(self):
        conn = get_conn()
        cursor = conn.cursor()
        sql_str_account = "Delete from Account where AccountID='{0}'".format(self.id)
        sql_str_saving = "Delete from SavingAccount where AccountID='{0}'".format(self.id)
        sql_str_checking = "Delete from CheckAccount where AccountID='{0}'".format(self.id)
        r = 0
        err = False
        err_msg = ""
        try:
            cursor.execute(sql_str_account)
            r_saving = cursor.execute(sql_str_saving)
            r_checking = cursor.execute(sql_str_checking)
            cursor.execute("Delete from SavingAccountConstraint where AccountID='{0}'".format(self.id))
            cursor.execute("Delete from CheckingAccountConstraint where AccountID='{0}'".format(self.id))
            r = r_saving + r_checking
        except Exception as e:
            print(e)
            err = True
            err_msg = "该账户可能存在贷款"
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


class Saving_Account(Account):
    # AccountID, BankName, Balance, OpenDate
    def __init__(self, id=None, name=None, balance=None, open_date=None, rate=None, currency_type=None):
        super().__init__(id, name, balance, open_date)
        self.rate = rate
        self.currency_type = currency_type


    def add_account(self):
        conn = get_conn()
        cursor = conn.cursor()
        rand_id = random.sample('0123456789',9)
        rand_id = "".join(rand_id)
        print(rand_id)
        while True:
            r_num = cursor.execute("Select AccountID from SavingAccount where AccountID={0} Union Select AccountID from CheckAccount where AccountID={1}".format(rand_id, rand_id))
            if r_num == 0:
                break
            rand_id = random.sample('0123456789',9)
            rand_id = "".join(rand_id)
        sql_str = 'Insert into SavingAccount(' \
                  'AccountID, BankName, Balance, OpenDate, Rate, CurrencyType) ' \
                  'value("{0}","{1}","{2}","{3}","{4}","{5}")'.format(rand_id, self.name, self.balance, self.open_date,
                                                                    self.rate, self.currency_type)
        sql_str = sql_str.replace('"None"', "Null")
        sql_str = sql_str.replace('""', "Null")
        # print(sql_str)
        r = 0
        success = True
        err_msg = "OK"
        try:
            cursor.execute("Insert into Account(AccountID) value('{0}')".format(rand_id))
            r = cursor.execute(sql_str)
            
        except Exception as e:
            if r == 0:
                print(e)
                success = False
                err_msg = "账户号可能重复或可能无此银行"
            else:
                success = False
                err_msg = "发生未知错误"
        else:
            if r == 0:
                success = False
                err_msg = "账户号可能重复或可能无此银行"
            else:
                conn.commit()
                success = True
                err_msg = "添加成功"
        finally:
            cursor.close()
            conn.close()
            return success, err_msg
    
    def edit_account(self):
        conn = get_conn()
        cursor = conn.cursor()
        sql_str = 'Update SavingAccount set BankName="{0}", Balance="{1}", OpenDate="{2}", Rate="{3}", CurrencyType="{4}" where AccountID="{5}"'.format(self.name, self.balance, self.open_date,self.rate, self.currency_type, self.id)
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
                err_msg = "账户号可能重复或可能无此银行"
            else:
                success = False
                err_msg = "发生未知错误"
        else:
            if r == 0:
                success = False
                err_msg = "无更改"
            else:
                conn.commit()
                success = True
                err_msg = "修改成功"
        finally:
            cursor.close()
            conn.close()
            return success, err_msg


class Checking_Account(Account):
    # AccountID, BankName, Balance, OpenDate
    def __init__(self, id=None, name=None, balance=None, open_date=None, overdraft=None):
        super().__init__(id, name, balance, open_date)
        self.overdraft = overdraft


    def add_account(self):
        conn = get_conn()
        cursor = conn.cursor()
        rand_id = random.sample('0123456789',9)
        rand_id = "".join(rand_id)
        print(rand_id)
        while True:
            r_num = cursor.execute("Select AccountID from SavingAccount where AccountID={0} Union Select AccountID from CheckAccount where AccountID={1}".format(rand_id, rand_id))
            if r_num == 0:
                break
            rand_id = random.sample('0123456789',9)
        sql_str = 'Insert into CheckAccount(' \
                  'AccountID, BankName, Balance, OpenDate, OverDraft) ' \
                  'value("{0}","{1}","{2}","{3}","{4}")'.format(rand_id, self.name, self.balance, self.open_date,
                                                                    self.overdraft)
        sql_str = sql_str.replace('"None"', "Null")
        sql_str = sql_str.replace('""', "Null")
        print(sql_str)
        r = 0
        success = True
        err_msg = "OK"
        try:
            cursor.execute("Insert into Account(AccountID) value('{0}')".format(rand_id))
            r = cursor.execute(sql_str)
            
        except Exception as e:
            if r == 0:
                print(e)
                success = False
                err_msg = "账户号可能重复或可能无此银行"
            else:
                success = False
                err_msg = "发生未知错误"
        else:
            conn.commit()
            success = True
            err_msg = "添加成功"
        finally:
            cursor.close()
            conn.close()
            return success, err_msg
        
    def edit_account(self):
        conn = get_conn()
        cursor = conn.cursor()
        sql_str = 'Update CheckAccount set BankName="{0}", Balance="{1}", OpenDate="{2}", OverDraft="{3}" where AccountID="{4}"'.format(self.name, self.balance, self.open_date,self.overdraft, self.id)
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
                err_msg = "未知错误"
            else:
                success = False
                err_msg = "发生未知错误"
        else:
            if r == 0:
                success = False
                err_msg = "无更改"
            else:
                conn.commit()
                success = True
                err_msg = "修改成功"
        finally:
            cursor.close()
            conn.close()
            return success, err_msg
    
