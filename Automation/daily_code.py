import os
import re
import json
import subprocess
from pathlib import Path

import requests
from google import genai


ROOT = Path(__file__).resolve().parent.parent

QUESTION_URLS = [
    "https://raw.githubusercontent.com/Soumik-Maity/basic-coding-with-c/main/questions.json",
    "https://raw.githubusercontent.com/Soumik-Maity/basic-coding-with-c/main/questions2.json",
]

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def get_latest_day():
    days = []

    for item in ROOT.iterdir():
        if item.is_dir():
            match = re.fullmatch(r"Day(\d+)", item.name)

            if match:
                days.append(int(match.group(1)))

    return max(days) if days else 0


def get_existing_question_numbers():
    numbers = set()

    for file in ROOT.glob("Day*/*.c"):
        match = re.search(r"-(\d+)\.c$", file.name)

        if match:
            numbers.add(int(match.group(1)))

    return numbers


def download_questions():
    questions = []

    for url in QUESTION_URLS:
        print(f"Downloading questions from {url}")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            questions.extend(data)

        elif isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    questions.extend(value)

    return questions


def get_question_number(question):
    possible_keys = [
        "id",
        "question_id",
        "number",
        "questionNumber",
    ]

    for key in possible_keys:
        if key in question:
            try:
                return int(question[key])
            except (ValueError, TypeError):
                pass

    return None


def get_question_text(question):
    possible_keys = [
        "question",
        "text",
        "problem",
        "description",
    ]

    for key in possible_keys:
        value = question.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    return json.dumps(question, indent=2)


def generate_c_solution(number, question):
    prompt = f"""
You are solving a beginner C programming exercise.

Question number: {number}

Question:
{question}

Write a simple solution suitable for a first-year BTech CSE student.

IMPORTANT RULES:

1. Return ONLY C source code.
2. Do not use Markdown ``` fences.
3. Put the full question at the top inside a C block comment.
4. Use standard C.
5. Keep the solution simple and beginner friendly.
6. Avoid advanced techniques unless absolutely necessary.
7. Read required input from stdin.
8. Print only the required output.
9. Use meaningful variable names.
10. main() must return 0.

Example structure:

/*
Question:
The question goes here.
*/

#include <stdio.h>

int main()
{{
    // solution

    return 0;
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    code = response.text.strip()

    # Remove Markdown fences if the model accidentally sends them.
    code = re.sub(r"^```c\s*", "", code)
    code = re.sub(r"^```\s*", "", code)
    code = re.sub(r"\s*```$", "", code)

    return code.strip() + "\n"


def compile_program(source):
    executable = source.with_suffix("")

    result = subprocess.run(
        [
            "gcc",
            str(source),
            "-std=c11",
            "-Wall",
            "-Wextra",
            "-o",
            str(executable),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print()
        print(f"ERROR: {source.name} did not compile.")
        print(result.stderr)

        return False

    executable.unlink(missing_ok=True)

    print(f"{source.name} compiled successfully.")

    return True


def main():
    latest_day = get_latest_day()
    next_day = latest_day + 1

    print(f"Latest day: Day{latest_day:02d}")
    print(f"Next day: Day{next_day:02d}")

    existing_questions = get_existing_question_numbers()

    questions = download_questions()

    available = {}

    for question in questions:
        number = get_question_number(question)

        if number is None:
            continue

        if number in existing_questions:
            continue

        available[number] = question

    available = sorted(available.items())

    if not available:
        print("No new questions available.")
        return

    # First 50 days = 2 questions/day.
    # After Day 50 = 1 question/day.
    questions_today = 2 if next_day <= 50 else 1

    selected = available[:questions_today]

    if len(selected) < questions_today:
        raise RuntimeError(
            f"Only {len(selected)} question(s) available, "
            f"but {questions_today} are required."
        )

    folder = ROOT / f"Day{next_day:02d}"

    if folder.exists():
        raise RuntimeError(
            f"{folder.name} already exists. "
            "Stopping to prevent overwriting your work."
        )

    folder.mkdir()

    try:
        for number, question_data in selected:

            question = get_question_text(question_data)

            print()
            print(f"Generating Question {number}...")

            code = generate_c_solution(
                number,
                question,
            )

            filename = folder / f"day{next_day}-{number}.c"

            filename.write_text(
                code,
                encoding="utf-8",
            )

            print(f"Created: {filename}")

            if not compile_program(filename):
                raise RuntimeError(
                    f"Compilation failed for Question {number}"
                )

    except Exception:
        # Delete the new folder if something fails.
        for file in folder.glob("*"):
            file.unlink(missing_ok=True)

        folder.rmdir()

        raise

    print()
    print("=" * 40)
    print(f"Day{next_day:02d} completed!")
    print("=" * 40)


if __name__ == "__main__":
    main()