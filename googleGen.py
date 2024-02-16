import requests
import random
import os
import urllib.parse
from openai import OpenAI

from googleapiclient.discovery import build


def google_images(query,key,cse_id):
    service = build("customsearch", "v1", developerKey=key)
    res = service.cse().list(q=query+" book front cover", cx=cse_id, searchType='image').execute()    
    #print(query+"book cover")
    return res['items'][0]['link']

    
def get_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    # Get the current working directory
    cwd = os.getcwd()

    # Build the path to the API key file
    api_key_file = os.path.join(cwd, "google", "api_key.txt")

    # Open the file and read the key
    with open(api_key_file, "r") as f:
        api_key = f.read()

    # Build the path to the CSE ID file
    cse_id_file = os.path.join(cwd, "google", "cse_id.txt")

    # Open the CSE ID file and read the CSE ID
    with open(cse_id_file, "r") as f:
        cse_id = f.read()

    # Build the path to the google images key file
    google_key_file = os.path.join(cwd, "google", "custom_search.txt")
    # # Open the file and read the key for google images
    with open(google_key_file, "r") as f:
        google_key = f.read()
        
    # Read the OPENAI_API_KEY from the environment
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Print the API key
    print("API Key:", openai_api_key)
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Come up with philosophical questions."},
            {"role": "assistant", "content": "What is the true meaning of life?\nWhat is the secret to happiness?"},
            {"role": "user", "content": "Come up with philosophical questions."},
            {"role": "system", "content": "temperature=2\nmax_tokens=4"}        
        ]
    )

    # Extract and print only the response text
    response_text = completion.choices[0].message.content
    print(response_text)

    # Print the API key and CSE ID
    print(api_key)
    print(cse_id)

    # Split the response text into lines and filter out empty lines
    questions_list = [line.strip() for line in response_text.splitlines() if line.strip()]
    questions = ["What is the meaning of life?", "What is the purpose of existence?", "Why are we here?", "What is the secret to happiness?", "What is the key to success?"]

    # Select a random question
    #question = random.choice(questions)
    # Select a random question
    question = random.choice(questions_list)
    print(question)
    # Build the API endpoint URL for google Books API
    url = f"https://www.googleapis.com/books/v1/volumes?q={question}&key={api_key}"

    # Send the GET request
    response = requests.get(url)

    #set to store the titles
    titles = set()

    if response.status_code == 200:
        data = response.json()
        # items is a field of dictionaries returned by the json format.
        books = data['items']
        # Books is a list of dictionaries
        total_books = min(len(books), 3)
        # Get the current working directory
        cwd = os.getcwd()
        question_folder = os.path.join(cwd, "covers", question.replace("?", ""))
        os.makedirs(question_folder, exist_ok=True)       
        i = 0
        while i<total_books:
            title = books[i]['volumeInfo']['title']
            #author = books[i]['volumeInfo']['authors'][0]
            if title not in titles:
                print(title)

                book_cover_url=google_images(title,google_key,cse_id)
                image=get_image(book_cover_url)
                # Replace invalid characters in the title with underscores
                title = title.replace("/", "")
                title = title.replace(":", "")
                title = title.replace("?", "")
                title = title.replace("\"", "")
                print(title)
                # Write the image to a file
                if image is not None:
                    titles.add(title)
                    # Build the path to the cover image file
                    cover_path = os.path.join(question_folder, f"{title}.jpg")  
                    with open(cover_path, "wb") as f:
                        f.write(image)
                else:
                    print(f"Error: Could not retrieve cover image for '{title}'")
            i=i+1    
    else:
        print(f"Error: {response.status_code}")

    # Convert set to list
    titles_list = list(titles)

    voiceover_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Create a script for a 30-second video."},
            {"role": "user", "content": "Start with the question"+question+".Then, introduce a collection of"
            +"thought-provoking books, each exploring different facets of the question. As you showcase the book titles of"+ 
            ", ".join([f"{title}" for title in titles_list[:-1]]) + f", and {titles_list[-1]}, make the script in a way that connects the books to the overarching theme."},
            {"role": "user", "content": "Before introducing the next title, leave a gap so the viewer can absorb what you say about the previous book."
             + "Fill the gaps with a script that connects the books to the overarching theme."},
            {"role": "user", "content": "Output should only include the script words in a single string."},
            {"role": "system", "content": "temperature=2\nfrequency_penalty=1"}


        ]
    )

    # Extract only the response text
    voiceover_response_text = voiceover_completion.choices[0].message.content
    print(voiceover_response_text)
    
    voiceover_response_text_path = os.path.join(question_folder, "voiceover_response_text.txt")  
    # Optional Step to write the response to a txt file.
    # Open the file in write mode ('w')
    with open(voiceover_response_text_path, 'w') as file:
        # Write the string to the file
        file.write(voiceover_response_text)
    #print(type(voiceover_response_text))
        
    hashtags_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "For the following voiceover:"+voiceover_response_text+", provide hashtags that are space separated and suitable for Tik Tok."}  
        ]
    )

    # Extract only the response text
    tiktok_hashtags = hashtags_completion.choices[0].message.content
    print(tiktok_hashtags)
    
    tiktok_hashtags_path = os.path.join(question_folder, "tiktok_hashtags.txt")  
    # Optional Step to write the response to a txt file.
    # Open the file in write mode ('w')
    with open(tiktok_hashtags_path, 'w') as file:
        # Write the string to the file
        file.write(tiktok_hashtags)

    speech_file_path = os.path.join(question_folder,question.replace("?", "")+"_voiceover.mp3") 
    voiceover_response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=voiceover_response_text
    )
    #print(voiceover_response)
    #print(type(voiceover_response))
    with open(speech_file_path, 'wb') as file:
        file.write(voiceover_response.content)
    #voiceover_response.stream_to_file(speech_file_path)

if __name__ == "__main__":
    main()



                          