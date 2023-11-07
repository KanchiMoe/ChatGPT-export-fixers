import json
from datetime import datetime

def format_timestamp(timestamp):
    timestamp = float(timestamp)
    dt = datetime.utcfromtimestamp(timestamp)
    formatted_ts1 = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
    formatted_ts3 = dt.strftime('%I:%M %p')
    formatted_ts2 = dt.strftime('%d/%m/%Y, %H:%M:%S')
    return formatted_ts1, formatted_ts3, formatted_ts2

def find_message_chain(data, message_id):
    for item in data:
        if "mapping" in item:
            mapping = item["mapping"]
            if message_id in mapping:
                message = mapping[message_id]
                parent_id = message.get("parent")
                child_ids = message.get("children", [])
                return message_id, parent_id, child_ids

    return None, None, []

def find_message_path(data, start_message_id, end_message_id):
    def find_path_helper(current_id, path):
        if current_id == end_message_id:
            return path + [current_id]

        _, _, child_ids = find_message_chain(data, current_id)
        for child_id in child_ids:
            new_path = find_path_helper(child_id, path + [current_id])
            if new_path:
                return new_path

        return None

    path = find_path_helper(start_message_id, [])
    return path

with open('data.json', 'r') as json_file:
    data = json.load(json_file)

start_message_id = "aaa2776b-4f06-4fb3-a28a-6fc0952466fb"
end_message_id = "9c0a31c2-7515-4fb4-b53e-f15395f3b241"

output_file = "out.html"

path = find_message_path(data, start_message_id, end_message_id)

if path:
    with open(output_file, "w") as out_file:
        for i in range(len(path)):
            message_id, _, _ = find_message_chain(data, path[i])
            message = data[0]["mapping"][message_id]["message"]
            author = message["author"]["role"]
            content = message["content"]["parts"][0] if message["content"]["parts"] else "No content"
            timestamp_ts1, timestamp_ts3, timestamp_ts2 = format_timestamp(message["create_time"])

            current_message_id = path[i]
            next_message_id = path[i + 1] if i < len(path) - 1 else None
            next_message_id_text = f"next: {next_message_id}" if next_message_id else ""

            content = content.replace("\n\n", "</p>\n<p>").replace("\n", " ")

            if author == "user":
                html_block = f'''
                    <div class="conversation-item">
                        <div class="author user">
                            <img alt="You" />
                        </div>
                        <div class="conversation-content-wrapper">
                            <div class="conversation-content">
                                <p>{content}</p>
                            </div>
                        </div>
                        <time class="time" datetime="{timestamp_ts1}" title="{timestamp_ts2}">{timestamp_ts3} current: {current_message_id} {next_message_id_text}</time>
                    </div>
                '''
            elif author == "assistant":
                html_block = f'''
                    <div class="conversation-item">
                        <div class="author GPT-3">
                            <svg width="41" height="41"><use xlink:href="#chatgpt" /></svg>
                        </div>
                        <div class "conversation-content-wrapper">
                            <div class="conversation-content">
                                <p>{content}</p>
                            </div>
                        </div>
                        <time class="time" datetime="{timestamp_ts1}" title="{timestamp_ts2}">{timestamp_ts3} current: {current_message_id} {next_message_id_text}</time>
                    </div>
                '''

            out_file.write(html_block)
            out_file.write("\n")
else:
    print(f"No path found from {start_message_id} to {end_message_id}.")

print(f"Output written to {output_file}.")
