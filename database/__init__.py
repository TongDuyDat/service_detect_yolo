from mongoengine import connect
try:
    username = 'dattongduy10'
    password = 'TongDat1.'
    hostname = 'cluster0.tcvgnb2.mongodb.net'
    database_name = 'image_caption'
    print("connect db")
    #connect(host="mongodb://my_user:my_password@127.0.0.1:27017/my_db?authSource=my_db")
    connect(
        host="mongodb+srv://dattongduy10:TongDat1.@cluster0.tcvgnb2.mongodb.net/image_caption"
    )
    print("connect db succes")
except:
    print("connect db error")
    
#mongodb+srv://dattongduy10:TongDat1.@cluster0.tcvgnb2.mongodb.net/