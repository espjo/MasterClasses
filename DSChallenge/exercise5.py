from flask import Flask, request
from flask_restful import Resource, Api
from sys import argv

import pandas as pd

app = Flask(__name__)
api = Api(app)

bookings_file = None
arr_port_paxs_total = None

def normalize_number(element):
	try:
		return int(element)
	except Exception as e:
		return 0

def processData():
	df = pd.read_csv(bookings_file, sep="^", usecols=["arr_port", "pax", "year"],  iterator=True, chunksize=10000)

	# Dataframes to concat partial results
	arr_port_paxs_total = None
        
	# Iterate every chunk
	for chunk in df:

		# Clean data filling nan with 0 and removing null values on top
		chunk["pax"] = chunk["pax"].fillna(0)
		chunk = chunk[(chunk["arr_port"].notnull()) & (chunk["year"].notnull()) & (chunk["pax"].notnull())]

        	# Filter data to year of interest
		chunk = chunk[chunk["year"] == 2013]

        	# Normalize arr_port codes and pax numbers
		chunk["arr_port"] = chunk["arr_port"].str.strip().str.upper()
		chunk["pax"] = chunk["pax"].apply(normalize_number)

        	# Group pax by arr_port (sum)
		arr_port_paxs = chunk.groupby(by="arr_port")["pax"].sum()

        	# Append partial results to totals
		arr_port_paxs_total = pd.concat([arr_port_paxs_total, arr_port_paxs])
        
    	# Group by arr_port over the partial results and sort descending 
	return pd.DataFrame(arr_port_paxs_total.groupby(by="arr_port").sum().sort_values(ascending=False)).reset_index()

@app.route('/topAirportsByPassengers')
def topNairports():
	try: 
		global arr_port_paxs_total
		top = request.args.get('top', default = 10, type = int)
		if top < 1:
			top = 10
		cached = False
		if arr_port_paxs_total is None:
			try:
				arr_port_paxs_total = processData()
			except Exception as e:
				return {"error": e}
		else:
			cached = True
		result = arr_port_paxs_total.head(n=top)
		return {"airports": result.to_dict(orient='index'), "cached": cached, "top": top}
	except Exception as e:
		return {"error": e}

if __name__ == '__main__':
	if len(argv) == 1:
		print("Usage: python exercise5.py <absolute path to your bookings file>")
	else:
		bookings_file = argv[1]
		if bookings_file is None or len(bookings_file) == 0:
			print("bookings file not defined")
			print("Usage: python exercise5.py <absolute path to your bookings file>")
		else:
			print(f"Using bookings file: {bookings_file}")
			app.run(debug=False)
