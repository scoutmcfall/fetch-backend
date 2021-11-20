  #send data to routes via these requests
    # res = requests.post('http://localhost:5000/transaction', json=test_data)
    # res = requests.post('http://localhost:5000/spend', json={"points":-5000,"payer":"DANNON"})



    """
each transaction is read in individually and the list of positive transactions is stored in session as ledger
if it is positive, it's added to the end of ledger (a list of dictionaries)
if it's negative, it's added to negs (list of dictionaries) which the spend route iterates through, 
subtracting each from ledger and updating ledger each iteration 

so, session consists of: {ledger: [], negs: [], payer_totals:{}}

in order to return the totals/payer, iterate through the updated ledger and populate a dictionary of {payer:points}
using .get
then return that dictionary
"""