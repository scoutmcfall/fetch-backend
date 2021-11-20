Greetings!
In order to run this program:
1. create a virtual environment: virtualenv env
2. activate the environment: source env/bin/activate
3. pip3 install -r requirements.txt
4. run the server: python3 server.py
5. the homepage url feeds in some test data
6. next, navigate to the transaction route (here's an example url you can use to add a transaction: "http://127.0.0.1:5000/transaction?payer=DANNON&points=300&timestamp=2020-10-31T10:00:00Z")
7. now, navigate to the spend route (here's an example that spends 300 points: http://127.0.0.1:5000/spend?points=300)
8. finally, navigate to the balances route to see all the payers' final balances: http://127.0.0.1:5000/balances
  

Each transaction is read in individually and the list of positive transactions is stored in session as ledger.
If it is positive, it's added to the end of ledger (a list of dictionaries).
If it's negative, it's added to negs (list of dictionaries) which the spend route iterates through, 
subtracting each from ledger and updating ledger each iteration.

So, session consists of: {ledger: [], negs: [], balance:{}}

