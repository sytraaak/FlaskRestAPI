from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
import csv
import datetime
import sqlite3

#sql alchemy
db = create_engine("sqlite:///users.db",
                   echo=True,
                   connect_args={'check_same_thread': False})
Base = declarative_base(db)
Session = sessionmaker(bind=db)

#sqlite
connection = sqlite3.connect("users.db", check_same_thread=False)
cursor = connection.cursor()

db_password = 1385321

class Statistics(Base):
    __tablename__ = "statistics"
    date = Column(DateTime, primary_key=True)
    user_name = Column(String)
    iss = Column(Integer)
    rez = Column(Integer)
    fraud = Column(Integer)
    canceled = Column(Integer)
    lowcost = Column(Integer)

class User(Base):
    __tablename__ = "users"
    user_name = Column(String, primary_key=True, unique=True)
    iss = Column(Integer)
    rez = Column(Integer)
    fraud = Column(Integer)
    canceled = Column(Integer)
    lowcost = Column(Integer)
    svcb_login = Column(Integer, unique=True)

class Fraud(Base):
    __tablename__ = "fraud_emails"
    email = Column(String, primary_key=True, unique=True)

class QueueCount(Base):
    __tablename__ = "Q_80"
    date = Column(DateTime, primary_key=True, unique=True)
    value = Column(Integer)

class MorningStats(Base):
    __tablename__ = "morning_stats"
    date = Column(DateTime, primary_key=True, unique=True)
    user_name = Column(String)
    iss = Column(Integer)
    rez = Column(Integer)
    fraud = Column(Integer)
    canceled = Column(Integer)
    lowcost = Column(Integer)

session = Session()

#TODO filtrování řádků podle data
def filter_by_date(date_from, date_to):
    start = datetime.datetime.strptime(date_from, "%d.%m.%y").date()
    end = datetime.datetime.strptime(date_to, "%d.%m.%y").date()
    all_rows = session.query(Statistics).all()
    count_iss, count_rez, count_lowcost, count_canceled, count_fraud = 0, 0, 0, 0, 0

    with open(f"temporary_data/filtered_statistics.xls", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, dialect="excel")
        header = ["Date", "Name", "Issued", "Reservation", "Lowcost", "Canceled", "Fraud"]
        writer.writerow(header)
        for row in all_rows:
            date = row.date.date()
            if start <= date <= end:
                row_list = [str(date), row.user_name, row.iss, row.rez, row.lowcost, row.canceled, row.fraud]
                count_iss += row.iss
                count_rez += row.rez
                count_lowcost += row.lowcost
                count_canceled += row.canceled
                count_fraud += row.fraud
                writer.writerow(row_list)
        writer.writerow(["", "Součty: ", count_iss, count_rez, count_lowcost, count_canceled, count_fraud])

def save_morning_stats():
    users_from_db = session.query(User).all()
    for user in users_from_db:
        session.add(MorningStats(date=datetime.datetime.now(), user_name=user.user_name, iss=user.iss, rez=user.rez,
                               fraud=user.fraud, canceled=user.canceled, lowcost=user.lowcost))
        session.commit()
    return ["Ranní statistiky uloženy do databáze"]


def queue_80_check():
    today = str(datetime.datetime.today())
    new_today = datetime.datetime.strptime(today[0:11] + "00:00:00.000000", "%Y-%m-%d %H:%M:%S.%f")

    if session.query(QueueCount).filter_by(date=new_today).first() is not None:
        session.close()
        return [True]
    else:
        session.close()
        return [False]


def queue_80_add(reservation_on_queue):
    today = datetime.datetime.today().date()
    session.add(QueueCount(date=today, value=reservation_on_queue))
    session.commit()
    session.close()
    return [f"Počet rezervací na Q80 k dnešnímu dni zapsán: {reservation_on_queue}"]

#todo toto je nepoužito a nefunkční
def repeat_80_check(reservation_on_queue):
    today = datetime.datetime.today().date()
    session.add(QueueCount(date=today, value=reservation_on_queue))
    session.commit()
    session.close()
    return [f"Počet rezervací na Q80 k dnešnímu dni zapsán: {reservation_on_queue}"]

def fraud_emails():
    """
    load all fraud email from db
    :return: list
    """
    mail_list = [email.email for email in session.query(Fraud).all()]
    return mail_list

def add_fraud(fraud_email):
    if session.query(Fraud).filter_by(email=fraud_email.lower()).first() is None:
        session.add(Fraud(email=fraud_email.lower()))
        session.commit()
        return [f"Fraud email {fraud_email} přidán do databáze"]
    else:
        return [f"CHYBA: Email {fraud_email} se již nachází v databázi podezřelých mailů"]

