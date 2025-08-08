from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from fpdf import FPDF
from datetime import datetime

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def form():
    with open("templates/form.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/submit-payment/")
def submit_payment(
    date_paid: str = Form(...),
    tenant_name: str = Form(...),
    tenant_address: str = Form(...),
    amount_paid: float = Form(...),
    landlord_name: str = Form(...),
    tenant_signature: str = Form(""),         
    landlord_signature: str = Form(""),
    landlord_signature_date: str = Form("")
):
    # Format dates
    try:
        date_paid_fmt = datetime.strptime(date_paid, "%Y-%m-%d").strftime("%B %d, %Y")
    except ValueError:
        date_paid_fmt = date_paid

    if landlord_signature_date:
        try:
            landlord_signature_date_fmt = datetime.strptime(
                landlord_signature_date, "%Y-%m-%d"
            ).strftime("%B %d, %Y")
        except ValueError:
            landlord_signature_date_fmt = landlord_signature_date
    else:
        landlord_signature_date_fmt = ""

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "RENT PAYMENT RECEIPT", ln=True, align="C")

    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 8, "Thank you for your payment!", ln=True, align="C")

    pdf.ln(10)  # Add vertical space

    pdf.set_draw_color(34, 197, 94)  # Green color for lines
    pdf.set_line_width(1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Date Paid: {date_paid_fmt}", ln=True)

    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Tenant Information", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 7, f"Name: {tenant_name}", ln=True)
    pdf.multi_cell(0, 7, f"Address: {tenant_address}")

    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Payment Details", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 7, f"Amount Paid: ${amount_paid:,.2f}", ln=True)
    pdf.cell(0, 7, f"Landlord: {landlord_name}", ln=True)

    pdf.ln(12)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Signatures", ln=True)
    pdf.ln(6)

    pdf.set_font("Helvetica", "", 12)
    # Tenant Signature line
    pdf.cell(50, 7, "Tenant Signature:", ln=False)
    if tenant_signature:
        pdf.cell(0, 7, tenant_signature, ln=True)
    else:
        pdf.cell(0, 7, "____________________________", ln=True)

    pdf.ln(8)

    # Landlord Signature line
    pdf.cell(50, 7, "Landlord Signature:", ln=False)
    if landlord_signature:
        pdf.cell(0, 7, landlord_signature, ln=True)
    else:
        pdf.cell(0, 7, "____________________________", ln=True)

    pdf.ln(8)

    # Signature Date line
    pdf.cell(50, 7, "Signature Date:", ln=False)
    if landlord_signature_date_fmt:
        pdf.cell(0, 7, landlord_signature_date_fmt, ln=True)
    else:
        pdf.cell(0, 7, "____________________________", ln=True)

    output_path = "rent_receipt.pdf"
    pdf.output(output_path)

    return FileResponse(output_path, media_type="application/pdf", filename="rent_receipt.pdf")
