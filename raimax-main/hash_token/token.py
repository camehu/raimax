'''from jose import JWTError, jwt
import datetime

payload_data = {
        "sub": "001",
        "name": 'Carlos',
        "nickname": "carlosa",
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=60)
    }
my_secret = 'my_super_secret'

token = jwt.encode(claims=payload_data, key=my_secret, algorithm='HS512')


print(token)'''
