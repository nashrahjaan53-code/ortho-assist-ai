import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ClinicalValidationService:
    def __init__(self):
          # Read the correctly named key from your .env file
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        
        # Swapping out the retired 1.5 model for the active 2.5 Flash model
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_medical_report(self, base64_image: str, prescription: str, history: str) -> str:
        system_prompt = (
            "You are an expert orthopedic radiologist and clinical pharmacologist AI assistant. "
            "Your task is to analyze the provided orthopedic X-ray, cross-reference it with the patient's "
            "clinical history, and perform a strict safety validation on the prescribed medication.\n\n"
            "Structure your response perfectly in markdown with the following sections:\n"
            "1.  X-Ray Visual Findings\n"
            "2.  Prescription Safety Evaluation (Check for drug-condition contraindications or wrong dosages)\n"
            "3.  Warnings / Red Flags (If any)\n"
            "4.  Clinical Recommendations"
        )

        # Structure the payload data for the Gemini SDK
        prompt = f"{system_prompt}\n\nPatient History: {history}\nPrescribed Medication: {prescription}"
        
        # Prepare the image structure directly from base64 string
        image_data = {
            'mime_type': 'image/jpeg',
            'data': base64_image
        }

        # Request generation
        response = self.model.generate_content([prompt, image_data])
        return response.text