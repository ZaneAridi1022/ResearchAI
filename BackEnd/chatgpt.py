import openai

def generate(self, prompt, n):
    try:
        generated_answers = []
        for i in range(n):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )
            generated_answers.append(response["choices"][0]["message"]["content"])
        return generated_answers
    except:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=2048,
                n=n,
            )
            generated_answers = [response_text["text"].strip() for response_text in response["choices"]]
            return generated_answers
        except BaseException:
            raise "Rate limit exceeded. Please try again later."