from ollama import Client

client = Client(host='http://localhost:11434')
response = client.chat(
    model='phi3',
    messages=[{'role': 'user', 'content': 'What is the capital of the UAE?'}]
)
print(response['message']['content'])