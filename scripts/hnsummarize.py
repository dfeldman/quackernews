import json
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summary(title, first_paragraph, comments):

    
# Replace with your actual API key

    # Format the comments into a single string
    comments_combined = ' '.join(comments)

    # Compose the prompt with clear instructions for the desired output style
    prompt_text = f"Create a humorous and mocking summary in the style of n-gate.com. It should be 3-4 sentences, and mock both the article and the commenters. Do not repeat the title. Use emojis or HTML em and i tags for emphasis. Make it SHORT and BITING. Title: {title}, First Paragraph: {first_paragraph}, Comments: {comments_combined}"

    # Send the request to ChatGPT
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a creative assistant."},
            {"role": "user", "content": prompt_text}
        ]
    )
    if response and response.choices and len(response.choices) > 0:
        print(response)
        content = response.choices[0].message.content.strip()
 
    # Return the generated summary
    return content

def add_summaries(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    for article in data:
        title = article['title']
        comments = article['comments']
        first_paragraph = article['first_paragraph']
        
        article['summary'] = summary(title, first_paragraph, comments)

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully generated {output_file} with summaries.")

if __name__ == '__main__':
    input_file = 'output/output.json'
    output_file = 'output/output2.json'
    add_summaries(input_file, output_file)
