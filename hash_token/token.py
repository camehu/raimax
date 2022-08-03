from jose import JWTError, jwt
import datetime


def token(sub, nome, apelido):
    payload_data = {
        "sub": sub,
        "name": nome,
        "nickname": apelido,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=60)
       }
    my_secret = 'my_super_secret'
    token = jwt.encode(claims=payload_data, key=my_secret, algorithm='HS512')
    return token


def decoToken(tokem):
    try:
      my_secret = 'my_super_secret'
      TKN = jwt.decode(tokem, key= my_secret, algorithms=["HS256"])
      return TKN

    except jwt.ExpiredSignatureError:
        print('Senha expirou')