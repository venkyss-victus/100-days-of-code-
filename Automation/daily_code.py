import os
import re
import subprocess
from pathlib import Path

import requests
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

QUESTION_URL = (
    "https://raw.githubusercontent.com/"
    "Soumik-Maity/basic-coding-with-c/main/questions.json"
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=GEMINI_API_KEY)


# ============================================================
# FIND LATEST DAY
# ============================================================

def get_latest_day():
    days = []

    for item in ROOT.iterdir():
        if item.is_dir():
            match = re.fullmatch(r"Day(\d+)", item.name)

            if match:
                days.append(int(match.group(1)))

    if not days:
        return 0

    return max(days)


# ============================================================
# DOWNLOAD QUESTIONS
# ============================================================

def download_questions():
    print("Downloading question bank...", flush=True)

    response = requests.get(
        QUESTION_URL,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    questions = {}

    for section in data.get("questionBank", []):

        for question in section.get("questions", []):

            question_id = question.get("id")

            if question_id is None:
                continue

            try:
                question_id = int(question_id)

            except (ValueError, TypeError):
                continue

            questions[question_id] = question

    print(
        f"Found {len(questions)} questions.",
        flush=True
    )

    return questions


# ============================================================
# GET QUESTION TEXT
# ============================================================

def get_question_text(question):
    text = question.get("text")

    if isinstance(text, str) and text.strip():
        return text.strip()

    for key in [
        "question",
        "problem",
        "description"
    ]:

        value = question.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    raise RuntimeError(
        "Could not find the question text."
    )


# ============================================================
# WORK OUT WHICH QUESTIONS BELONG TO EACH DAY
# ============================================================

def get_question_numbers_for_day(day):

    # Day01 = Questions 1 and 2
    # Day02 = Questions 3 and 4
    #
    # ...
    #
    # Day45 = Questions 89 and 90
    # Day46 = Questions 91 and 92
    # Day50 = Questions 99 and 100

    if day <= 50:

        first_question = ((day - 1) * 2) + 1

        return [
            first_question,
            first_question + 1
        ]

    # After Day50:
    #
    # Day51 = Question 101
    # Day52 = Question 102
    # etc.

    question_number = 100 + (day - 50)

    return [question_number]


# ============================================================
# ASK GEMINI TO WRITE C CODE
# ============================================================

def generate_solution(question_number, question_text):

    print(
        f"Generating solution for Question {question_number}...",
        flush=True
    )

    prompt = f"""
You are writing a C programming solution for a first-year
BTech CSE student's 100 Days of Code repository.

Question number:
{question_number}

Question:
{question_text}

Write the complete C program.

RULES:

1. Return ONLY C source code.
2. Do NOT use Markdown code fences.
3. Put the complete question at the top inside a C block comment.
4. Write beginner-friendly C code.
5. Use standard C compatible with GCC C11.
6. Prefer basic loops, conditions, arrays, strings and simple functions.
7. Do not use unnecessarily advanced techniques.
8. Read input from stdin where required.
9. Print only the result required by the problem.
10. Do not print prompts such as "Enter a number:" unless the question
    explicitly requires them.
11. Use understandable variable names.
12. main() must return 0.
13. Do not write explanations outside the C source code.

Use this general format:

/*
Question {question_number}:
{question_text}
*/

#include <stdio.h>

int main()
{{
    // solution

    return 0;
}}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            f"Gemini returned no code for Question {question_number}."
        )

    code = response.text.strip()

    # Remove Markdown fences if Gemini adds them anyway.

    code = re.sub(
        r"^```(?:c)?\s*",
        "",
        code
    )

    code = re.sub(
        r"\s*```$",
        "",
        code
    )

    print(
        f"Gemini finished Question {question_number}.",
        flush=True
    )

    return code.strip() + "\n"


# ============================================================
# COMPILE GENERATED C CODE
# ============================================================

def compile_program(source_file):

    executable = source_file.with_suffix("")

    print(
        f"Compiling {source_file.name}...",
        flush=True
    )

    result = subprocess.run(
        [
            "gcc",
            str(source_file),
            "-std=c11",
            "-Wall",
            "-Wextra",
            "-o",
            str(executable)
        ],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:

        print(
            f"Compilation failed for {source_file.name}.",
            flush=True
        )

        print(
            result.stderr,
            flush=True
        )

        executable.unlink(
            missing_ok=True
        )

        return False

    executable.unlink(
        missing_ok=True
    )

    print(
        f"{source_file.name} compiled successfully.",
        flush=True
    )

    return True


# ============================================================
# REMOVE AN INCOMPLETE DAY
# ============================================================

def cleanup_day_folder(folder):

    if not folder.exists():
        return

    print(
        f"Removing incomplete {folder.name}...",
        flush=True
    )

    for item in folder.iterdir():

        if item.is_file():
            item.unlink()

    folder.rmdir()


# ============================================================
# MAIN AUTOMATION
# ============================================================

def main():

    print()
    print("=" * 50)
    print("100 DAYS OF CODE AUTOMATION")
    print("=" * 50)
    print(flush=True)

    # --------------------------------------------------------
    # Find next day
    # --------------------------------------------------------

    latest_day = get_latest_day()

    next_day = latest_day + 1

    print(
        f"Latest day: Day{latest_day:02d}",
        flush=True
    )

    print(
        f"Next day:   Day{next_day:02d}",
        flush=True
    )

    # --------------------------------------------------------
    # Work out today's questions
    # --------------------------------------------------------

    question_numbers = get_question_numbers_for_day(
        next_day
    )

    print(
        f"Questions for today: {question_numbers}",
        flush=True
    )

    # --------------------------------------------------------
    # Download website questions
    # --------------------------------------------------------

    questions = download_questions()

    for number in question_numbers:

        if number not in questions:

            raise RuntimeError(
                f"Question {number} was not found "
                "in the website question bank."
            )

    # --------------------------------------------------------
    # Create next DayXX folder
    # --------------------------------------------------------

    day_folder = ROOT / f"Day{next_day:02d}"

    if day_folder.exists():

        raise RuntimeError(
            f"{day_folder.name} already exists. "
            "The automation will not overwrite it."
        )

    day_folder.mkdir()

    created_files = []

    # --------------------------------------------------------
    # Generate each question
    # --------------------------------------------------------

    try:

        for number in question_numbers:

            question_data = questions[number]

            question_text = get_question_text(
                question_data
            )

            print()
            print("-" * 50)
            print(
                f"Question {number}:",
                flush=True
            )

            print(
                question_text,
                flush=True
            )

            print("-" * 50)

            # Ask Gemini for solution

            code = generate_solution(
                number,
                question_text
            )

            # Your naming format:
            #
            # Day46/
            #   day46-91.c
            #   day46-92.c

            filename = (
                day_folder /
                f"day{next_day}-{number}.c"
            )

            filename.write_text(
                code,
                encoding="utf-8"
            )

            created_files.append(filename)

            print(
                f"Created: {filename.name}",
                flush=True
            )

            # Compile before allowing commit

            if not compile_program(filename):

                raise RuntimeError(
                    f"Generated code for Question {number} "
                    "failed compilation."
                )

    except Exception:

        print()
        print(
            "Automation failed.",
            flush=True
        )

        cleanup_day_folder(
            day_folder
        )

        raise

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print()
    print("=" * 50)

    print(
        f"Day{next_day:02d} CREATED SUCCESSFULLY",
        flush=True
    )

    print("=" * 50)

    for file in created_files:

        print(
            f"Created: {file.name}",
            flush=True
        )

    print()
    print(
        "All C programs compiled successfully.",
        flush=True
    )

    print(
        "GitHub Actions can now commit and push them.",
        flush=True
    )


if __name__ == "__main__":
    main()