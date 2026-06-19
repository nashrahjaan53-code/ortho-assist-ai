import flet as ft
import requests
from PIL import Image
import io

BACKEND_URL = "http://127.0.0.1:8000/api/v1/validate-case"

async def main(page: ft.Page):
    page.title = "OrthoAssist Mobile Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30
    page.bgcolor = "#0A0E1A"  # Slate space black

    # Custom theme configurations
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#3B82F6",
            on_primary=ft.Colors.WHITE,
            surface="#131926",
            on_surface=ft.Colors.WHITE,
        )
    )

    uploaded_image_bytes = None

    # Instantiate FilePicker service (Flet 0.85+ registers it automatically)
    file_picker = ft.FilePicker()

    async def show_welcome_screen(e=None):
        page.clean()

        logo_icon = ft.Icon(
            ft.Icons.MEDICAL_SERVICES_ROUNDED,
            size=64,
            color="#3B82F6"
        )
        
        app_title = ft.Text(
            value="OrthoAssist AI",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )
        
        app_subtitle = ft.Text(
            value="Intelligent Musculoskeletal Vision & Safety Validation",
            size=14,
            color="#06B6D4",
            text_align=ft.TextAlign.CENTER
        )

        capabilities_card = ft.Container(
            content=ft.Column([
                ft.Text("System Capabilities", size=18, weight=ft.FontWeight.BOLD, color="#94A3B8"),
                ft.Divider(color="#1E293B"),
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color="#06B6D4", size=18),
                    ft.Text("Computer Vision Radiograph Analysis", size=13, color=ft.Colors.WHITE)
                ]),
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color="#06B6D4", size=18),
                    ft.Text("Multimodal Clinical Patient Context Integration", size=13, color=ft.Colors.WHITE)
                ]),
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color="#06B6D4", size=18),
                    ft.Text("Automated Prescription Safety Verification", size=13, color=ft.Colors.WHITE)
                ]),
            ], spacing=12),
            padding=25,
            border_radius=16,
            bgcolor="#131926",
            border=ft.Border.all(1, "#1E293B"),
            width=500
        )

        disclaimer_box = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.WARNING_ROUNDED, color="#EF4444", size=20),
                ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT),
                ft.Text(
                    value="Notice: This system serves as an educational framework demonstration and is not validated for live clinical deployment configurations.",
                    size=11,
                    color="#EF4444",
                    expand=True
                )
            ]),
            width=500,
            bgcolor="#2A161A",
            border=ft.Border.all(1, "#991B1B"),
            border_radius=10,
            padding=15
        )

        start_button = ft.Button(
            content=ft.Row([
                ft.Icon(ft.Icons.DASHBOARD_ROUNDED, size=20),
                ft.Text("Access Diagnostics Dashboard", size=15, weight=ft.FontWeight.W_600)
            ], alignment=ft.MainAxisAlignment.CENTER),
            on_click=show_main_dashboard,
            width=280,
            height=48,
            bgcolor="#3B82F6",
            color=ft.Colors.WHITE
        )

        page.add(
            ft.Column(
                controls=[
                    ft.Container(height=40),
                    logo_icon,
                    app_title,
                    app_subtitle,
                    ft.Container(height=20),
                    capabilities_card,
                    ft.Container(height=15),
                    disclaimer_box,
                    ft.Container(height=25),
                    start_button,
                    ft.Container(height=40)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            )
        )
        page.update()

    async def show_main_dashboard(e=None):
        page.clean()

        # Input fields
        history_input = ft.TextField(
            label="Patient History & Symptoms",
            multiline=True,
            min_lines=3,
            max_lines=5,
            hint_text="e.g., 45yo male, fell from ladder, acute pain/swelling in left wrist...",
            border_color="#1E293B",
            focused_border_color="#3B82F6",
            bgcolor="#0A0E1A",
            color=ft.Colors.WHITE,
            hint_style=ft.TextStyle(color="#64748B"),
            label_style=ft.TextStyle(color="#94A3B8"),
        )
        
        prescription_input = ft.TextField(
            label="Prescribed Medication (Optional)", 
            hint_text="e.g., Oxycodone 5mg orally every 6 hours as needed (Leave blank if none)",
            border_color="#1E293B",
            focused_border_color="#3B82F6",
            bgcolor="#0A0E1A",
            color=ft.Colors.WHITE,
            hint_style=ft.TextStyle(color="#64748B"),
            label_style=ft.TextStyle(color="#94A3B8"),
        )
        
        upload_status = ft.Text("No file selected", color="#64748B", size=13)
        preview_img = ft.Image(src="", visible=False, width=320, height=200, fit=ft.BoxFit.CONTAIN, border_radius=10)
        
        async def on_pick_file(e):
            nonlocal uploaded_image_bytes
            files = await file_picker.pick_files(
                allow_multiple=False,
                file_type=ft.FilePickerFileType.IMAGE,
                dialog_title="Select Patient X-Ray Image"
            )
            if files:
                file_path = files[0].path
                with open(file_path, "rb") as f:
                    uploaded_image_bytes = f.read()
                upload_status.value = f"Selected: {files[0].name}"
                upload_status.color = "#3B82F6"
                preview_img.src = uploaded_image_bytes
                preview_img.visible = True
            else:
                upload_status.value = "No file selected."
                upload_status.color = "#64748B"
                preview_img.visible = False
            page.update()

        status_text = ft.Markdown(selectable=True)
        report_card = ft.Container(
            content=ft.Column([
                ft.Text("AI Case Analysis Output", size=16, weight=ft.FontWeight.BOLD, color="#3B82F6"),
                ft.Divider(color="#1E293B"),
                status_text
            ]),
            padding=25, 
            bgcolor="#131926", 
            border_radius=16,
            border=ft.Border.all(1, "#3B82F6"),
            width=650,
            visible=False
        )

        progress_ring = ft.ProgressRing(visible=False, color="#06B6D4", width=36, height=36)
        progress_text = ft.Text("", visible=False, color="#94A3B8", size=13)
        
        async def submit_case(e):
            nonlocal uploaded_image_bytes
            
            if not history_input.value or not history_input.value.strip():
                history_input.border_color = ft.Colors.RED_700
                page.update()
                return
            
            history_input.border_color = "#1E293B"
            
            # Show loading states
            progress_ring.visible = True
            progress_text.value = "Sending case details and running safety parameters..."
            progress_text.visible = True
            report_card.visible = False
            page.update()
            
            try:
                if uploaded_image_bytes is None:
                    img = Image.new('RGB', (224, 224), color='black')
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    final_bytes = img_byte_arr.getvalue()
                else:
                    final_bytes = uploaded_image_bytes
                
                medication = prescription_input.value.strip() if (prescription_input.value and prescription_input.value.strip()) else "None prescribed yet."
                files = {"file": ("xray.jpg", final_bytes, "image/jpeg")}
                data = {
                    "prescription": medication,
                    "patient_history": history_input.value
                }
                
                # Executing post request to the API backend
                response = requests.post(BACKEND_URL, files=files, data=data, timeout=60)
                if response.status_code == 200:
                    status_text.value = response.json()["report"]
                    report_card.visible = True
                else:
                    status_text.value = f"### API Server Error: {response.status_code}\n\n{response.text}"
                    report_card.visible = True
            except Exception as err:
                status_text.value = f"### Connection to Backend Failed\n\nUnable to reach backend diagnostic server at `{BACKEND_URL}`. Details:\n\n*Error: {str(err)}*"
                report_card.visible = True
            
            # Hide loading states
            progress_ring.visible = False
            progress_text.visible = False
            page.update()

        # Layout construction
        header_row = ft.Row(
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.LOCAL_HOSPITAL_ROUNDED, color="#3B82F6", size=24),
                    ft.Text("OrthoAssist Diagnostic Hub", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ]),
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_ROUNDED, 
                    on_click=show_welcome_screen,
                    tooltip="Return to Landing Page",
                    icon_color="#94A3B8"
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        radiograph_card = ft.Container(
            content=ft.Column([
                ft.Text("1. Radiograph Attachment", size=15, weight=ft.FontWeight.W_600, color="#94A3B8"),
                ft.Divider(color="#1E293B"),
                ft.Row([
                    ft.Button(
                        content=ft.Row([
                            ft.Icon(ft.Icons.FILE_UPLOAD_ROUNDED, size=16),
                            ft.Text("Select X-Ray Image")
                        ]),
                        on_click=on_pick_file
                    ),
                    upload_status
                ], alignment=ft.MainAxisAlignment.START, spacing=15),
                preview_img
            ], spacing=15),
            padding=20, 
            bgcolor="#131926", 
            border_radius=16, 
            border=ft.Border.all(1, "#1E293B"),
            width=650
        )

        clinical_card = ft.Container(
            content=ft.Column([
                ft.Text("2. Clinical Parameters", size=15, weight=ft.FontWeight.W_600, color="#94A3B8"),
                ft.Divider(color="#1E293B"),
                history_input,
                prescription_input,
            ], spacing=15),
            padding=20, 
            bgcolor="#131926", 
            border_radius=16, 
            border=ft.Border.all(1, "#1E293B"),
            width=650
        )

        page.add(
            ft.Column(
                controls=[
                    header_row,
                    ft.Container(height=10),
                    radiograph_card,
                    ft.Container(height=10),
                    clinical_card,
                    ft.Container(height=15),
                    ft.Button(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, size=18),
                            ft.Text("Execute AI Case Analysis", size=15, weight=ft.FontWeight.W_600)
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        on_click=submit_case,
                        width=300,
                        height=48,
                        bgcolor="#06B6D4",
                        color=ft.Colors.WHITE
                    ),
                    ft.Container(height=15),
                    ft.Column([
                        progress_ring,
                        progress_text
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    report_card,
                    ft.Container(height=30)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            )
        )
        page.update()

    # Load initial welcome screen
    await show_welcome_screen()

if __name__ == "__main__":
    ft.run(main)