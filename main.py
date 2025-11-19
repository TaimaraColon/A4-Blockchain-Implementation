from flask import Flask, render_template, request, redirect, url_for, send_file
# Assuming Blockchain class is now in A4.py (or you moved it into this file)
from A4 import Blockchain 
import re 
import json

app = Flask(__name__)

# Initialize the Blockchain instance
blockchain = Blockchain("Loans", [("borrower", "str"), ("lender", "str"), ("amount", "float")]) 
# Note: The initialization in A3.py's Blockchain class will print:
# " Initialized Blockchain 'Loans' and created Block."

# Fix: Adjusted regex to allow letters, spaces, or hyphens for names
def nameValidation(name):
    """Verify if the name contains only letters, spaces, or hyphens."""
    # Regex: Starts (^) and ends ($) with one or more (+) of the allowed characters.
    return bool(re.fullmatch(r"[A-Za-z\s-]+", name))


@app.route('/', methods=['POST','GET'])
def index():
    message = ""
    if request.method == 'POST':
        # All actions (add, mine, export) are now submitted via hidden 'action' field
        action = request.form.get('action') 

        if action == "add":
            borrower = request.form.get('borrower')
            lender = request.form.get('lender')
            amount = request.form.get('amount')
            
            # 1. Basic empty check
            if not borrower or not lender or not amount:
                message = "All fields must be filled."

            # 2. Name validation check
            elif not nameValidation(borrower) or not nameValidation(lender):
                message = "Names for Borrower and Lender must be only letters, spaces, hyphens, or apostrophes."

            # 3. Process valid data
            else:
                
                # Attempt to convert amount to float
                amountVal = float(amount) 
                
                # Create the transaction dictionary expected by blockchain.add()
                transaction = {
                    "borrower": borrower,
                    "lender": lender,
                    "amount": amountVal 
                }
                
                # Add data to the blockchain's list of unmined data
                blockchain.add(transaction)
                message = "Transaction was successful (Mine pending)."
        
        elif action == "mine":
            # Check if there is data to mine (list length > 0)
            if not blockchain.current_data: 
                message = "No transactions to mine."

            else:
                new_block = blockchain.mine()
                message = f"Block #{new_block['index']} was successfully mined and added to the chain."

        elif action == "export":
            # The export operation will save the file and return it
            filename = f"{blockchain.name}_blockchain.json"
            
            # Use the export method from A4 (which dumps the chain to a file)
            blockchain.export(filename) 
            
            # Use send_file to make the file downloadable
            return send_file(filename, as_attachment=True)
            
    # Always refresh and render the template after an action
    chain = blockchain.chain
    # Access the instance variable directly for pending data
    pending = blockchain.current_data 
    
    return render_template('index.html', chain=chain, pending=pending, message=message)


if __name__ == "__main__":
    # The assignment suggests a specific IP and Port for running: app.run(host='10.24.8.52', port=5000) [cite: 1]
    # Use 127.0.0.1 (localhost) and default port for development simplicity
    app.run(host='127.0.0.1', debug=True)