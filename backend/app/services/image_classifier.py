from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

MODEL_NAME = "your-crop-disease-model"

processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)


def predict_disease(image_path: str):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    probs = outputs.logits.softmax(dim=1)

    confidence, idx = probs.max(dim=1)

    label = model.config.id2label[idx.item()]

    crop, disease = label.split("___")

    return {
        "crop": crop,
        "disease": disease,
        "confidence": float(confidence.item()),
    }