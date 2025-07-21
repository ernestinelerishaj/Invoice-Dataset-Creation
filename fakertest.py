import random
from faker import Faker
import json

fake = Faker()

# Function to generate a random GSTIN
def random_gstin():
    state_code = random.randint(1, 37)  # GSTIN state codes range from 01 to 37
    pan = fake.bothify(text="?????#####")  # Random alphanumeric format for PAN
    check_digit = random.randint(0, 9)
    return f"{state_code:02}{pan}{check_digit}Z{random.randint(1, 9)}"

# Function to generate a random date in various formats
def random_date():
    date = fake.date_between(start_date='-5y', end_date='today')
    formats = ['%d-%m-%Y', '%d.%m.%Y', '%d / %B / %Y', '%d / %m / %Y']
    return date.strftime(random.choice(formats))

# Function to generate a consistent invoice entry
def generate_invoice():
    invoice_number = f"INV{random.randint(1000, 9999)}-{random.choice(['A', 'B', 'C', 'D'])}"
    invoice_date = random_date()
    buyer_gstin = random_gstin()
    supplier_gstin = random_gstin()
    
    items = [
        {"description": fake.catch_phrase(), "price": round(random.uniform(100, 1000), 2), "quantity": random.randint(1, 5)}
        for _ in range(random.randint(1, 3))
    ]
    
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = round(subtotal * random.uniform(0.01, 0.18), 2)  # Random tax between 1% and 18%
    total = round(subtotal + tax, 2)

    # Create item description text
    item_text = "\n".join([f"{idx + 1} {item['description']} ${item['price']} {item['quantity']} ${round(item['price'] * item['quantity'], 2)}" for idx, item in enumerate(items)])

    # Generate a random format for the invoice text
    text_formats = [
        f"Brand {fake.company()} INVOICE\nInvoice to: {fake.company()}, {fake.address()} GSTIN: {buyer_gstin} State: Maharashtra\nInvoice# {invoice_number}\nDate: {invoice_date}\nSL. Item Description Price Qty. Total\n{item_text}\nSubtotal ${subtotal}\nTax (CGST + SGST) ${tax}\nTotal ${total}\nSupplier GSTIN: {supplier_gstin}\nPayment: XYZ Bank IFSC: ABCD12345",
        
        f"Hansen, Reed and Clark INVOICE\nInvoice Number: {invoice_number}\nDate: {invoice_date}\nBill To: {fake.company()}, GSTIN: {buyer_gstin}\nItems:\n{item_text}\nSubtotal: ${subtotal}\nTax: ${tax}\nTotal: ${total}\nSupplier GSTIN: {supplier_gstin}",
        
        f"Tech Innovations INVOICE\nInvoice# {invoice_number}\nDate: {invoice_date}\nTo: {fake.company()} GSTIN: {buyer_gstin}\nSL. Item Description Price Qty. Total\n{item_text}\nSubtotal ${subtotal}\nTotal ${total}\nSupplier GSTIN: {supplier_gstin}\nPayment Terms: Net {random.choice([15, 30])} days",
        
        f"Supplier: {fake.company()} INVOICE\nInvoice# {invoice_number}\nDate: {invoice_date}\nBilled To: {fake.company()} GSTIN: {buyer_gstin}\nSL. Item Description Price Qty. Total\n{item_text}\nTotal: ${total}\nSupplier GSTIN: {supplier_gstin}",
        
        f"Invoice from {fake.company()}\nInvoice# {invoice_number}\nDate: {invoice_date}\nFor: {fake.company()}, GSTIN: {buyer_gstin}\nItems:\n{item_text}\nSubtotal: ${subtotal}\nTotal: ${total}\nSupplier GSTIN: {supplier_gstin}",
        
        f"{fake.company()} Billing Invoice\nInvoice# {invoice_number}\nInvoice Date: {invoice_date}\nCustomer: {fake.company()} GSTIN: {buyer_gstin}\nDetails of Services:\n{item_text}\nSubtotal: ${subtotal}\nTotal Amount: ${total}\nSupplier GSTIN: {supplier_gstin}",
        
        f"Invoice Summary\nNumber: {invoice_number}\nDate: {invoice_date}\nBilled To: {fake.company()} GSTIN: {buyer_gstin}\nItems:\n{item_text}\nSubtotal: ${subtotal}\nTotal Amount: ${total}\nSupplier GSTIN: {supplier_gstin}",
        
        f"{fake.company()} Invoice\nInvoice# {invoice_number}\nInvoice Date: {invoice_date}\nTo: {fake.company()}, GSTIN: {buyer_gstin}\nSL. Item Description Price Qty. Total\n{item_text}\nTotal Amount: ${total}\nSupplier GSTIN: {supplier_gstin}",
        
        f"{fake.company()} INVOICE\nInvoice Number: {invoice_number}\nInvoice Date: {invoice_date}\nTo: {fake.company()} GSTIN: {buyer_gstin}\nSL. Item Description Price Qty. Total\n{item_text}\nTotal Amount: ${total}\nSupplier GSTIN: {supplier_gstin}",
        
        f"{fake.company()} INVOICE\nInvoice Number: {invoice_number}\nInvoice Date: {invoice_date}\nTo: {fake.company()} GSTIN: {buyer_gstin}\nSL. Item Description Price Qty. Total\n{item_text}\nTotal Amount: ${total}\nSupplier GSTIN: {supplier_gstin}"
    ]
    
    # Randomly select a format for the invoice text
    text = random.choice(text_formats)
    
    return {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "invoice_amount": str(total),
        "buyer_gstin": buyer_gstin,
        "supplier_gstin": supplier_gstin,
        "text": text
    }

# Generate 100 invoices with varied date formats and consistent invoice number pattern
invoices = [generate_invoice() for _ in range(500)]

# Print or save the invoices as needed
with open('formatted_invoices.json', 'w') as f:
    json.dump(invoices, f, indent=4)

# Optionally, print the generated invoices to console
for invoice in invoices:
    print(json.dumps(invoice, indent=4))
