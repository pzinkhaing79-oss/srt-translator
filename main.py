import re
import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_srt(file_content):
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?)(?=\n\n|\Z)')
    return [{"index": m[0], "timestamp": m[1], "text": m[2].strip()} for m in pattern.findall(file_content)]

@app.post("/translate")
async def translate_api(
    api_key: str = Form(...), 
    model_choice: str = Form(...), 
    target_lang: str = Form("Burmese"), # ဘာသာစကား ရွေးချယ်မှုအသစ်
    file: UploadFile = File(...)
):
    content = (await file.read()).decode("utf-8")
    subtitles = parse_srt(content)
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_choice)
    
    chunk_size = 20
    translated_all = []
    
    # စုစုပေါင်း chunk အရေအတွက်ကို တွက်ချက်ခြင်း
    total_chunks = (len(subtitles) + chunk_size - 1) // chunk_size

    for i in range(0, len(subtitles), chunk_size):
        chunk = [s['text'] for s in subtitles[i:i + chunk_size]]
        prompt = f"Translate the following subtitles into {target_lang}. Keep the exact same number of lines and do not add any explanations:\n" + "\n".join(chunk)
        
        try:
            response = model.generate_content(prompt)
            translated_lines = response.text.strip().split('\n')
            # line count မကိုက်ရင် မူရင်းအတိုင်း ခေတ္တထားမယ်
            if len(translated_lines) != len(chunk):
                translated_all.extend(chunk)
            else:
                translated_all.extend(translated_lines)
        except:
            translated_all.extend(chunk)

    # SRT ပြန်လည်တည်ဆောက်ခြင်း
    output = ""
    for i in range(len(subtitles)):
        trans_text = translated_all[i] if i < len(translated_all) else subtitles[i]['text']
        output += f"{subtitles[i]['index']}\n{subtitles[i]['timestamp']}\n{trans_text}\n\n"
        
    return {"translated_srt": output}
