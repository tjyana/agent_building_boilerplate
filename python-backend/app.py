from flask import Flask, request, jsonify
from dotenv import load_dotenv
import time
from flask_cors import CORS
load_dotenv()
import utils
# import keys

app = Flask(__name__)
CORS(app)

MODEL = "gpt-4o"

message_history = utils.construct_messages("""
                                           You are a helpful AI assistant who provides travel research and reccomendations
                    You are a helpful assistant for booking travel trips.
                 You need to collect folowing info:
                    1. Destination
                    2. Departure date
                    3. Return date
                    4. Number of adults

                Please ask multiple steps to get the information
                give time to user to decide and provide info

                if user doesn't know specifics, help guide them thru more q
                examples:
                user: "I want to go somewhere hot"
                assistant: "Great! Here are some options: Miami, Cancun, and Honolulu. Which one would you like to go to?"

                output format:


                some conditionals

                Once we have the following info
                    1. Destination (city)
                    2. Departure date
                    3. Return date
                    4. Number of adults

                say it is finished and provide a summary of the trip


                next_action: "message" or

                if you have all the info, call the api and return the results in the following format

                                return: json object with the following info
                {
                    "destination": "city",
                    "departure_date": "date",
                    "return_date": "date",
                    "adults": "number"
                    "budget": "number"
                }
                                           """)

@app.route('/')
def home():
    return "Server is running"



# # This is the original code
# @app.route('/get_response', methods=['POST'])
# def get_response():
#     data = request.get_json()
#     messages = data['messages']
#     print("Incoming messages", messages)
#     time.sleep(2)
#     response = utils.run_text_prompt_with_history(messages)
#     print(response)
#     return jsonify({
#         "role": "assistant",
#         "content": response
#     })

# This is the updated code
@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    messages = data['messages']
    print("Incoming messages", messages)
    time.sleep(2)

    # Assuming the user's new message is the last one in the list:
    if messages and "content" in messages[-1]:
        user_input = messages[-1]["content"]
    else:
        return jsonify({"error": "No user input provided"}), 400

    # Now pass both the message history and the new input text
    response_json = utils.run_text_prompt_with_history(messages, user_input)
    print(response_json)
    response_dict = dict(response_json)
    if response_dict['next_action'] == "message":
        print(response_json)
        return jsonify({
            "role": "assistant",
            "content": response_dict['message'],
            "data": response_json
        })



# @app.route('/get_response', methods=['POST'])
# def get_response():
#     data = request.get_json()
#     messages = data['messages']
#     print("Incoming messages", messages)
#     time.sleep(2)

#     # Assuming the user's new message is the last one in the list:
#     if messages and "content" in messages[-1]:
#         user_input = messages[-1]["content"]
#     else:
#         return jsonify({"error": "No user input provided"}), 400

#     # Now pass both the message history and the new input text
#     response_text = utils.run_text_prompt_with_history(messages, user_input)
#     print(response_text)
#     return jsonify({
#         "role": "assistant",
#         "content": response_text
#     })



# def search_serpapi(query: str) -> dict:

#     params = query.update(
#         {
#             "api_key": SERP_API_KEY,
#             "engine": "google_hotels",
#             "gl": "us",
#             "hl": "en"
#         }
#     )

#     search = GoogleSearch(params)
#     results = search.get_dict()

#     return results

# Expects json of the following form:

# {
#   "engine": "google_hotels",
#   "q": location,
#   "check_in_date": start_date,
#   "check_out_date": end_date,
#   "adults": num_adults,
#   "children": num_children,
#   "currency": "USD",
#   "gl": "us",
#   "hl": "en",
#   "api_key": SERP_API_KEY
# }


# Replace with your actual SerpAPI key
# SERP_API_KEY = keys.serp_api_key
# SERP_API_KEY = os.getenv("SERP_API_KEY")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Get query from request
    if not query:
        return jsonify({"error": "Missing search query"}), 400

    serp_url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "hl": "en",  # Language
        "gl": "us",  # Country code
    }

    response = requests.get(serp_url, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch search results"}), response.status_code

if __name__ == '__main__':
    # Debug mode should be set to False in production
    app.run(debug=True, port=8000)
