from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'])


def gerar_hash(texto_plano):
    return pwd_context.hash(texto_plano)


def verifcar_hask(texto_plano, hash_plano):
    return  pwd_context.verify(texto_plano, hash_plano)