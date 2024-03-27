from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from mangum import Mangum

from tooling import process_progression
from crud.CreateSession import SessionLocal
from crud.Models import Email, UserCreate, ChordCreate, ChordPlayed, BetaTestingInput
from crud.Chords import get_chord_shapes, get_chords_played
from crud.Email import send_email

app = FastAPI()

# Allow all origins (replace '*' with the specific origin you want to allow)
origins = ["http://localhost:3000", "https://voicingvault.web.app"]

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

@app.get('/{chord_list}')
async def get_fingerings(chord_list: str, db: Session=Depends(get_db)):
    chords_as_list = chord_list.split(' ')
    c_major_shapes = get_chord_shapes(db)
    chord_fingerings = process_progression.process_chord_progression(chord_list=chords_as_list, c_major_shapes=c_major_shapes)
    return chord_fingerings

@app.post('/create-chord')
async def create_chord(chord: ChordCreate, db: Session=Depends(get_db)):
    insert_sql = text("INSERT INTO chord_shape (chord_type, chord_fingering) VALUES (:chord_type, :chord_fingering)")
    params = {'chord_type': chord.chord_type, 'chord_fingering': chord.chord_fingering}
    db.execute(insert_sql, params)
    db.commit()

@app.post('/create-player-user')
async def create_player(user: UserCreate, db: Session=Depends(get_db)):
    try:
        insert_sql = text("INSERT INTO player (google_uid, email) VALUES (:google_uid, :email)")
        params = {'google_uid': user.google_uid, 'email': user.email}
        db.execute(insert_sql, params)
        db.commit()
    except:
        print('User already in db')

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


@app.get('/get-chords-played/{google_uid}')
async def get_chords_pl(google_uid: str, db: Session=Depends(get_db)):
    return get_chords_played(google_uid, db)


@app.post('/send-email')
async def send_me_email(beta_testing_input: BetaTestingInput, db: Session=Depends(get_db)):
    select_sql = text("SELECT email FROM player WHERE google_uid=:google_uid")
    result = db.execute(select_sql, {'google_uid': beta_testing_input.google_uid})
    email = result.fetchone()[0]
    total_message = email + ' wants to sign up with \n Experience: ' + beta_testing_input.experience + '\n They hope to: ' + beta_testing_input.hope
    await send_email(total_message)


@app.post('/grant-access')
async def grant_access(email: Email, db: Session=Depends(get_db)):
    update_sql = text("UPDATE player SET access_approved=TRUE WHERE email=:email")
    db.execute(update_sql, {'email':email.email})
    db.commit()


@app.get('/has-access/{google_uid}')
async def has_access(google_uid: str, db: Session=Depends(get_db)):
    select_sql = text("SELECT access_approved FROM player WHERE google_uid=:google_uid")
    result = db.execute(select_sql, {'google_uid': google_uid})
    status = result.fetchone()[0]
    return status


handler = Mangum(app)