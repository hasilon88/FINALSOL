from CRUD import *
from security import *
import uvicorn
import base64;
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request
import random
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# --- Code to prevent DDOS attacks --- 
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(RateLimitExceeded)
async def ratelimit_exception(request: Request, exc: RateLimitExceeded):
    return HTTPException(detail="Too Many Requests", status_code=429)

@app.get("/rate-limited/")
@limiter.limit("5/minute")
async def read_root(request: Request):
    return {"message": "test"}
# ---

# Fix a common problem with CORE ---
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---

verification_codes = {}

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_email(recipient_email, verification_code):
    sender_email = "hasilonjr@gmail.com"  # Enter your address
    sender_password = "ksfl syii rbzg ayva"
    
    subject = "Your verification code"
    body = f"Your verification code is: {verification_code}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

@app.post("/start-verification/")
async def start_verification(email: str):
    code = generate_verification_code()
    verification_codes[email] = code
    send_email(email, code)
    return {"message": "Verification code sent to the provided email."}

@app.post("/verify-email/")
async def verify_email(email: str, code: str):
    expected_code = verification_codes.get(email)
    if not expected_code:
        raise HTTPException(status_code=404, detail="Email not found.")
    
    if expected_code == code:
        # You can add more logic here, like activating the user's account.
        return {"message": "Verification successful!"}
    else:
        return {"message": "Incorrect verification code."}

# Main server
@app.post("/create_user/")
async def createUser(userData: dict):
    requiredKeys = ["name", "email", "password"]
    for key in requiredKeys:
        if key not in userData:
            raise HTTPException(status_code=400, detail=f"Key {key} is missing")

    encryptedEmail = encryptString(userData.get("email"), "ascii_maps/ascii_mapping.json")
    
    salt = generate_salt()

    password  = encryptPassword(userData.get("password"), salt)

    keyPair = generateKeyPair()
    keyPair = convertKeyPairToStr(keyPair)

    privateKey = base64.b64encode(keyPair.get("str_private_key"))
    publicKey = base64.b64encode(keyPair.get("str_public_key"))

    addUser(createConnection(), userData.get("name"), encryptedEmail, password, privateKey, publicKey, salt)

    return {"message": "User successfully created", "user": userData}


@app.post("/create_message/")
async def createMessage(messageData: dict):
    requiredKeys = ["email", "receiverId", "content"]
    for key in requiredKeys:
        if key not in messageData:
            raise HTTPException(status_code=400, detail=f"Key {key} is missing")
    
    email = encryptString(messageData.get("email"), "ascii_maps/ascii_mapping.json")
    user = getUserByAttribute(createConnection(), "email", email)
    
    # receiverPublicKey = getUserByAttribute(createConnection(), "id", messageData.get("receiverId")).get("public_key")
    # receiverPublicKey = convertStrPublicKeyToKey(receiverPublicKey)

    # content = encryptWithPublicKey(messageData.get("content"), receiverPublicKey)
    content = messageData.get("content")

    addMessage(createConnection(), user.get("id"), messageData.get("receiverId"), content)

    return {"message": "Message successfully sent", "messageData": messageData}

@app.post("/validate_user/")
def validate_user(userData: dict):
    requiredKeys = ["email", "password"]
    for key in requiredKeys:
        if key not in userData:
            raise HTTPException(status_code=400, detail=f"Key {key} is missing")
    
    
    user = getUserByAttribute(createConnection(), "email", encryptedEmail)
    encryptedEmail = encryptString(userData.get("email"), "ascii_maps/ascii_mapping.json")

    password = encryptPassword(userData.get("password"), user.get("salt"))

    if password == user.get("password"):
        return {"status": "success"}
    
    return {"status": "failure", "message": "Invalid credentiels"}

@app.get("/get_convo/{userEmail}/{userPassword}/")
def getConvos(userEmail: str, userPassword: str):

    userEmail = encryptString(userEmail, "ascii_maps/ascii_mapping.json")

    password = encryptString(userPassword, "ascii_maps/ascii_mapping.json")
    password = hash(password)
    password = encryptString(password, "ascii_maps/ascii_mapping2.json")

    user = getUserByAttribute(createConnection(), "email", userEmail)

    if user.get("password") != password:
        return{"error": "incorret credentiels"}
    
    privateKey = user.get("private_key")
    receivedChats = getMessagesByReceiverId(createConnection(), user.get("id"))
    sentChats = getSentMessagesBySenderId(createConnection(), user.get("id"))

    privateKey = convertStrPrivateKeyToKey(privateKey)

    # list = []
    # for message in receivedChats:
    #     list.append(decryptWithPrivateKey(message, privateKey))

    return {"received_messages": receivedChats, "sent_messages": sentChats}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
