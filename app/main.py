from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello!"}


# List of domains allowed to talk to your API
origins = ["*"]

# Attach the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, PATCH, etc.)
    allow_headers=["*"], # Allows all headers
)

# routers go here (e.g., app.include_router(post.router)


#Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

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


# How Voting and Likes System works:
# logged in users should be able to like a post.
# the user should be able to like a post once.
# GET post should fetch the total number of likes.
# in a relational DB, it's a many-to-many relationship  


# CORS