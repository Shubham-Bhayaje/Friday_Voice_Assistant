from hugchat import hugchat
def chatBo(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cokkis.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response  = chatbot.chat(user_input)
    print(response)
    
    # Extract important words
    important_words_list = extract_important_words(response)
    print("Important words:", important_words_list)

    return response

def extract_important_words(response):
    # Check if response is a valid Message object
    if isinstance(response, hugchat.Message):
        # Extract important words from the response text
        text = response.text
        important_words_list = [line.strip("*").strip() for line in text.split("\n") if line.strip()]
        return important_words_list
    else:
        print("Invalid response format")
        return []

query = "Extract important words from the user input and give in list format,dont give anything even explanation: i want book bus ticket"
chatBo(query)