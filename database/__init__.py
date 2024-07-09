from mongoengine import connect
import os
try:
    print("connect db")
    #connect(host="mongodb://my_user:my_password@127.0.0.1:27017/my_db?authSource=my_db")
    connect(
        host=os.getenv("database")
    )
    print("connect db succes")
except:
    print("connect db error")