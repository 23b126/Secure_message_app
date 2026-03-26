from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Crypto.Cipher import AES
import base64, os

app = FastAPI()

# Static files and templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("encrypt.html", {"request": request})

# AES encryption helper
def encrypt_message(message: str, key: str):
    key_bytes = key.encode("utf-8")
    cipher = AES.new(key_bytes, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode("utf-8"))
    return (base64.b64encode(cipher.nonce).decode("utf-8"),
            base64.b64encode(ciphertext).decode("utf-8"))

# AES decryption helper
def decrypt_message(ciphertext_b64: str, nonce_b64: str, key: str):
    key_bytes = key.encode("utf-8")
    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    cipher = AES.new(key_bytes, AES.MODE_EAX, nonce=nonce)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted.decode("utf-8")

# Route for encryption form
@app.get("/encrypt", response_class=HTMLResponse)
async def get_encrypt_form(request: Request):
    return templates.TemplateResponse("encrypt.html", {"request": request})

# Handle encryption form submission
@app.post("/encrypt", response_class=HTMLResponse)
async def post_encrypt(request: Request, message: str = Form(...), key: str = Form(...)):
    try:
        nonce, ciphertext = encrypt_message(message, key)
        result = f"Ciphertext: {ciphertext}\nNonce: {nonce}"
    except Exception as e:
        result = f"Error: {e}"
    return templates.TemplateResponse("encrypt.html", {"request": request, "result": result})

# Route for decryption form
@app.get("/decrypt", response_class=HTMLResponse)
async def get_decrypt_form(request: Request):
    return templates.TemplateResponse("decrypt.html", {"request": request})

# Handle decryption form submission
@app.post("/decrypt", response_class=HTMLResponse)
async def post_decrypt(request: Request, ciphertext: str = Form(...), nonce: str = Form(...), key: str = Form(...)):
    try:
        decrypted = decrypt_message(ciphertext, nonce, key)
        result = f"Decrypted Message: {decrypted}"
    except Exception as e:
        result = f"Error: {e}"
    return templates.TemplateResponse("decrypt.html", {"request": request, "result": result})
