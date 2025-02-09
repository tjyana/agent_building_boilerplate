import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
# import keys

MODEL = "gpt-4o"

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY in environment variables")

# Set the API key for the OpenAI package
openai.api_key = api_key

# Make an API call to OpenAI's GPT-4 endpoint

def get_openai_client():
    return OpenAI(api_key = api_key)

client = get_openai_client()

def construct_messages(system_text):
    messages=[
        {"role": "system", "content": system_text}
    ]
    return messages

def run_text_prompt_with_history(msgs, input_text, client=client):
    msgs.append({"role": "user", "content": [
            {"type": "text", "text": input_text},
        ]})
    response = client.chat.completions.create(
        model = MODEL,
        messages = msgs,
        temperature=0.0,
    )
    # msgs.append({"role": "assistant", "content": [
    #         {"type": "text", "text": response.choices[0].message.content},
    #     ]})
    return response.choices[0].message.content

def run_text_prompt(msgs, client=client):

    response = client.chat.completions.create(
        model = MODEL,
        messages = msgs,
        temperature=0.0,
    )
    return response.choices[0].message.content


def get_gpt_response(message, client):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """


                 """},
                {"role": "user", "content": message}
            ],
            temperature=0.7,  # Optional: Adjusts randomness of the output
        )

        # Print the assistant's reply
        reply = response.choices[0].message["content"]
        print("Assistant reply:", reply)
        return reply

    except Exception as e:
        print("Error calling OpenAI API:", e)
