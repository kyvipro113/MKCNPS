from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text
from sqlalchemy.sql import elements

class Account_Info(declarative_base()):
    __tablename__ = "ACCOUNT_INFO"
    __table_args__ = {"schema": "MKCNP"}

    uid = Column(elements.quoted_name("UID", True), String, primary_key=True)
    email = Column(elements.quoted_name("EMAIL", True), String)
    pwd = Column(elements.quoted_name("PWD", True), String)
    phone_number = Column(elements.quoted_name("PHONE_NUMBER", True), String)
    username_link = Column(elements.quoted_name("USERNAME_LINK", True), String)
    language = Column(elements.quoted_name("LANGUAGE", True), String)
    status = Column(elements.quoted_name("STATUS", True), String)
    act_login_by_phone_number = Column(elements.quoted_name("ACT_LOGIN_BY_PHONE_NUMBER", True), String)
    first_login = Column(elements.quoted_name("FIRST_LOGIN", True), String)