from datetime import datetime

from . import BasePydanticModel
from .transcription import TokenUsageModel


class ParticipantModel(BasePydanticModel):
    id: str
    name: str
    role: str
    isHost: bool
    additionalNotes: str


class CallDetailsModel(BasePydanticModel):
    date: datetime
    callType: str
    notes: str
    participants: list
    notetype: list
    minutes_elapsed: float
    title: str
    transcription: dict
    token_usage: TokenUsageModel
