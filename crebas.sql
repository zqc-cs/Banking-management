/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/6/7 9:39:13                             */
/*==============================================================*/

drop database if exists lab3;

create database lab3;

use lab3;

drop table if exists AccessCount;

drop table if exists Account;

drop table if exists Bank;

drop table if exists CheckAccount;

drop table if exists CheckingAccountConstraint;

drop table if exists Staff;

drop table if exists Customer;

drop table if exists Department;

drop table if exists Loan;

drop table if exists OfferMoney;

drop table if exists SavingAccount;

drop table if exists SavingAccountConstraint;

/*==============================================================*/
/* Table: Bank                                                  */
/*==============================================================*/
create table Bank
(
   BankName             varchar(50) not null,
   City                 varchar(20) not null,
   BankAssets           double(20,2) not null,
   primary key (BankName)
);

/*==============================================================*/
/* Table: Department                                            */
/*==============================================================*/
create table Department
(
   DepartmentID         varchar(9) not null,
   BankName             varchar(50) not null,
   ManagerID            varchar(18) not null,
   DepartmentName       varchar(10) not null,
   DepartmentType       varchar(10) not null,
   primary key (DepartmentID),
   constraint fk_department_bank Foreign Key(BankName) references Bank(BankName)
);

/*==============================================================*/
/* Table: Staff                                           */
/*==============================================================*/
create table Staff
(
   StaffID              varchar(18) not null,
   BankName             varchar(50) not null,
   DepartmentID         varchar(9),
   StaffName            varchar(15) not null,
   StaffPhone           varchar(11) not null,
   StaffAddress         varchar(50) not null,
   StartDate            date not null,
   primary key (StaffID),
   constraint fk_staff_bank Foreign Key(BankName) references Bank(BankName),
   constraint fk_staff_department Foreign Key(DepartmentID) references Department(DepartmentID)
);

alter table Department add constraint fk_department_manager Foreign Key(ManagerID) references Staff(StaffID);

/*==============================================================*/
/* Table: Customer                                              */
/*==============================================================*/
create table Customer
(
   CustomerID           char(18) not null,
   StaffID              char(18),
   CustomerName         varchar(15) not null,
   CustomerPhone        varchar(11) not null,
   CustomerAddress      varchar(50) not null,
   ContactName          varchar(15) not null,
   ContactPhone         varchar(11) not null,
   ContactMail          varchar(45),
   ContactAddress       varchar(50) not null,
   Relationship         varchar(15) not null,
   primary key (CustomerID),
   constraint fk_customer_staff Foreign Key(StaffID) references Staff(StaffID)
);

/*==============================================================*/
/* Table: Account                                               */
/*==============================================================*/
create table Account
(
   AccountID            varchar(18) not null,
   primary key (AccountID)
);

/*==============================================================*/
/* Table: SavingAccount                                         */
/*==============================================================*/
create table SavingAccount
(
   AccountID            varchar(18) not null,
   BankName             varchar(50) not null,
   Balance              double(20,2) not null,
   OpenDate            	datetime not null,
   Rate                 real not null,
   CurrencyType         varchar(15) not null,
   primary key (AccountID),
   constraint fk_savingaccount_bank Foreign Key(BankName) references Bank(BankName)
);

/*==============================================================*/
/* Table: CheckAccount                                          */
/*==============================================================*/
create table CheckAccount
(
   AccountID            varchar(18) not null,
   BankName             varchar(50) not null,
   Balance              double(20,2) not null,
   OpenDate            	datetime not null,
   OverDraft            double(15,2) not null,
   primary key (AccountID),
   constraint fk_checkaccount_bank Foreign Key(BankName) references Bank(BankName)
);


/*==============================================================*/
/* Table: AccessAccount                                          */
/*==============================================================*/
create table AccessAccount
(
   CustomerID           char(18) not null,
   AccountID            varchar(18) not null,
   RecentlyAccessDate   datetime not null,
   primary key (CustomerID, AccountID),
   constraint fk_accessaccount_customer Foreign Key(CustomerID) references Customer(CustomerID),
   constraint fk_accessaccount_acount Foreign Key(AccountID) references Account(AccountID)
);

/*==============================================================*/
/* Table: AccessChecking                                        */
/*==============================================================*/
/*
create table AccessChecking
(
   CustomerID           char(18) not null,
   AccountID            varchar(18) not null,
   RecentlyAccessDate  datetime not null,
   primary key (CustomerID, AccountID),
   constraint fk_accesschecking_customer Foreign Key(CustomerID) references Customer(CustomerID),
   constraint fk_accesschecking_acount Foreign Key(AccountID) references Account(AccountID)
);
*/

/*==============================================================*/
/* Table: SavingAccountConstraint                               */
/*==============================================================*/
create table SavingAccountConstraint
(
   CustomerID           char(18) not null,
   BankName             varchar(50) not null,
   AccountID            varchar(18) not null,
   primary key (CustomerID, BankName),
   constraint fk_savingaccountconstraint_customer Foreign Key(CustomerID) references Customer(CustomerID) ON UPDATE CASCADE,
   constraint fk_savingaccountconstraint_bank Foreign Key(BankName) references Bank(BankName),
   constraint fk_savingaccountconstraint_acount Foreign Key(AccountID) references Account(AccountID)
);

