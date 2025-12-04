from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageClassification, AutoImageProcessor

model_name = "WinKawaks/SketchXAI-Base-QuickDraw345"
# Load model
model = AutoModelForImageClassification.from_pretrained(model_name)

# Your transform (SketchXAI expects 224×224 grayscale normalized)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),              # shape: [1, H, W]
    transforms.Normalize(mean=[0.5], std=[0.5])
])

# Load and preprocess image
image = Image.open("elephant.jpeg").convert("L")
image = image.convert("RGB")
tensor = transform(image).unsqueeze(0)  # shape [1, 1, 224, 224]

with torch.no_grad():
    outputs = model(tensor)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    confidence, pred_class = torch.max(probs, dim=1)

print("Prediction:", model.config.id2label[pred_class.item()])
print("Confidence:", confidence.item())
