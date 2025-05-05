from fastapi import UploadFile, HTTPException
from PIL import Image
from io import BytesIO


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
        