import openai

def create_caption (script: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You summarize prompts into funy video captions that are less than a sentence long"},
                {"role": "user", "content": f"Please the following story a short, funny caption: {script}"}
            ],
        temperature=0.2,
        max_tokens=80
    )
    return response['choices'][0]['message']['content']
