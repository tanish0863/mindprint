from core import thinking_test, speed_test, subject_quiz
from report import build_report

def main():
    print("\n=== MindPrint Full Demo ===\n")
    name = input("Name: ")
    age = input("Age: ")
    stream = input("Stream: ")
    subject = input("Subject for micro-quiz: ")

    print("\nPhase 1: Thinking pattern...")
    t_scores, dominant = thinking_test(age, stream)

    print("\nPhase 2: Decision speed...")
    speed = speed_test()

    print("\nPhase 3: Subject knowledge...")
    correct, wrong_topics = subject_quiz(age, stream, subject)

    print("\nGenerating AI roadmap report...\n")
    report = build_report(name, age, stream, t_scores, dominant, speed, correct, wrong_topics)
    print(report)

if __name__ == "__main__":
    main()
