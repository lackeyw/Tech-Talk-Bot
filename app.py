import requests
import time
import sys
import string
import os
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['POST'])
def respond_to_message():

	callback = request.json(silent=True)

	payload = {
			"bot_id" : "fd4639380b059b8db9b34c4e14",
			"text" : 0
		}

	message_text = callback["text"]

	message_text = message_text.lower()

	if message_text[0:4] == "!bot":

		if "heroku status" in message_text:
			payload["text"] = "Heroku is up and running"

		elif "weather" in message_text:
			weather_payload = { 
			"zip" : "28211",
			"units" : "imperial",
			"appid" : "b4776ecbb9eb16180ab1951e1b237a16"
			}
			city_index = message_text.find(" in ")
			city_index = city_index + 4
			city = message_text[city_index:]
			weather_payload["zip"] = city
			r = requests.get("http://api.openweathermap.org/data/2.5/weather", params = weather_payload)
			city_temp = r.json()["main"]
			city_high = round(city_temp["temp_max"])
			city_low = round(city_temp["temp_min"])
			city_weather = r.json()["weather"]
			description = city_weather[0]
			weather_full = "Today in " + city +", the weather is " + description["description"] + " with a high of " + str(city_high) + " and a low of " + str(city_low) + "."
			payload["text"] = weather_full
			

		elif "scoreboard" in message_text:
			list_o_likes = []
			empty_q = {"message_text" : "", "num_of_likes" : "0", "user" : ""}
			r = requests.get('https://api.groupme.com/v3/groups/49437486/likes?period=week&token=Xnxazjnd5LYTfTaoKLewd1zhVBFHbIlXNYyfXttg')
			rJson = r.json()["response"]
			liked_messages = rJson["messages"]
			for i in liked_messages:
				q = {"message_text" : i["text"], "num_of_likes" : str(len(i["favorited_by"])), "user" : i["name"]}
				list_o_likes.append(q)

			if len(list_o_likes) < 5:
				for j in (0, 5- len(list_o_likes)):
					list_o_likes.append(empty_q)

			scoreboard_text = "The top five most-liked messages of the past week are:\n1. " + list_o_likes[0]["user"] + ":'" + list_o_likes[0]["message_text"] + "', " + list_o_likes[0]["num_of_likes"] + " likes\n2. " + list_o_likes[1]["user"] + ":'" + list_o_likes[1]["message_text"] + "', " + list_o_likes[1]["num_of_likes"] + " likes\n3. " + list_o_likes[2]["user"] + ":'" + list_o_likes[2]["message_text"] + "', " + list_o_likes[2]["num_of_likes"] + " likes\n4. " + list_o_likes[3]["user"] + ":'" + list_o_likes[3]["message_text"] + "', " + list_o_likes[3]["num_of_likes"] + " likes\n5. " + list_o_likes[4]["user"] + ":'" + list_o_likes[4]["message_text"] + "', " + list_o_likes[4]["num_of_likes"] + " likes\n"
			payload["text"] = scoreboard_text

		else:
			payload["text"] = "I'm sorry, I could not understand your request."

		print(payload["text"])
		r = requests.post('https://api.groupme.com/v3/bots/post', params = payload)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
