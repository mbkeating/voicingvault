from pydantic import BaseModel

class ChordQuery(BaseModel):
    chord_list: list[str]
    allowed_strings: list[bool] = [True, True, True, True, True, True]
    min_fret: int
    max_fret: int


class User(BaseModel):
    email: str
    password: str


class UserEmail(BaseModel):
    email: str


class UserVerify(BaseModel):
    email: str
    code: str


class UserResetPassword(BaseModel):
    email: str
    code: str
    password: str


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
    subject: str
    message: str