from flask import Flask
import time
import requests
from datetime import datetime

app = Flask(__name__)

#Using just one API call for the entire page because the amount of information is small and the cost of a network trip is high
@app.route('/train_board')
def get_train_board():
	predictions, schedule = __get_predictions_and_schedule()
	departures = __get_departures(predictions, schedule)
	data = {}
	data['departures'] = departures
	today = datetime.today()
	data['day_of_week'] = today.strftime('%A')
	data['date'] = today.strftime('%m-%d-%Y')
	data['time'] = today.strftime('%-I:%M %p')

	return data

def __get_predictions_and_schedule():
	# This query URL asks for the predications of Commuter Rail (type 2) trips at North Station, we also want to include the schedule 
	# information to get more baseline information about the departues
	url = 'https://api-v3.mbta.com/predictions?filter[stop]=place-north&filter[route_type]=2&include=schedule'
	response = requests.get(url).json()
	schedule = response['included']
	#Sorting these two lists by ID ensures they will match when then are processed in parallel order
	schedule.sort(key=lambda x:x['relationships']['trip']['data']['id'])
	predictions = response['data']
	predictions.sort(key=lambda x:x['relationships']['trip']['data']['id'])

	return predictions, schedule

def __get_departures(predictions, schedule):
	departures = []
	for i in range(len(schedule)):
		train_info = {}
		if schedule[i]['attributes']['departure_time']:
			departure_str = schedule[i]['attributes']['departure_time'][:-6]
			date_time_obj = datetime.strptime(departure_str, '%Y-%m-%dT%H:%M:%S')
			departure_str = date_time_obj.strftime('%-I:%M')
			train_info['departure_time'] =  departure_str
			#t his field is used for sorting purposes since API does 
			# not provide departure times for predictions and will not 
			# sort on schedule departure times
			train_info['dep_time_obj'] = date_time_obj
			train_info['destination'] = schedule[i]['relationships']['route']['data']['id'][3:]
			train_info['status'] = predictions[i]['attributes']['status']
			#Train numbers aren't always available, so we use python's "better to ask forgiveness than permission" principle
			try:
				train_info['train_number'] = predictions[i]['relationships']['vehicle']['data']['id']
			except TypeError:
				train_info['train_number'] = 'N/A'
			departures.append(train_info)
	departures.sort(key=lambda x : x['dep_time_obj'])
	for train in departures:
		del train['dep_time_obj']

	return departures


