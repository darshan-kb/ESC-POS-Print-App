import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import barcode
from barcode import Code128
from barcode.writer import ImageWriter

# Define the invoice data
invoice_number = 'INV-001'
invoice_date = '2023-03-28'
customer_name = 'John Doe'
items = [
    {'description': 'Product A', 'quantity': 2, 'price': 10},
    {'description': 'Product B', 'quantity': 1, 'price': 15},
    {'description': 'Product C', 'quantity': 3, 'price': 5},
]

# Set up the PDF document
pdf_buffer = io.BytesIO()
pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
pdf.setTitle('Invoice #{}'.format(invoice_number))

# Define the font styles
pdf.setFont("Helvetica-Bold", 14)
pdf.setFillColorRGB(0, 0, 0.8)
heading = pdf.drawCentredString(150*mm, 270*mm, "Invoice")

pdf.setFont("Helvetica", 12)
pdf.setFillColorRGB(0, 0, 0)
pdf.drawString(30*mm, 250*mm, "Invoice Number:")
pdf.drawString(30*mm, 235*mm, "Invoice Date:")
pdf.drawString(30*mm, 220*mm, "Customer Name:")
pdf.line(30*mm, 215*mm, 180*mm, 215*mm)

pdf.drawString(110*mm, 250*mm, invoice_number)
pdf.drawString(110*mm, 235*mm, invoice_date)
pdf.drawString(110*mm, 220*mm, customer_name)

# Draw the table headers
pdf.drawString(30*mm, 200*mm, "Description")
pdf.drawString(95*mm, 200*mm, "Quantity")
pdf.drawString(125*mm, 200*mm, "Price")
pdf.line(30*mm, 195*mm, 180*mm, 195*mm)

# Draw the table rows
y = 185
for item in items:
    description = item['description']
    quantity = item['quantity']
    price = item['price']
    total = quantity * price
    pdf.drawString(30*mm, y*mm, description)
    pdf.drawRightString(115*mm, y*mm, str(quantity))
    pdf.drawRightString(150*mm, y*mm, "{:.2f}".format(price))
    pdf.drawRightString(180*mm, y*mm, "{:.2f}".format(total))
    y -= 5

# Draw the total amount
total_amount = sum(item['quantity'] * item['price'] for item in items)
pdf.line(30*mm, (y-5)*mm, 180*mm, (y-5)*mm)
pdf.drawString(95*mm, (y-10)*mm, "Total Amount:")
pdf.drawRightString(180*mm, (y-10)*mm, "{:.2f}".format(total_amount))

# Create the barcode and add it to the PDF
code = Code128(invoice_number, writer=ImageWriter())
barcode_buffer = io.BytesIO()
code.write(barcode_buffer)
barcode_image = barcode_buffer.getvalue()
pdf.drawImage(barcode_image, 30*mm, 270*mm, width=50*mm, height=15*mm)

# Save the PDF document
pdf.save()