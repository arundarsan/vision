import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : 'https://face-recognition-36ef1-default-rtdb.firebaseio.com/'
    })

ref = db.reference('database-1')
data = {
        '1234': {
                    'name': 'Pejman',
                    'age' : '23'

            },
        '2345' : {
                    'name': 'Immanuel',
                    'age' : '23'
            },
        '777' : {
                    'name' : 'Arun',
                    'age'  : '25'
            }
        }
for key,value in data.items():
    ref.child(key).set(value)

