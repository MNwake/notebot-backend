from typing import List

from pydantic import BaseModel

from database import TokenUsage


class UtteranceModel(BaseModel):
    speaker: str
    start: int
    end: int
    text: str
    confidence: float

class TranscriptionResponseModel(BaseModel):
    utterances: List[UtteranceModel]


class TokenUsageModel(BaseModel):
    transcription_cost: float
    input_cost: float
    output_cost: float
    total_cost: float

    def save(self):
        token_usage = TokenUsage(
            transcription_cost=self.transcription_cost,
            input_cost=self.input_cost,
            output_cost=self.output_cost,
            total_cost=self.total_cost
        )
        token_usage.save()
        return token_usage
