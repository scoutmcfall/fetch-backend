  #send data to routes via these requests
    # res = requests.post('http://localhost:5000/transaction', json=test_data)
    # res = requests.post('http://localhost:5000/spend', json={"points":-5000,"payer":"DANNON"})


    session to track individual transactions including the payer
    and a ledger, which is a list of tuples (timestamp, points, payer), in order to be able to sort by timestamp 
    so we can use the oldest points first