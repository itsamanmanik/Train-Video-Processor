from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
import glob

def generate_report(output_filename, train_number, total_coaches, processed_dir):
    """
    Generates a PDF report summarizing the train video analysis.
    """
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []

    summary_style = ParagraphStyle(
        'SummaryStyle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        alignment=1
    )
    
    story.append(Paragraph(f"Train Video Analysis Report", summary_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(f"**Train Number:** {train_number}", styles['Normal']))
    story.append(Paragraph(f"**Total Coaches Detected:** {total_coaches}", styles['Normal']))
    story.append(Paragraph("---", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("This report provides a detailed breakdown of the coaches identified in the input video, along with annotated frames showing detected components such as doors.", styles['Normal']))
    
    story.append(PageBreak())

    for i in range(1, total_coaches + 1):
        coach_folder = os.path.join(processed_dir, f"{train_number}_{i}")
        if os.path.exists(coach_folder):
            story.append(Paragraph(f"Coach {i}", styles['Heading2']))
            story.append(Spacer(1, 0.2 * inch))

            image_paths = sorted(glob.glob(os.path.join(coach_folder, f"{train_number}_{i}_*.jpg")))
            annotated_images = [path for path in image_paths if '_original' not in path]

            if annotated_images:
                for img_path in annotated_images:
                    img = Image(img_path, width=5.5*inch, height=4*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.1 * inch))
            else:
                story.append(Paragraph("No annotated images found for this coach.", styles['Normal']))
            
            story.append(PageBreak())

    doc.build(story)
    print(f"Report '{output_filename}' generated successfully.")