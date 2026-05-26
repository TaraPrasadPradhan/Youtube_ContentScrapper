import os
from openai import OpenAI
from dotenv import load_dotenv
from Youtube import fetch_script,get_video_title
from fpdf import FPDF

load_dotenv(override=True)

api_key=os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Key Not Found")
elif not api_key.startswith('AIza'):
    print("Wrong Api Key Found")
else:
    print("Key Found")


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

gemini = OpenAI(
   base_url=GEMINI_BASE_URL,
   api_key=api_key
)

url=input("Enter the URL")
Data=fetch_script(url)
MODEL = "gemini-2.5-flash-lite"
SystemPrompt="""
You are a helpful assistant.

Analyze the YouTube transcript carefully.

Tasks:
1. Give short overview
2. Extract important learning points
3. Create MCQ questions
4. Provide answers
5. Use markdown format

"""
UserPrompt=f"""
Please generate 5 important mcq question from the given content +{Data},
and generate a pdf
"""

response=gemini.chat.completions.create(
    model=MODEL,
    messages=[
        {'role':'system','content':SystemPrompt},
        {'role':'user','content':UserPrompt}

    ]

)
# print(response.choices[0].message.content)
content = response.choices[0].message.content


title=get_video_title(url)
SPrompt="generate a short filename"
Uprompt=f"""from this youtube video tile genaret one short filename for save this video content as pdf
title:{title}
"""
response=gemini.chat.completions.create(
    model=MODEL,
    messages=[
        {'role':'system','content':SPrompt},
        {'role':'user','content':Uprompt}

    ]

)
filename=response.choices[0].message.content


print(filename)

def generate_pdf(content, filename="document.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, content)

    pdf.output(filename)

    print(f"PDF saved as {filename}")

generate_pdf(content,filename=filename)


