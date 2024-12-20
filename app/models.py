# models.py
import os
import torch
from transformers import Pipeline, pipeline
from huggingface_hub import login
from typing import Literal
from transformers import AutoProcessor, AutoModel
from schemas import VoicePresets
from getpass import getpass
from dotenv import load_dotenv
from diffusers import DiffusionPipeline, StableDiffusionInpaintPipelineLegacy
from PIL import Image
import numpy as np

prompt = "How to set up a FastAPI project?"
system_prompt = """
Your name is FastAPI bot and you are a helpful
chatbot responsible for teaching FastAPI to your users.
Always respond in markdown.
"""

def load_text_model():
    """
    Load the Hugging Face pipeline for text generation.
    Ensures Hugging Face login is handled during model loading.
    """
    # Prompt for Hugging Face token if not already set
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    if hf_token is None:
        print("Hugging Face token not found.")
        hf_token = getpass("Enter your Hugging Face API token: ")
        os.environ["HF_TOKEN"] = hf_token  # Temporarily set the token

    # Login to Hugging Face
    try:
        login(token=hf_token)
        print("Login successful.")
    except Exception as e:
        raise ValueError(f"Failed to authenticate with Hugging Face: {e}")

    # Load the pipeline
    try:
        print("Loading the model pipeline...")
        pipe = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            torch_dtype=torch.bfloat16,
        )
        print("Model loaded successfully.")
        return pipe
    except Exception as e:
        raise RuntimeError(f"Failed to load the model pipeline: {e}")


def generate_text(pipe: Pipeline, prompt: str, temperature: float = 0.7) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    predictions = pipe(
        prompt,
        temperature=temperature,
        max_new_tokens=256,
        do_sample=True,
        top_k=50,
        top_p=0.95,
    )
    output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]
    return output

def load_audio_model() -> tuple[AutoProcessor, AutoModel]:
    processor = AutoProcessor.from_pretrained("suno/bark-small")
    model = AutoModel.from_pretrained("suno/bark-small")
    return processor, model


def generate_audio(
    processor: AutoProcessor,
    model: AutoModel,
    prompt: str,
    preset: VoicePresets,
) -> tuple[np.array, int]:
    inputs = processor(text=[prompt], return_tensors="pt", voice_preset=preset)
    output = model.generate(**inputs, do_sample=True).cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate
    return output, sample_rate

def load_image_model() -> StableDiffusionInpaintPipelineLegacy:
    pipe = DiffusionPipeline.from_pretrained(
        "segmind/tiny-sd", torch_dtype=torch.float32
    )
    return pipe

def generate_image(
    pipe: StableDiffusionInpaintPipelineLegacy, prompt: str
) -> Image.Image:
    output = pipe(prompt, num_inference_steps=10).images[0]
    return output