/*==============================================================*/
/* Table: CheckingAccountConstraint                             */
/*==============================================================*/
create table CheckingAccountConstraint
(
   CustomerID           char(18) not null,
   BankName             varchar(50) not null comment 'ÒøÐÐÃû',
   AccountID            varchar(18) not null,
   primary key (CustomerID, BankName),
   constraint fk_checkingaccountconstraint_customer Foreign Key(CustomerID) references Customer(CustomerID) ON UPDATE CASCADE,
   constraint fk_checkingaccountconstraint_bank Foreign Key(BankName) references Bank(BankName),
   constraint fk_checkingaccountconstraint_acount Foreign Key(AccountID) references Account(AccountID)
);
/*==============================================================*/
/* Table: LoanOfAccount                                           */
/*==============================================================*/
/*
create table LoanOfAccount
(
   AccountID            varchar(18) not null,
   LoanID               varchar(20) not null,
   primary key (AccountID, LoanID),
   constraint fk_loanofaccount_acount Foreign Key(AccountID) references Account(AccountID),
   constraint fk_loanofaccount_loan Foreign Key(LoanID) references Account(LoanID)
);
*/
/*==============================================================*/
/* Table: Loan                                                  */
/*==============================================================*/
create table Loan
(
   BankName             varchar(50) not null,
   AccountID			varchar(18) not null,
   LoanID               varchar(20) not null,
   LoanSum              double(15,2) not null,
   LoanState				smallint not null,
   LoanDate				datetime not null,
   primary key (LoanID),
   constraint fk_loan_bank Foreign Key(BankName) references Bank(BankName),
   constraint fk_loan_account Foreign Key(AccountID) references Account(AccountID)
);

/*==============================================================*/
/* Table: OfferMoney                                            */
/*==============================================================*/
create table OfferMoney
(
   LoanID               varchar(20) not null,
   OfferID              varchar(20) not null,
   OfferDate            datetime not null,
   OfferSum             double(15,2) not null,
   primary key (LoanID, OfferID),
   constraint fk_offermoney_loan Foreign Key(LoanID) references Loan(LoanID)
);

insert into Bank(BankName,City,BankAssets) values
	("USTC WEST", "合肥", 100000000.0),
    ("USTC EAST", "合肥", 500000000.0),
    ("USTC MIDDLE", "合肥", 500000000.0);

insert into Staff(StaffID,BankName,DepartmentID,StaffName,StaffPhone,StaffAddress, StartDate) values 
	("001", "USTC WEST", null, "张三", "001", "合肥市中国科学技术大学西校区",now()),
    ("002", "USTC WEST", null, "李四", "002", "合肥市中国科学技术大学西校区",now()),#![feature(renamed_spin_loop)]
    ("003", "USTC EAST", null, "王五", "003", "合肥市中国科学技术大学东校区",now()),
    ("004", "USTC EAST", null, "赵六", "004", "合肥市中国科学技术大学东校区",now()),
    ("005", "USTC MIDDLE", null, "孙七", "005", "合肥市中国科学技术大学中校区",now()),
    ("006", "USTC MIDDLE", null, "郑八", "006", "合肥市中国科学技术大学中校区",now());

insert into Department(DepartmentID,BankName,ManagerID,DepartmentName,DepartmentType) values
	("001", "USTC WEST", "001", "财务", "金融"),
    ("002", "USTC EAST", "003", "财务", "金融"),
    ("003", "USTC MIDDLE", "005", "财务", "金融");


insert into Account(AccountID)
	values
    ("000000001"),
    ("000000002"),
    ("000000003"),
    ("000000004"),
    ("000000005");

insert into SavingAccount(AccountID, BankName,Balance,OpenDate,Rate,CurrencyType) 
	values
    ("000000001", "USTC WEST", 1000, "2021-6-15", 0.005, "CNY"),
    ("000000002", "USTC EAST", 1000, "2021-6-16", 0.006, "CNY"),
    ("000000003", "USTC MIDDLE", 1000, "2021-6-17", 0.007, "CNY"),
    ("000000004", "USTC WEST", 1000, "2021-6-18", 0.008, "CNY"),
    ("000000005", "USTC EAST", 1000, "2021-6-19", 0.009, "CNY");


insert into Loan(BankName,AccountID,LoanID,LoanSum,LoanState,LoanDate)
	values
    ("USTC EAST", "000000001", "100000000", 1000, 0, "2021-6-15"),
    ("USTC WEST", "000000001", "200000000", 1000, 0, "2021-6-16"),
    ("USTC MIDDLE", "000000002", "300000000", 1000, 0, "2021-6-17"),
    ("USTC EAST", "000000003", "400000000", 1000, 0, "2021-6-18"),
    ("USTC EAST", "000000004", "500000000", 1000, 0, "2021-6-19");

update Staff set DepartmentID="001" where StaffID="001" or StaffID="002";
update Staff set DepartmentID="002" where StaffID="003" or StaffID="004";
update Staff set DepartmentID="003" where StaffID="005" or StaffID="006";
