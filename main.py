import os
from random import randint
from mangum import Mangum
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
import bcrypt
from mangum import Mangum

from tooling import process_progression
from crud.CreateSession import SessionLocal
from crud.Models import Email, User, UserEmail, UserVerify, UserResetPassword, ChordCreate, ChordPlayed, BetaTestingInput
from crud.Chords import get_chord_shapes, get_chords_played
from crud.Email import send_email

app = FastAPI()

# Allow all origins (replace '*' with the specific origin you want to allow)
origins = ["http://localhost:3000", "https://voicingvault.web.app", "https://voicingvault.com", "voicingvault.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.post('/create-user')
async def create_user(data: User, db: Session=Depends(get_db)):
    """
    Create a temporary user with email and password

    @return True if the user creation was a success and false otherwise
    """
    print('what up')
    salt = bcrypt.gensalt()

    # Hash the password and convert to hex (for storage)
    hashed_password = bcrypt.hashpw(
        password=data.password.encode(),
        salt=salt
    ).hex()

    insert = text("INSERT INTO users (email, password) VALUES (:email, :password)")
    params = {'email': data.email, 'password': hashed_password}

    try:
        db.execute(insert, params)
        db.commit()
        return True
    except:
        db.rollback()
        # There's already a user with that email. Check if the user is verified
        query = text("SELECT verified FROM users WHERE email = :email")
        params = {'email': data.email}
        try:
            result = db.execute(query, params)
            user = result.fetchall()[0]
            print(user)
            if user.verified:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "A user with that email already exists"
                    },
                )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": str(e)
                },
            )
        
        # The user isn't verified, update the password
        update = text("UPDATE users SET password = :password WHERE email = :email")
        params = {'email': data.email, 'password': hashed_password}
        try:
            db.execute(update, params)
            db.commit()
            return True
        except:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Error creating user"
                },
            )


@app.post('/create-verification-code')
async def create_verification_code(data: UserEmail, db: Session=Depends(get_db)):
    """
    Create a 6 digit verification code (randomly)
    set it to the verification code field in the user table
    and send an email to the user with the verification code
    """
    # Generate random 6 digit code (as a string)
    code = str(randint(100000, 999999))

    # Update the users table to have the code
    update = text("UPDATE users SET verification_code = :code WHERE email = :email")
    params = {'code': code, 'email': data.email}

    try:
        db.execute(update, params)
        db.commit()
    except:
        db.rollback()

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Error creating verification code"
            },
        )
    
    # Email the user the new code
    subject = 'VoicingVault Verification Code'
    message = 'Your 6-digit verification code is ' + code
    try:
        await send_email(data.email, subject, message)
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Error sending verification code"
            },
        )
    
    return True


@app.post('/verify-user')
async def verify_user_with_code(data: UserVerify, db: Session=Depends(get_db)):
    """
    Check that the code equals the code stored in the db for user
    """
    query = text("SELECT verification_code FROM users WHERE email = :email")
    params = {'email': data.email}

    try:
        result = db.execute(query, params)
        code = result.fetchone()
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "No user exists for that email"
            },
        )
    
    verification_code = code[0]
    if verification_code == data.code:
        update = text("UPDATE users SET verified = TRUE WHERE email = :email")
        
        try:
            db.execute(update, params)
            db.commit()
            return True
        except:
            db.rollback()
            
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Error verifying user"
                },
            )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Incorrect code"
        },
    )


@app.post('/login-user')
async def login_user(data: User, db: Session=Depends(get_db)):
    """
    Verify that the user credientials (username and password) are correct

    @return the user_id if the credentials are correct
    """
    query = text("""
        SELECT password, verified
        FROM users
        WHERE email = :email
    """)
    params = {'email': data.email}
    
    try:
        result = db.execute(query, params)
        user = result.fetchall()[0]
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "No user exists for that email"
            },
        )

    # Check the given password against the hashed password in the db
    check = bcrypt.checkpw(
        password=data.password.encode(),
        hashed_password=bytes.fromhex(user.password)
    )

    if check:
        # Make sure the user is verified
        verified = user.verified
        if verified:
            return {
                'email': data.email
            }
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "User is not verified"
                },
            )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Incorrect password for username"
        },
    )


