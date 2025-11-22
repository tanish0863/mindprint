import os
import random
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

CORE_QUESTIONS = [
    "When you face a new problem, what do you do first?",
    "When something is complicated, how do you deal with it?",
    "How do you make decisions when you are unsure?",
    "If your first method fails, what do you usually do next?",
    "What helps you understand something fastest?",
    "When you get stuck, what do you usually rely on?",
    "What motivates you to keep working on a difficult task?",
    "How do you learn something completely new?",
    "When you plan your day, what matters most?",
    "How do you check if you have understood a concept well?",
]

OPTIONS = [
    "A) Break it down and analyze step-by-step",
    "B) Try examples and adjust until it works",
    "C) Look for a similar example or guidance to follow",
    "D) Jump in and experiment freely",
]

TRAIT_MAP = {"A": "Analytical", "B": "Experimental", "C": "Observational", "D": "Exploratory"}

def rephrase(q, age, stream):
    prompt = f"""
Rephrase the question for:
Age: {age}
Stream: {stream}
RULES:
- Do NOT change meaning
- Change only theme/context
- Output ONLY the question
Core: "{q}"
"""
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=120
    )
    return res.choices[0].message.content.strip()

def thinking_test(age, stream):
    selected = random.sample(CORE_QUESTIONS, 5)
    results = []
    for q in selected:
        pq = rephrase(q, age, stream)
        print("\n" + pq)
        for opt in OPTIONS:
            print(opt)
        while True:
            ans = input("A/B/C/D: ").upper()
            if ans in "ABCD":
                break
        results.append(ans)
    scores = {"Analytical":0, "Experimental":0, "Observational":0, "Exploratory":0}
    for r in results:
        scores[TRAIT_MAP[r]] += 1
    dominant = max(scores, key=scores.get)
    return scores, dominant

def speed_test():
    pool = [
        ("5 + 7 = ?", "12"),
        ("Opposite of 'increase'?", "decrease"),
        ("Which is bigger: 0.5 or 0.05?", "0.5"),
        ("Square root of 81?", "9")
    ]
    selected = random.sample(pool, 4)
    score = 0
    for q, correct in selected:
        print("\n" + q)
        start = time.time()
        ans = input("Answer: ").strip()
        t = time.time() - start
        if ans.lower() == correct.lower(): score += 8
        if t > 10: score -= 3
    if score < 0: score = 0
    return score

def subject_quiz(age, stream, subject):
    prompt = f"""
Generate exactly 5 MCQs for:
Age: {age}
Stream: {stream}
Subject: {subject}

STRICT FORMAT (no extra text):
Q | OptionA | OptionB | OptionC | OptionD | CORRECT LETTER

Example:
What is 2+2? | 3 | 4 | 5 | 6 | B
"""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=600
    )
    lines = resp.choices[0].message.content.strip().split("\n")

    correct = 0
    wrong_topics = []

    for line in lines:
        parts = [p.strip() for p in line.split("|")]

        # Skip malformed lines safely
        if len(parts) != 6:
            continue

        q, a, b, c, d, correct_option = parts
        print(f"\n{q}")
        print(f"A) {a}")
        print(f"B) {b}")
        print(f"C) {c}")
        print(f"D) {d}")

        user = input("A/B/C/D: ").upper()
        if user == correct_option.upper():
            correct += 1
        else:
            wrong_topics.append(q)

    return correct, wrong_topics
