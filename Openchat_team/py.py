import json

# Read data from JSON file
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

# HTML templates for user and assistant roles
user_template = '''
<div class="conversation-item">
    <div class="author user">
        <img alt="You" />
    </div>
    <div class="conversation-content-wrapper">
        <div class="conversation-content">
            {content}
        </div>
    </div>
    <time class="time" datetime="N/a" title="There was no timestamp in the JSON file">N/a</time>
</div>
'''

assistant_template = '''
<div class="conversation-item">
    <div class="author GPT-3">
        <svg width="41" height="41">
            <use xlink:href="#chatgpt" />
        </svg>
    </div>
    <div class="conversation-content-wrapper">
        <div class="conversation-content">
            {content}
        </div>
    </div>
    <time class="time" datetime="N/a" title="There was no timestamp in the JSON file">N/a</time>
</div>
'''

# Process messages and generate HTML
html_content = ''
for message in data['history'][0]['messages']:
    text = message['content']
    paragraphs = text.split('\n\n')  # Split by double newline
    formatted_paragraphs = ["</p>\n<p>".join(paragraph.split('\n')) for paragraph in paragraphs]
    formatted_text = "</p>\n<p>".join(formatted_paragraphs)
    if message['role'] == 'user':
        html_content += user_template.format(content=f'<p>{formatted_text}</p>')
    elif message['role'] == 'assistant':
        html_content += assistant_template.format(content=f'<p>{formatted_text}</p>')

# Create HTML file with the generated content
with open('out.html', 'w') as html_file:
    html_file.write(html_content)

print("HTML file 'out.html' generated successfully.")
