
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Set up the Groq API key
groq_client = Groq(api_key="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")

# List to store generated text
outputs = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/samai')
def index():
    return render_template('samai.html', outputs=outputs)


f = open('samai.txt','r')
r = f.read()


@app.route('/generate', methods=['POST'])
def generate():
    # Get user input from the form
    user_input = request.form.get('query')
    user= f"User Query: {user_input}, Relevant Information: {r}\n\nPlease answer the user's query based only on the relevant information provided above."
    
    if not user:
        return jsonify({'error': 'Query is required'}), 400

    # Call the Groq API to get a response
    try:
        response = get_groq_response(user)
        outputs.append({'input': user, 'response': response})
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_groq_response(user, max_tokens=150):
    chat_completion = groq_client.chat.completions.create(
        messages=[{
            "role": "system", 
            "content": "Respond intelligently by analyzing the provided data. If the information is unrelated to the prompt, tactfully mention that it falls outside the scope of your training. and gives answer for the asking question only not other information and provides the answer in concine manner and small and note that now there is Year 2025"
        }, {
            "role": "user", 
            "content": user
        }],
        model="mixtral-8x7b-32768",
        max_tokens=max_tokens
    )
    return chat_completion.choices[0].message.content


if __name__ == '__main__':
    app.run(debug=True)
