# pip install -q -U google-generativeai
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

history = []

print("Hello I'm Charith, How can I help you? ")


while True:
    user_input = input("You : ")

    chat_session = model.start_chat(
        history= history
    )

    response = chat_session.send_message(user_input)

    model_response = response.text
    print(f'Charith : {model_response}')
    print()

    history.append({"role":"user", "parts":[user_input]})
    history.append({"role":"model", "parts":[model_response]})