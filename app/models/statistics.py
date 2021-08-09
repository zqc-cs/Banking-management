from . import get_conn


def statistics_saving(begin_time, end_time):
    conn = get_conn()
    cursor = conn.cursor()
    result = []
    err_msg = ""
    show_windows = False
    sql_str = "Select BankName, count(*) as AccountCount, sum(Balance) as BalanceCount from SavingAccount where OpenDate>='{0}' and openDate<='{1}' group by BankName;".format(begin_time, end_time)
    try:
        cursor.execute(sql_str)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        err_msg = "发生未知错误"
        show_windows = True
    else:
        err_msg = "成功"
        show_windows = False
    finally:
        cursor.close()
        conn.close()
        return result, show_windows, err_msg


def statistics_loan(begin_time, end_time):
    conn = get_conn()
    cursor = conn.cursor()
    result = []
    err_msg = ""
    show_windows = False
    sql_str = "Select BankName, count(*) as LoanCount, sum(LoanSum) as LoanSumCount from Loan where LoanDate>='{0}' and LoanDate<='{1}' group by BankName;".format(begin_time, end_time)
    try:
        cursor.execute(sql_str)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        err_msg = "发生未知错误"
        show_windows = True
    else:
        err_msg = "成功"
        show_windows = False
    finally:
        cursor.close()
        conn.close()
        return result, show_windows, err_msg