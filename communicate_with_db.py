from sqlalchemy.orm import Session
from .database import User, engine, Event
import json



session = Session(engine)

def get_user_by_nickname(value: any):
    user = session.query(User).where(User.nickname ** value).first()
    return user


def add_item_to_db(obj):
    session.add(obj)
    session.commit()

def create_json(object : object):
    converted = object.__dict__
    converted.pop('_sa_instance_state', None)
    # converted["time"] = converted["time"].strftime("%H:%M")
    # converted["data"] = converted["data"].strftime("%Y-%m-%d")
    print(converted, "converted object")
    jsoned_dict = json.dumps(converted)
    return jsoned_dict

def get_events_for_current_user_by(date, user):
    events = session.query(Event).filter(Event.date == date, Event.user == user).all()#Event.date == date, Event.user == user
    jsnonified = []
    for event in events:
        print(event)
        jsnonified.append(create_json(event))
        return jsnonified

def get_user_by(email):
    return session.query(User).filter(User.email == email).first()

def delete_user_events_by(email):
    user = get_user_by(email)
    if user:
        session.query(Event).filter(Event.user == user.id).delete()
        session.commit()


def delete_user_using(email):
    user = get_user_by(email)
    if user:
        session.delete(user)
def delete_event_using(header, user):
    session.query(Event).filter(Event.header == header, Event.user == user).delete()