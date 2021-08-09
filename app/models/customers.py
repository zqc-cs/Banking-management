# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: customers.py
@time: 2021/06/08
"""
from . import get_conn

def search_account(customer_id):
    conn = get_conn()
    cursor = conn.cursor()
    result = []
    r = 0
    has_err = False
    sql_str = "Select AccountID, BankName, 0 as AccountType from SavingAccountConstraint where CustomerID='{0}' \
                Union Select AccountID, BankName, 1 as AccountType from CheckingAccountConstraint where CustomerID='{1}'".format(customer_id, customer_id)
    print(sql_str)
    try:
        r = cursor.execute(sql_str)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        has_err = True
    finally:
        cursor.close()
        conn.close()
        return has_err, result

class Customer():
    # 客户类，存客户的信息
    def __init__(self, name=None, id=None, staff_id=None, phone=None, addr=None,
                 contact_name=None, contact_phone=None, contact_mail=None, contact_addr=None, relationship=None):
        self.name = name
        self.id = id
        self.staff_id = None if staff_id == "" else staff_id
        self.phone = phone
        self.addr = addr
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.contact_mail = None if contact_mail == "" else contact_mail
        self.contact_addr = contact_addr
        self.relationship = relationship

    def add_customer(self):
        # 获取数据库连接
        self.staff_id = None if self.staff_id == "" else self.staff_id
        self.contact_mail = None if self.contact_mail == "" else self.contact_mail
        conn = get_conn()
        print("Adwd", self.relationship)
        cursor = conn.cursor()
        sql_str = 'Insert into Customer(' \
                  'CustomerID,StaffID,CustomerName,CustomerPhone,CustomerAddress,' \
                  'ContactName,ContactPhone,ContactMail,ContactAddress,Relationship)' \
                  'value("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}")'.format(
            self.id, self.staff_id, self.name, self.phone, self.addr,
            self.contact_name, self.contact_phone, self.contact_mail, self.contact_addr, self.relationship)
        sql_str = sql_str.replace('"None"', "Null")
        sql_str = sql_str.replace('""', "Null")
        print(sql_str)
        r = 0
        success = True
        err_msg = "OK"
        try:
            r = cursor.execute(sql_str)
            conn.commit()
        except Exception as e:
            if r == 0:
                print(e)
                success = False
                err_msg = "身份证号重复或无此员工"
            else:
                success = False
                err_msg = "发生未知错误"
        else:
            success = True
            err_msg = "添加成功"
        finally:
            cursor.close()
            conn.close()
            return success, err_msg

    @staticmethod
    def search_customer(search_all=True, CustomerID=None, CustomerName=None):
        '''CustomerID as id, StaffID as staff_id, CustomerName as name, CustomerPhone as phone," \
                      " CustomerAddress as addr, ContactName as contact_name, ContactPhone as contact_phone," \
                      " ContactMail as contact_mail, ContactAddress as contact_addr, Relationship as relationship" \
                      " '''
        conn = get_conn()
        cursor = conn.cursor()
        sql_str = ""
        result = []
        err_msg = ""
        show_windows = False
        if search_all:
            # 全部查询
            sql_str = "Select * from Customer"
        else:
            sql_str = "Select * from Customer where "
            if CustomerID == "" and CustomerName == "":
                err_msg = "请输入查询条件"
                show_windows = True
                return result, err_msg, show_windows
            else:
                if CustomerID is not None and CustomerID != "":
                    sql_str += "CustomerID='{0}'".format(CustomerID)
                else:
                    sql_str += "CustomerName='{0}'".format(CustomerName)
        try:
            row = cursor.execute(sql_str)
            result = cursor.fetchall()
        except Exception as e:
            err_msg = "可能不存在对应用户"
            show_windows = True
        else:
            if row == 0:
                show_windows = True
                err_msg = "用户不存在"
            else:
                err_msg = "查询成功"
                show_windows = False
        finally:
            cursor.close()
            conn.close()
            return result, err_msg, show_windows

    def delete_customer(self):
        sql_str = "Delete from Customer where CustomerID='{0}'".format(self.id)
        print(sql_str)
        # 要考虑客户是否存在着关联账户或者贷款记录
        err_msg = ""
        err = True
        try:
            conn = get_conn()
            cursor = conn.cursor()
            r = cursor.execute(sql_str)
            if r == 0:
                err = True
                err_msg = "删除失败"
                cursor.close()
                conn.close()
                return err, err_msg
        except Exception as e:
            err = True
            err_msg = "删除失败，可能存在关联账户"
            print(e)
        else:
            conn.commit()
            err = False
            err_msg = "删除成功"
        finally:
            cursor.close()
            conn.close()
            return err, err_msg


    def edit_customer(self, old_ID):
        sql_str = ""
        err_msg = ""
        err = True
        self.staff_id = None if self.staff_id == "" else self.staff_id
        self.contact_mail = None if self.contact_mail == "" else self.contact_mail
        if self.id == old_ID:
            sql_str = "Update Customer Set StaffID='{0}',CustomerName='{1}',CustomerPhone='{2}'," \
                      "CustomerAddress='{3}'," \
                      "ContactName='{4}',ContactPhone='{5}',ContactMail='{6}',ContactAddress='{7}',Relationship='{8}' " \
                      "where CustomerID='{9}'".format(self.staff_id, self.name, self.phone, self.addr,
                                                       self.contact_name, self.contact_phone, self.contact_mail,
                                                       self.contact_addr, self.relationship, self.id)
        else:
            r = 0
            conn = get_conn()
            cursor = conn.cursor()
            r = cursor.execute("Select * from Customer where CustomerID={0}".format(self.id))
            cursor.close()
            conn.close()
            if r > 0:
                # 存在已有数据
                err_msg = "客户新身份证冲突"
                err = True
                return err, err_msg
            else:
                sql_str = "Update Customer Set CustomerID='{0}',StaffID='{1}',CustomerName='{2}',CustomerPhone='{3}'," \
                      "CustomerAddress='{4}'," \
                      "ContactName='{5}',ContactPhone='{6}',ContactMail='{7}',ContactAddress='{8}',Relationship='{9}' " \
                      "where CustomerID='{10}'".format(self.id, self.staff_id, self.name, self.phone, self.addr,
                                                       self.contact_name, self.contact_phone, self.contact_mail,
                                                       self.contact_addr, self.relationship, old_ID)
        try:
            conn = get_conn()
            cursor = conn.cursor()
            sql_str = sql_str.replace("'None'", "Null")
            print(sql_str)
            r = cursor.execute(sql_str)
            
        except Exception as e:
            err_msg = "出错，可能不存在该员工"
            err = True
            print(e)
        else:
            err = False
            err_msg = "成功"
        finally:
            conn.commit()
            cursor.close()
            conn.close()
            return err, err_msg
