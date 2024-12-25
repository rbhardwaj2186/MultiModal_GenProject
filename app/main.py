import os
import sys
sys.path.append(os.path.dirname(os.path.abspath('D:/Work/Gre/UTD/Courses/Winter/Projects/LLM/LLM_Fine_Tuning/LLM_Fine_Tuning/MultiModal_GenProject/app/models.py')))
from fastapi import FastAPI, Query, status, Response
from starlette.responses import StreamingResponse, JSONResponse
from .models import load_text_model, generate_text, load_audio_model, generate_audio, load_image_model, generate_image
from .utils import audio_array_to_buffer
import uvicorn
from schemas import VoicePresets
from video_models import VideoEnhancementModel, preprocess_frame, postprocess_frame
from schemas import ProcessingConfig
from fastapi.responses import RedirectResponse
import cv2
import torch
app = FastAPI()

model = VideoEnhancementModel()
model.eval()

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


@app.post("/enhance-video/")
async def enhance_video(video: UploadFile = File(...), config: ProcessingConfig = ProcessingConfig()):
    try:
        temp_file = "temp_video.mp4"
        with open(temp_file, "wb") as f:
            f.write(await video.read())

        cap = cv2.VideoCapture(temp_file)
        frame_count, fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), int(cap.get(cv2.CAP_PROP_FPS))
        processed_frames, frame_number = [], 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_number % config.frame_skip == 0:
                input_tensor = preprocess_frame(frame)
                with torch.no_grad():
                    enhanced = model(input_tensor) * config.enhancement_level
                processed_frames.append(postprocess_frame(enhanced))
            frame_number += 1

        cap.release()
        return JSONResponse(content={"status": "success", "frames_processed": len(processed_frames), "fps": fps})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run("App.main:app", port=8000, reload=True)
