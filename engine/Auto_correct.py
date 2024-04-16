from hugchat import hugchat

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cokkis.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response  = chatbot.chat(user_input)
    print(response)
    return response
query = "only correct following text and dont give anything even explanation dont even provide(Corrected: This is an example of a spelling mistake.):- Thi is an example of speling mstake"
chatBot(query)
