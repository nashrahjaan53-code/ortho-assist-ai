import flet as ft
import requests
from PIL import Image
import io

BACKEND_URL = "http://127.0.0.1:8000/api/v1/validate-case"

def main(page: ft.Page):
    page.title = "OrthoAssist Mobile Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30
    

    uploaded_image_bytes = None

# Change ft.FilePickerResultEvent to ft.ControlEvent
    def on_file_result(e: ft.ControlEvent):
        nonlocal uploaded_image_bytes
        if e.files:
            file_path = e.files[0].path
            with open(file_path, "rb") as f:
                uploaded_image_bytes = f.read()
            upload_status.value = f"Selected: {e.files[0].name}"
            upload_status.color = ft.Colors.BLUE_400
        else:
            upload_status.value = "No file selected."
            upload_status.color = ft.Colors.GREY_500
        page.update()

    file_picker = ft.FilePicker(on_change=on_file_result)
    page.overlay.append(file_picker)


    upload_status = ft.Text("No file selected", color=ft.Colors.GREY_500, size=13)

    def show_main_dashboard(e):
        page.clean()
        
        history_input = ft.TextField(
            label="Patient History & Symptoms", 
            multiline=True, 
            min_lines=3,
            hint_text="e.g., 45yo male, suspected wrist fracture...",
            border_color=ft.Colors.BLUE_900,
            focused_border_color=ft.Colors.BLUE_400
        )
        
        prescription_input = ft.TextField(
            label="Prescribed Medication (Optional)", 
            hint_text="e.g., Oxycodone 20mg (Leave blank if none)",
            border_color=ft.Colors.BLUE_900,
            focused_border_color=ft.Colors.BLUE_400
        )
        
        status_text = ft.Markdown(selectable=True)

        def submit_case(e):
            nonlocal uploaded_image_bytes
            
            if not history_input.value.strip():
                status_text.value = "Please complete the patient history parameter."
                page.update()
                return

            status_text.value = "Running data synthesis and validating safety parameters..."
            page.update()

            try:
                # Fallback to blank image if user didn't upload a file
                if uploaded_image_bytes is None:
                    img = Image.new('RGB', (224, 224), color='black')
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    final_bytes = img_byte_arr.getvalue()
                else:
                    final_bytes = uploaded_image_bytes

                # Treat empty string as a clear declaration that no medication was assigned
                medication = prescription_input.value.strip() if prescription_input.value else "None prescribed yet."

                files = {"file": ("xray.jpg", final_bytes, "image/jpeg")}
                data = {
                    "prescription": medication,
                    "patient_history": history_input.value
                }
                
                response = requests.post(BACKEND_URL, files=files, data=data, timeout=60)
                if response.status_code == 200:
                    status_text.value = response.json()["report"]
                else:
                    status_text.value = f"API Server Error: {response.status_code}\n\n{response.text}"
            except Exception as err:
                status_text.value = f"Connection failed to backend: {str(err)}"
            
            page.update()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("OrthoAssist Diagnostic Hub", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Advanced Decision Support Engine", size=13, color=ft.Colors.BLUE_400),
                    ft.Divider(color=ft.Colors.BLUE_900),
                ]),
                margin=ft.margin.only(bottom=15)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("1. Radiograph Attachment", size=15, weight=ft.FontWeight.W_600),
                    ft.Row([
                        ft.Button("Select X-Ray Image", on_click=lambda _: file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)),
                        upload_status
                    ], alignment=ft.MainAxisAlignment.START)
                ]),
                padding=20, bgcolor=ft.Colors.SURFACE_CONTAINER_LOW, border_radius=12, border=ft.border.all(1, ft.Colors.BLUE_900)
            ),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column([
                    ft.Text("2. Clinical Parameters", size=15, weight=ft.FontWeight.W_600),
                    history_input,
                    prescription_input,
                ], spacing=15),
                padding=20, bgcolor=ft.Colors.SURFACE_CONTAINER_LOW, border_radius=12, border=ft.border.all(1, ft.Colors.BLUE_900)
            ),
            ft.Container(height=15),
            ft.Button("Execute AI Case Analysis", on_click=submit_case, width=250, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
            ft.Container(height=15),
            ft.Container(
                content=ft.Column([
                    ft.Text("Analysis Output Report", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    ft.Divider(color=ft.Colors.GREY_800),
                    status_text
                ]),
                padding=25, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=12, width=600
            )
        )
        page.update()

 
    app_title = ft.Text(
        value="OrthoAssist AI", 
        size=36, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.WHITE
    )
    
    app_subtitle = ft.Text(
        value="Intelligent Musculoskeletal Decision Support", 
        size=14, 
        color=ft.Colors.BLUE_400
    )

    explanation_card = ft.Container(
        content=ft.Column([
            ft.Text("System Capabilities", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200),
            ft.Divider(color=ft.Colors.BLUE_900),
            ft.Text(
                "• Computer Vision Feature Parsing: Evaluates alignment patterns and dense skeletal structures via an inline processing layer.\n\n"
                "• Optional Pharmacological Validation: Analyzes custom medication workflows against active anatomical diagnostic traits.\n\n"
                "• Automated Diagnostic Reporting: Delivers clean, structured analysis summaries instantly utilizing advanced generative language reasoning.",
                size=13,
                color=ft.Colors.GREY_300,
                line_height=1.4
            )
        ], spacing=10),
        padding=25,
        border_radius=16,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border=ft.border.all(1, ft.Colors.BLUE_900),
        width=450
    )

    disclaimer_box = ft.Container(
        content=ft.Text(
            value="Notice: This system serves as an educational framework demonstration and is not validated for live clinical deployment configurations.",
            size=11,
            color=ft.Colors.RED_300,
            text_align=ft.TextAlign.CENTER
        ),
        width=400,
        padding=10
    )

    start_button = ft.Button(
        "Access Dashboard", 
        on_click=show_main_dashboard,
        width=220,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE
    )

    page.add(
        ft.Column(
            controls=[
                app_title,
                app_subtitle,
                ft.Container(height=15),
                explanation_card,
                ft.Container(height=25),
                start_button,
                ft.Container(height=15),
                disclaimer_box
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

if __name__ == "__main__":
    ft.run(main)