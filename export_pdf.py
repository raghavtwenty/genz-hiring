from reportlab.pdfgen import canvas


def create_resume_pdf(magic, output_file):
    # Create a PDF document
    pdf_canvas = canvas.Canvas(output_file)

    # Set font and size
    pdf_canvas.setFont("Helvetica", 10)

    # Add text content to the PDF
    text_lines = magic.split("\n")
    for line in text_lines:
        if len(line) > 120:
            newi = line.split(".")
            for newlitem in newi:
                pdf_canvas.drawString(
                    20, 800, newlitem
                )  # You may need to adjust the coordinates
                # Move to the next line
                pdf_canvas.translate(0, -15)
        else:
            pdf_canvas.drawString(20, 800, line)

        # Move to the next line
        pdf_canvas.translate(0, -15)

    # Save the PDF file
    pdf_canvas.save()
