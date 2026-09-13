from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

#Routers
app.include_router(post.router)
app.include_router(user.router)

# JWT auth: token lives on the client, not stored on the API/backend.

# Login flow:
# Client -> API: /login (email + password)
# API checks credentials, creates a JWT, sends it back

# Using it:
# Client -> API: /posts + {token}
# API checks if the token is valid, sends data back if yes

# JWT structure:
# Header: alg (hash algorithm), typ (JWT). Almost always the same.
# Payload: the actual data/claims. Readable by anyone, not encrypted.
#   Technically editable too, but editing it breaks the signature.
# Signature: made from header + payload + secret key. Can't be faked
#   without the secret, so tampering gets caught.

# Not encrypted = anyone can read it. Signed = anyone can tell if it's fake.