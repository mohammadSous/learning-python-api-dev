from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

#Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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


# Logging In User.
# Hit the login endpoint with email and password

# Find the user by email
# If no user with that email exists, reject the login

# Check the password (it's stored hashed, not plain text)
# Can't "unhash" it, so instead: hash the attempted password
# using the same salt as the stored hash, then compare the two hashes
# If they match, the password is correct

# If both checks pass, create and return a JWT