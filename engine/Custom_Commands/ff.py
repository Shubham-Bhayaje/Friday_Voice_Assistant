import torch
from transformers import BertTokenizer, BertModel

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Example sentence
sentence = "She locked the door with the key and went to bed."

# Tokenize input text
inputs = tokenizer(sentence, return_tensors="pt")

# Forward pass through the model
with torch.no_grad():
    outputs = model(**inputs)

# Get contextualized embeddings for each token
last_hidden_states = outputs.last_hidden_state

# Print contextualized embeddings for each token
for i, token in enumerate(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])):
    print(f'Token: {token}\tEmbedding: {last_hidden_states[0][i].tolist()}')
