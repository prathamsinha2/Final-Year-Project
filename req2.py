from flask import Flask, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Product class
class Product:
    def __init__(self, rfid_tag, name, price):
        self.rfid_tag = rfid_tag
        self.name = name
        self.price = price

# Example product list
products = [
    Product("390094635F91", "BISCUIT", 100.0),
    Product("39009462804F", "BREAD", 20.0),
    Product("3900946DB070", "DETERGENT", 200.0),
    Product("3900947865B0", "SOAP", 100.0),
    Product("3900945B7F89", "MILK", 25.0)
]

# Global counters
total_amount = 0.0
item_count = 0

def find_product(rfid):
    for product in products:
        if product.rfid_tag == rfid:
            return product
    return None

@app.route('/scan', methods=['POST'])
def scan():
    global total_amount, item_count
    rfid = request.form.get('rfid')
    if not rfid:
        logging.warning("No RFID provided")
        return "Error: No RFID provided", 400

    product = find_product(rfid)
    if product:
        total_amount += product.price
        item_count += 1
        logging.info(f"Product scanned: {product.name}, Price: {product.price}")
        return f"{product.name}\n{product.price:.2f}"
    else:
        logging.warning(f"Unknown RFID: {rfid}")
        return f"Unknown Tag\n{rfid}"


@app.route('/display', methods=['POST'])
def display():
    global total_amount, item_count
    logging.info(f"Total Items: {item_count}, Total Bill: {total_amount}")
    return f"{item_count}\n{total_amount:.2f}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Bind to the specific IP and port
