from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError


SECRET_KEY = "minha_chave_super_secreta"
ALGORITHM = "HS256"


def validar_token(authorization: str):
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token mal formatado.")
        
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tipo = payload.get("tipo")
        
        if tipo not in ['adm', 'prof']:
            raise HTTPException(status_code=403, detail="Acesso negado.")
        
        return payload
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
