import json
from datetime import datetime

try:
    # Load the JSON data from the file
    with open("data.json", "r", encoding='utf-8') as file:
        data = json.load(file)
except json.decoder.JSONDecodeError as e:
    # Print the error message, line number, and column number
    print(f"JSON decoding error: {e}")
    print(f"Line {e.lineno}, column {e.colno}: {e.msg}")


# Create an HTML output file
with open("out.html", "w") as html_file:
    # Define the HTML template for chatgpt and user messages
    chatgpt_template = """
    <div class="conversation-item">
        <div class="author GPT-3">
            <svg width="41" height="41">
                <use xlink:href="#chatgpt" />
            </svg>
        </div>
        <div class="conversation-content-wrapper">
            <div class="conversation-content">
                <p>{text}</p>
            </div>
        </div>
        <time class="time" datetime="{ts1}" title="{ts2}">{ts3}</time>
    </div>
    """

    user_template = """
    <div class="conversation-item">
        <div class="author user">
            <img alt="You" />
        </div>
        <div class="conversation-content-wrapper">
            <div class="conversation-content">
                <p>{text}</p>
            </div>
        </div>
        <time class="time" datetime="{ts1}" title="{ts2}">{ts3}</time>
    </div>
    """

    # Find the chat section with the specified UUID
    chat_section = None
    for chat in data["data"]["chat"]:
        if chat.get("uuid") == 1688766875794:
            chat_section = chat
            break

    if chat_section is not None:
        chat_data = chat_section["data"]
        for message in chat_data:
            TS2 = message.get("dateTime")
            text = message.get("text")
            inversion = message.get("inversion")

            if TS2 is not None and text is not None and inversion is not None:
                if inversion:
                    message["inversion"] = "user"
                    template = user_template
                else:
                    message["inversion"] = "chatgpt"
                    template = chatgpt_template

                # Replace "\n\n" with "</p><p>" in the text
                text = text.replace("\n\n", "</p><p>")

                # Convert TS2 to the desired format (e.g., "2023-09-16T00:15:44.837Z")
                try:
                    ts2_datetime = datetime.strptime(TS2, "%d/%m/%Y, %H:%M:%S")
                    TS1 = ts2_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3]  # Remove microseconds
                    TS3 = ts2_datetime.strftime("%I:%M %p")
                except ValueError:
                    TS1 = TS2  # Use the original value if the format is not as expected
                    TS3 = TS2

                # Replace placeholders in the template with actual values
                html_message = template.format(text=text, ts1=TS1, ts2=TS2, ts3=TS3)

                # Write the HTML message to the output file
                html_file.write(html_message)

# The HTML file (out.html) is now populated with the messages for the specified UUID.
