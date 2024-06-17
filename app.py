# Import necessary libraries from Dash and for making HTTP requests
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import requests
import json

# Replace with your actual API URL and headers for the Llama 3 model
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}

# Define a default context to provide background information for the chatbot
DEFAULT_CONTEXT = "This is the default context that provides background information for the chatbot."

# Function to send a request to the Llama 3 model API and return the response
def query_llama_model(inputs):
    payload = {"inputs": inputs, "parameters": {"max_length": 10000}}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Smart Chatbot'),  # Title of the app
    dcc.Textarea(
        id='chat-history',  # ID for the chat history component
        readOnly=True,  # Make the text area read-only
        value='',  # Initial value of the text area
        style={'width': '100%', 'height': 400}  # Styling for the text area
    ),
    dcc.Input(
        id='user-input',  # ID for the user input component
        type='text',  # Type of input
        placeholder='Enter your question here'  # Placeholder text for the input
    ),
    html.Button(
        'Submit',  # Text on the button
        id='submit-button',  # ID for the submit button
        n_clicks=0  # Initial number of clicks
    ),
])

# Define the callback function to update the chat history
@app.callback(
    Output('chat-history', 'value'),  # Output: chat history value
    [Input('submit-button', 'n_clicks')],  # Input: number of clicks on the submit button
    [State('user-input', 'value'), State('chat-history', 'value')]  # States: user input and chat history values
)
def update_output(n_clicks, user_input, chat_history):
    if n_clicks > 0 and user_input:
        # Format the user input for question answering with the default context
        formatted_input = f"Question: {user_input}"

        # Get the response from the Llama 3 model
        result = query_llama_model(formatted_input)
        answer = result[0].get('generated_text', 'I am not sure about that.')

        # Append the answer to the chat history
        chat_history += f'{answer}\n'
        return chat_history
    return chat_history

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
