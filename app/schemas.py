# schemas.py
from typing import Literal
from pydantic import BaseModel

VoicePresets = Literal["v2/en_speaker_1", "v2/en_speaker_9"]

class ProcessingConfig(BaseModel):
    enhancement_level: float = 1.0
    frame_skip: int = 1