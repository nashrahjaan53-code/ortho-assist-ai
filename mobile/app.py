import flet as ft
import requests
from PIL import Image
import io

BACKEND_URL = "http://127.0.0.1:8000/api/v1/validate-case"

def main(page: ft.Page):
    page.title = "OrthoAssist Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    def show_main_dashboard(e):
        page.clean()
        
        history_input = ft.TextField(
            label="Patient History & Symptoms", 
            multiline=True, 
            min_lines=3,
            hint_text="e.g., 45yo male, suspected wrist fracture..."
        )
        prescription_input = ft.TextField(
            label="Prescribed Medication", 
            hint_text="e.g., Oxycodone 20mg"
        )
        status_text = ft.Markdown(selectable=True)

        def submit_case(e):
            if not history_input.value or not prescription_input.value:
                status_text.value = "Error: Please complete all input parameters."
                page.update()
                return

            status_text.value = "Analyzing data and validating safety parameters..."
            page.update()

            try:
                # Create a valid 224x224 blank image in memory so PyTorch doesn't crash
                img = Image.new('RGB', (224, 224), color='black')
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_bytes = img_byte_arr.getvalue()

                # Pack the valid image bytes into the payload
                files = {"file": ("mock_xray.jpg", img_bytes, "image/jpeg")}
                data = {
                    "prescription": prescription_input.value,
                    "patient_history": history_input.value
                }
                
                # Send request to FastAPI
                response = requests.post(BACKEND_URL, files=files, data=data, timeout=60)
                if response.status_code == 200:
                    status_text.value = response.json()["report"]
                else:
                    status_text.value = f"API Server Error: {response.status_code}\n\n{response.text}"
            except Exception as err:
                status_text.value = f"Connection failed to backend: {str(err)}"
            
            page.update()

        page.add(
            ft.Text("OrthoAssist Diagnostic Hub", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            history_input,
            prescription_input,
            ft.Button("Run AI Safety Check", on_click=submit_case),
            ft.Divider(),
            ft.Text("Clinical AI Analysis Output:", size=16, weight=ft.FontWeight.W_600),
            status_text
        )
        page.update()

    app_title = ft.Text(
        value="OrthoAssist AI", 
        size=32, 
        weight=ft.FontWeight.BOLD, 
        text_align=ft.TextAlign.CENTER
    )
    
    app_subtitle = ft.Text(
        value="Clinical Decision Support System", 
        size=16, 
        color=ft.Colors.BLUE_400,
        text_align=ft.TextAlign.CENTER
    )

    explanation_card = ft.Container(
        content=ft.Column([
            ft.Text(
                "What this application does:", 
                size=18, 
                weight=ft.FontWeight.W_600
            ),
            ft.Text(
                "1. Scans orthopedic radiographs using a local vision extraction layer.\n"
                "2. Cross-references visual indicators with text-based patient charts.\n"
                "3. Automatically runs cross-checks against target drug descriptions to catch toxic interactions, dosage anomalies, or clinical contraindications before finalized processing.",
                size=14,
                color=ft.Colors.GREY_300
            )
        ], spacing=10),
        padding=20,
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        width=400
    )

    disclaimer_text = ft.Text(
        value="For educational demonstration and portfolio validation purposes only. Not certified for clinical deployment.",
        size=11,
        color=ft.Colors.RED_300,
        text_align=ft.TextAlign.CENTER,
        width=360
    )

    start_button = ft.Button(
        "Open Dashboard", 
        on_click=show_main_dashboard,
        width=200
    )

    page.add(
        ft.Column(
            controls=[
                app_title,
                app_subtitle,
                ft.Container(height=20),
                explanation_card,
                ft.Container(height=30),
                start_button,
                ft.Container(height=20),
                disclaimer_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

if __name__ == "__main__":
    ft.run(main)