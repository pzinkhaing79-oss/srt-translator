import re

def parse_srt(file_content):
    # SRT ဖိုင်ထဲက အချိန်မှတ်တွေနဲ့ စာသားတွေကို ခွဲထုတ်တဲ့ Logic
    # pattern က SRT format (index, timestamp, text) ကို ရှာဖို့ဖြစ်ပါတယ်
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?)(?=\n\n|\Z)')
    matches = pattern.findall(file_content)
    
    subtitles = []
    for m in matches:
        subtitles.append({
            "index": m[0],
            "timestamp": m[1],
            "text": m[2].strip()
        })
    return subtitles

# စမ်းသပ်ကြည့်ဖို့ (Test run)
if __name__ == "__main__":
    sample_data = "1\n00:00:01,000 --> 00:00:04,000\nHello, how are you?\n\n2\n00:00:05,000 --> 00:00:08,000\nWelcome to our app."
    result = parse_srt(sample_data)
    for sub in result:
        print(f"Index {sub['index']}: {sub['text']}")import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

def get_gemini_response(api_key, model_name, text_content):
    # API Key ကို ဝင်လာတဲ့ request အတိုင်း configure လုပ်မယ်
    genai.configure(api_key=api_key)
    
    # model_name က 'gemini-1.5-flash' သို့မဟုတ် 'gemini-1.5-pro' ဖြစ်နိုင်ပါတယ်
    model = genai.GenerativeModel(model_name)
    
    prompt = f"Translate these SRT subtitles to Burmese carefully: \n{text_content}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/translate")
async def translate_srt(
    api_key: str = Form(...), 
    model_choice: str = Form("gemini-1.5-flash"), # default ကို flash ထားမယ်
    file: UploadFile = File(...)
):
    # ၁။ ဖိုင်ကို ဖတ်မယ်
    content = await file.read()
    srt_text = content.decode("utf-8")
    
    # ၂။ SRT ကို parse လုပ်ပြီး စာသားတွေကိုပဲ ထုတ်မယ် (ယခင် အဆင့်က code ကို သုံးမယ်)
    # ၃။ Gemini ဆီ ပို့မယ်
    translated_result = get_gemini_response(api_key, model_choice, srt_text)
    
    return {"translated_text": translated_result}

