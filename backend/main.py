from fastapi import FastAPI, UploadFile, File, Form
import base64
from PIL import Image
import io
from .model_loader import OrthoVisionModel
from .llm_service import ClinicalValidationService

app = FastAPI(title="OrthoAssist Core Backend")

# Initialize our services
vision_service = OrthoVisionModel()
llm_service = ClinicalValidationService()

@app.post("/api/v1/validate-case")
async def validate_case(
    file: UploadFile = File(...),
    prescription: str = Form(...),
    patient_history: str = Form(...)
):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Optional: Run local vision model for feature logging/analytics
    _ = vision_service.extract_features(image)
    
    # Convert image to base64 string for direct LLM multimodal processing
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # Generate unified report
    report_markdown = llm_service.generate_medical_report(encoded_image, prescription, patient_history)
    
    return {"status": "success", "report": report_markdown}