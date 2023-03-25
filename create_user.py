from database import User,session,Event
from communicate_with_db import add_item_to_db
from werkzeug.security import generate_password_hash

# pwd = generate_password_hash("admin")
# admin = User("admin", "admin@admin.com", pwd)
# add_item_to_db(admin)
#
# usr = session.query(User).where(User.nickname == "admin").first().email
# print(usr)
events = session.query(Event).all()
for i in events:
    print(i.date)
