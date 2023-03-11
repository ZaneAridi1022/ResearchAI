import openai
from oack import AK

def generate(prompt):
    openai.api_key = AK
    # try:
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
    return response["choices"][0]["message"]["content"]
# except:
    print("Rate limit exceeded. Please try again later.")