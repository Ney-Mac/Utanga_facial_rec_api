from fastapi import UploadFile, HTTPException
from PIL import Image
from io import BytesIO


MAX_IMAGE_SIZE_MB = 3
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024


async def load_image(image: UploadFile):
    if not image.filename.lower().endswith((".jpeg", ".jpg", ".png")):
        raise HTTPException(status_code=400, detail="Formato de imagem inválido.")

    img_content = await image.read()

    try:
        img = Image.open(BytesIO(img_content))
        img.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="O arquivo não é uma imagem válida.")

    return img_content
        
async def carregar_e_validar_imagem(image: UploadFile):
    if not image.filename.lower().endswith((".jpeg", ".jpg", ".png")):
        raise HTTPException(status_code=400, detail="Formato de imagem inválido.")

    img_content = await image.read()
    
    if len(img_content) > MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail=f"A imagem excede o tamanho máximo permitido de {MAX_IMAGE_SIZE_MB} MB.")
    
    try:
        img = Image.open(BytesIO(img_content))
        img.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="O arquivo não é uma imagem válida.")

    return img_content
    