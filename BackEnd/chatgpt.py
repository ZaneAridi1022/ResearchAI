import openai
from oack import AK

def argumentsInFavor(prompt):
    openai.api_key = AK
    sturcteredQuery = "Could you please give me arguments that support following claim " + prompt + "."
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": sturcteredQuery},
            ]
        )
    
    print(response["choices"][0]["message"]["content"])

    sturcteredQuery = "Could you please provide me a study for each of these arguments: " + response["choices"][0]["message"]["content"] 
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": sturcteredQuery},
            ]
        )
    
    print(response["choices"][0]["message"]["content"])

    sturcteredQuery = "Could you please provide me with URLs for these studies: " + response["choices"][0]["message"]["content"] 
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": sturcteredQuery},
            ]
        )
    
    return response["choices"][0]["message"]["content"]

# print(argumentsInFavor("Trickle down economics is bad for the United States economy."))