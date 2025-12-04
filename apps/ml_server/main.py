from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import base64
import io
import torch
import clip
from PIL import Image
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["GET", "POST"],
    allow_headers= ["*"],
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

class ClipRequest(BaseModel):
    prompt: str
    image: str

@app.get("/")
async def root():
    return {"message": "Hello From ML_Server"}

@app.post("/score-image")
def confidence_rating(data:ClipRequest):
    img_bytes = base64.b64decode(data.image)
    pil_image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    image_tensor = preprocess(pil_image).unsqueeze(0).to(device)
    prompts = [
        data.prompt,
        "A doodle sketch of " + data.prompt,
        "A sketch of " + data.prompt
    ]
    text_tokens = clip.tokenize(prompts).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        text_features = model.encode_text(text_tokens)

    similarity = torch.cosine_similarity(image_features, text_features)[0].item()
    print(similarity)
    confidence = max(0, similarity)

    return {
        "prompt": data.prompt,
        "confidence": confidence,
        "confidence_percent": round(confidence * 100, 2)
    }

