from reportlab.lib.pagesizes import A7
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# Define the invoice data
invoice_number = "INV-001"
customer_name = "John Smith"
invoice_date = "2023-03-28"
items = [
    {"item_name": "Product A", "quantity": 2, "price": 10},
    {"item_name": "Product B", "quantity": 1, "price": 5},
]

# Calculate the total amount
total_amount = sum([item["quantity"] * item["price"] for item in items])

# Create the PDF file
pdf_file_name = "invoice.pdf"
pdf = canvas.Canvas(pdf_file_name, pagesize=A7)

# Set the margins
left_margin = 5 * mm
bottom_margin = 5 * mm
pdf.translate(left_margin, bottom_margin)

# Set the starting position of the text
x, y = 0, 60

# Define the content
pdf.setFont("Helvetica", 8)
pdf.drawString(x, y, f"Invoice Number: {invoice_number}")
pdf.drawString(x, y-10, f"Customer Name: {customer_name}")
pdf.drawString(x, y-20, f"Invoice Date: {invoice_date}")

y -= 40

pdf.setFont("Helvetica-Bold", 8)
pdf.drawString(x, y, "Items:")
pdf.setFont("Helvetica", 8)

y -= 10

for item in items:
    pdf.drawString(x, y, f"{item['item_name']} - {item['quantity']} x ${item['price']} = ${item['quantity']*item['price']}")
    y -= 10

y -= 10

pdf.setFont("Helvetica-Bold", 8)
pdf.drawString(x, y, f"Total Amount: ${total_amount}")

# Save the PDF file
pdf.save()

print(f"PDF file '{pdf_file_name}' has been created successfully.")
