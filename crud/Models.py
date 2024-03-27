from pydantic import BaseModel

class UserCreate(BaseModel):
    google_uid: str
    email: str

class ChordCreate(BaseModel):
    chord_fingering: str
    chord_type: str

class ChordPlayed(BaseModel):
    player_id: str
    chord_ids: list[int]
    chord_root_positions: list[int]

class BetaTestingInput(BaseModel):
    experience: str
    hope: str
    google_uid: str

class Email(BaseModel):
    email: str