import os
import sys
sys.path.append(os.path.dirname(os.path.abspath('D:/Work/Gre/UTD/Courses/Winter/Projects/LLM/LLM_Fine_Tuning/LLM_Fine_Tuning/MultiModal_GenProject/app/models.py')))
from fastapi import FastAPI, Query, status, Response
from starlette.responses import StreamingResponse
from .models import load_text_model, generate_text, load_audio_model, generate_audio, load_image_model, generate_image
from .utils import audio_array_to_buffer
import uvicorn
from schemas import VoicePresets
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/generate/text")
def serve_language_model_controller(prompt=Query(...)):
    pipe = load_text_model()
    output = generate_text(pipe, prompt)
    return {"response": output}

@app.get(
    "/generate/audio",
    responses={status.HTTP_200_OK: {"content": {"audio/wav": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_audio_model_controller(
    prompt=Query(...),
    preset: VoicePresets = Query(default="v2/en_speaker_1"),
):
    processor, model = load_audio_model()
    output, sample_rate = generate_audio(processor, model, prompt, preset)
    return StreamingResponse(audio_array_to_buffer(output, sample_rate), media_type="audio/wav")

@app.get("/generate/image",
         responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
         response_class=Response)

def serve_text_to_image_model_controller(prompt=Query(...)):
    pipe = load_image_model()
    output = generate_image(pipe, prompt)
    return Response(content=img_to_bytes(output), media_type="image/png")

@app.get("/", include_in_schema=False)
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)


if __name__ == "__main__":
    uvicorn.run("App.main:app", port=8000, reload=True)
