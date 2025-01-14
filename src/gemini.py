import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def ask_gemini(book_name, history):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"""本の名前と本の旅路が（タイムスタンプ、緯度、経度）の形式で与えられるので、その旅路を説明してください。なお、具体的な輸送手段には触れずに、ロマンチックな説明を心がけてください。本の名前：{book_name}本の旅路:{history}""")
    print(response.text)
    return response.text
