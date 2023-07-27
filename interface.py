import gradio as gr
import requests

context = ""

def chatbot_interface(chat_history, user_input):
    # Extract the previous context from the chat history
    prev_context = "".join([f"{user}: {bot} " for user, bot in chat_history])

    # Update the context with the new question
    context = prev_context + user_input + " "

    response = requests.post("http://localhost:5000/chatbot", json={"question": user_input})
    response_text = response.json()["answer"]

    # Update the context with the model's response
    context += response_text + " "

    return response_text

def chat(chat_history, user_input):
    # Call your chatbot_interface function to get the response
    bot_response = chatbot_interface(chat_history, user_input)

    response = ""
    for letter in bot_response:
        response += letter + ""
        yield chat_history + [(user_input, response)]

with gr.Blocks() as demo:
    gr.Markdown('Customer Service Chatbot')
    with gr.Tab("Chat with the Bot"):
        chatbot = gr.Chatbot()
        message = gr.Textbox("Hi")
        message.submit(chat, [chatbot, message], chatbot)

demo.queue().launch(debug=True)
