import openai

# Set your API key
openai.api_key = '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'  # Replace with your actual API key
def get_gpt_response(message, max_tokens=200):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                  {"role": "user", "content": message}],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


prompt = query

response = get_gpt_response(prompt)
print(response)