def del_fraud(fraud_email):
    if session.query(Fraud).filter_by(email=fraud_email.lower()).first() is not None:
        email_in_db = session.query(Fraud).filter_by(email=fraud_email.lower())
        email_in_db.delete()
        session.commit()
        return [f"E-mail {fraud_email} smazán z databáze podezřelých mailů"]
    else:
        return [f"CHYBA: E-mail {fraud_email} se v databázi nenachází"]

def statistics():
    """
    shows actual daily statistics of users
    :return: list
    """
    users_from_db = session.query(User).all()
    users_stats = []
    for user in users_from_db:
        users_stats.append(f"""{user.user_name}:\nVystaveno: {user.iss}\nNevystaveno: {user.rez}\nKradaci: {user.fraud}\nZrusene: {user.canceled}\nLowcost: {user.lowcost}\n""")
    return users_stats

def save_stats():
    """
    Saves data to statistics table with date of creation
    Can be used to long term statistics
    Also resets daily statistics
    """
    users_from_db = session.query(User).all()
    for user in users_from_db:
        session.add(Statistics(date=datetime.datetime.now(), user_name=user.user_name, iss=user.iss, rez=user.rez,
                               fraud=user.fraud, canceled=user.canceled, lowcost=user.lowcost))
        session.commit()
    users_from_db = session.query(User).all()
    for user in users_from_db:
        user.rez = 0
        user.iss = 0
        user.fraud = 0
        user.lowcost = 0
        user.canceled = 0
    session.commit()

def filter_database(date_from, date_to):
    start = datetime.datetime.strptime(date_from, "%d.%m.%y").date()
    end = datetime.datetime.strptime(date_to, "%d.%m.%y").date()

    database_stats = []
    database_dict = {}
    rows = session.query(Statistics).all()
    for record in rows:
        row_date = record.date.date()
        if start <= row_date <= end:
            if record.user_name not in database_dict:
                database_dict[record.user_name] = {"iss": record.iss,
                                                   "rez": record.rez,
                                                   "fraud": record.fraud,
                                                   "canceled": record.canceled,
                                                   "lowcost": record.lowcost}
            else:
                for key in database_dict[record.user_name].keys():
                    database_dict[record.user_name][key] += eval(f"record.{key}")
    for user in database_dict:
        database_stats.append(user)
        for record in database_dict[user]:
            database_stats.append(f"{record}: {database_dict[user][record]}")
        database_stats.append("\n")
    return database_stats

def get_count_of(name: str, search_for: str):
    """
    used in setter function to get information who has got minimum of reservation type
    :param name: user name fe Jan Burda (with space)
    :param search_for: iss, rez, fraud, canceled, lowcost
    :return: count of name's count for
    """
    user = session.query(User).filter_by(user_name=name).one()
    return eval(f"user.{search_for}")

def add_user(name: str, svcb_number: int, password: int):
    if password == db_password:
        if session.query(User).filter_by(user_name=name).first() is None:
            session.add(User(user_name=name, iss=0, rez=0, fraud=0, canceled=0, lowcost=0, svcb_login=svcb_number))
            Base.metadata.create_all(db)
            session.commit()
            return [f"Vytvořen uživatel {name}"]
        else:
            return ["Uživatel s tímto jménem již existuje"]
    else:
        return ["Zadali jste chybné heslo"]

def all_users():
    """
    Loads list of all employees
    :return: list of users
    """
    session = Session()
    users = [user.user_name for user in session.query(User).all()]
    return users

def all_users_info(search_for: str):
    """
    :param search_for: iss, rez, fraud, canceled, lowcost
    :return: count of search for of all users
    """
    users_from_db = session.query(User).all()
    for user in users_from_db:
        print(eval(f"user.{search_for}"))

def update_user(name: str, update_what: str):
    user = session.query(User).filter_by(user_name=name).one()
    if update_what == "iss":
        user.iss += 1
    elif update_what == "rez":
        user.rez += 1
    elif update_what == "fraud":
        user.fraud += 1
    elif update_what == "canceled":
        user.canceled += 1
    elif update_what == "lowcost":
        user.lowcost += 1
    session.commit()
    print(eval(f"user.{update_what}"))

def delete_user(name: str, password: int):
    if password == db_password:
        if session.query(User).filter_by(user_name=name).first() is not None:
            user = session.query(User).filter_by(user_name=name)
            user.delete()
            session.commit()
            return [f"Uživatel {name} smazán"]
        else:
            return ["Tento uživatel neexistuje"]
    else:
        return ["Zadali jste chybné heslo"]



Base.metadata.create_all(db)

# todo testy

filter_by_date("3.10.22", "4.10.22")