@app.post('/generate-password-reset-code')
async def generate_password_reset_code(data: UserEmail, db: Session=Depends(get_db)):
    # Generate a random 9 digit code and save as verification_code in the users table
    code = str(randint(100000000, 999999999))
    update = text("UPDATE users SET verification_code = :code WHERE email = :email")
    params = {'code': code, 'email': data.email}

    try:
        db.execute(update, params)
        db.commit()
    except:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Error generating temporary password"
            },
        )
    
    # Email the user the new code
    subject = 'VoicingVault Temporary Password'
    message = 'Your temporary password is ' + code
    try:
        await send_email(data.email, subject, message)
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Error sending temporary password"
            },
        )
    
    return True


@app.post('/reset-password')
async def reset_password(data: UserResetPassword, db: Session=Depends(get_db)):
    """
    Reset the password for a user if they enter the correct matching code
    """
    # Check that the code matches the temporary password in the user table
    query = text("SELECT verification_code FROM users WHERE email = :email")
    params = {'email': data.email}

    try:
        result = db.execute(query, params)
        code = result.fetchall()[0]
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "No user exists for that email"
            },
        )
    
    verification_code = code.verification_code
    if verification_code == data.code:
        # Update the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(
            password=data.password.encode(),
            salt=salt
        ).hex()

        update = text("UPDATE users SET password = :password WHERE email = :email")
        update_params = {'password': hashed_password, 'email': data.email}

        try:
            db.execute(update, update_params)
            db.commit()
            return True
        except:
            db.rollback()
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Error resetting password"
                },
            )
    
    return False




@app.get('/{chord_list}')
async def get_fingerings(chord_list: str, db: Session=Depends(get_db)):
    try:
        chords_as_list = chord_list.split(' ')
        c_major_shapes = get_chord_shapes(db)
        chord_fingerings = process_progression.process_chord_progression(chord_list=chords_as_list, c_major_shapes=c_major_shapes)
        return chord_fingerings
    except:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Error generating chord tablature"
                },
            )

@app.post('/create-chord')
async def create_chord(chord: ChordCreate, db: Session=Depends(get_db)):
    insert_sql = text("INSERT INTO chord_shape (chord_type, chord_fingering) VALUES (:chord_type, :chord_fingering)")
    params = {'chord_type': chord.chord_type, 'chord_fingering': chord.chord_fingering}
    db.execute(insert_sql, params)
    db.commit()

@app.post('/track-chord-played')
async def track_chord_played(played: ChordPlayed, db: Session=Depends(get_db)):
    # Create a chord progression played record
    prog_insert = text("INSERT INTO chord_progression_played (player_id) VALUES (:player_id) RETURNING id")
    params = {'player_id': played.player_id}
    result = db.execute(prog_insert, params)
    prog_id = result.fetchone()[0]

    for i in range(len(played.chord_ids)):
        insert_sql = text("INSERT INTO chord_played (chord_progression_played_id, chord_id, chord_root_pos) VALUES (:prog_id, :chord_id, :chord_root_pos)")
        params = {'prog_id': prog_id, 'chord_id': played.chord_ids[i], 'chord_root_pos': played.chord_root_positions[i]}
        db.execute(insert_sql, params)
        db.commit()


@app.get('/get-chords-played/{email}')
async def get_chords_pl(email: str, db: Session=Depends(get_db)):
    return get_chords_played(email, db)

"""
@app.post('/send-email')
async def send_me_email(beta_testing_input: BetaTestingInput, db: Session=Depends(get_db)):
    select_sql = text("SELECT email FROM player WHERE google_uid=:google_uid")
    result = db.execute(select_sql, {'google_uid': beta_testing_input.google_uid})
    email = result.fetchone()[0]
    total_message = email + ' wants to sign up with \n Experience: ' + beta_testing_input.experience + '\n They hope to: ' + beta_testing_input.hope
    await send_email(total_message)
"""

@app.post('/send-email')
async def send_me_email(email: Email):
    await send_email(os.getenv("EMAIL_ADDR"), email.subject, email.message)


handler = Mangum(app)