import json
import mongo_interface as mongo
from faker import Faker
import time
import random

fake = Faker()

# first, import a similar Provider or use the default one
from faker.providers import BaseProvider

# create new provider class
class MyFakerProvider(BaseProvider):
    
    def get_route(self):
        n1 = str(random.randint(1, 9))
        n2 = str(random.randint(1, 50))
        n3 = str(random.randint(1, 11))
        n4 = str(random.randint(1, 28))
	
        routes = {
	    "routes_id": "user1_" + n1 + "_" + n2,
	    "username": "user1",
	    "date": "2021-"+ n3 + "-" + n4,
	    "city": "Arezzo",
	    "route": [
		    {
			"lat": "1234",
			"long": "1234",
			"comment": "first place"
		    },
		    {
			"lat": "5679",
			"long": "4231",
			"comment": "second place"
		    }
	    ]
    	}
        return routes

print(" [X] Starting faker. Ctrl+c  to end the program")
# add new provider to faker instance
fake.add_provider(MyFakerProvider)


# using faker with a sleep of 30 seconds:
while(True):
    time.sleep(30)
    data = fake.get_route()
    mongo.create_routes(data)
    print(" fake data added")
