import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def build_report(name, age, stream, t_scores, dom, speed, correct, wrong_topics):
    prompt = f"""
Generate a full student learning report and improvement roadmap.

Student: {name}
Age: {age}
Stream: {stream}

Thinking Pattern Scores:
{t_scores}
Dominant: {dom}

Decision Speed Score: {speed}/32

Subject Quiz:
Correct: {correct}/5
Weak Questions: {wrong_topics}

Sections required:
1) Summary of how the student thinks
2) Strengths
3) Weaknesses
4) Explanation of how thinking style affects study performance
5) Guidance on what learning methods suit the student
6) 7-day roadmap (day-by-day steps)
7) 1-month long-term plan

Style: motivating, clear, professional, no generic advice.
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=1200
    )
    return res.choices[0].message.content.strip()
