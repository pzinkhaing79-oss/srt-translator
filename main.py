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
        print(f"Index {sub['index']}: {sub['text']}")
