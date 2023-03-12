import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def generate(prompt):
    # try:
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
    return response["choices"][0]["message"]["content"]

topic = "trickle down economics"
json_format = "{'topic':topic, 'supporting_arguments':[], 'refuting_arguments':[]}"
print(generate(f"Please provide supporting and refuting arguments for {topic} in JSON format like so {json_format}.  Please include short taglines for each argument that succinctly capture its main point."))


