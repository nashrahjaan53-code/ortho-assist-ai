import torch
from transformers import ViTImageProcessor, ViTModel
from PIL import Image

class OrthoVisionModel:
    def __init__(self):
        # Universally supported, highly stable standard Vision Transformer from Google
        self.model_id = "google/vit-base-patch16-224"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Loading stable vision model: {self.model_id} on {self.device}...")
        
        # Load the standard processor and model seamlessly
        self.processor = ViTImageProcessor.from_pretrained(self.model_id)
        self.model = ViTModel.from_pretrained(self.model_id).to(self.device)
        self.model.eval()
        
        print(" Core Vision feature extractor online!")

    def extract_features(self, image: Image.Image):
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Extract the pooler output (a clean vector representing the image patterns)
            image_features = outputs.pooler_output
        return image_features.cpu().numpy().tolist()