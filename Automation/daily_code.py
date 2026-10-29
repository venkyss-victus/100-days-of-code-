import os
import re
import subprocess
from pathlib import Path

import requests
from google import genai


# ============================================================
# SETTINGS
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
# FIND CURRENT DAY
# ============================================================

def get_latest_day():
    days = []

    for item in ROOT.iterdir():

        if not item.is_dir():
            continue

        match = re.fullmatch(r"Day(\d+)", item.name)

        if match:
            days.append(int(match.group(1)))

    return max(days) if days else 0


# ============================================================
# DOWNLOAD QUESTIONS
# ============================================================

def download_questions():

    print("Downloading question bank...")

    response = requests.get(
        QUESTION_URL,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    questions = {}

    question_bank = data.get("questionBank", [])

    for section in question_bank:

        section_questions = section.get(
            "questions",
            []
        )

        for question in section_questions:

            question_id = question.get("id")

            if question_id is None:
                continue

            try:
                question_id = int(question_id)

            except (ValueError, TypeError):
                continue

            questions[question_id] = question

    print(
        f"Found {len(questions)} questions "
        "in the question bank."
    )

    return questions


# ============================================================
# GET QUESTION TEXT
# ============================================================

def get_question_text(question):

    text = question.get("text")

    if text:
        return text.strip()

    # Fallback in case website changes the name later

    for key in [
        "question",
        "problem",
        "description"
    ]:

        value = question.get(key)

        if isinstance(value, str):
            return value.strip()

    raise RuntimeError(
        "Could not find question text."
    )


# ============================================================
# GENERATE C CODE USING GEMINI
# ============================================================

def generate_solution(
    question_number,
    question_text
):

    print(
        f"Generating solution for "
        f"Question {question_number}..."
    )

    prompt = f"""
You are writing a beginner-level C programming solution
for a first-year BTech CSE student's 100 Days of Code
GitHub repository.

QUESTION NUMBER:
{question_number}

QUESTION:
{question_text}

Write the complete C program.

STRICT REQUIREMENTS:

1. Return ONLY C source code.
2. Do NOT use Markdown code fences.
3. Put the full question at the top of the file
   inside a C block comment.
4. Use simple beginner-friendly C.
5. Prefer loops, conditions, arrays, strings and
   simple functions.
6. Avoid unnecessarily advanced techniques.
7. Read input using standard input.
8. Print only the output required by the question.
9. Use meaningful variable names.
10. Include return 0; in main().
11. The program must compile using GCC with C11.
12. Do not include explanations outside the C code.

Example format:

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
        model="gemini-2.5-flash",
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    code = response.text.strip()

    # Remove Markdown fences if Gemini adds them.

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

    return code.strip() + "\n"


# ============================================================
# COMPILE GENERATED PROGRAM
# ============================================================

def compile_program(source_file):

    executable = source_file.with_suffix("")

    print(
        f"Compiling {source_file.name}..."
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
        text=True
    )

    if result.returncode != 0:

        print()
        print("COMPILATION FAILED")
        print(result.stderr)

        executable.unlink(
            missing_ok=True
        )

        return False

    executable.unlink(
        missing_ok=True
    )

    print(
        f"{source_file.name} "
        "compiled successfully."
    )

    return True


# ============================================================
# DETERMINE QUESTIONS FOR DAY
# ============================================================

def get_question_numbers_for_day(day):

    # Day 1 = Questions 1 and 2
    # Day 2 = Questions 3 and 4
    # ...
    # Day 45 = Questions 89 and 90
    # Day 46 = Questions 91 and 92
    # ...
    # Day 50 = Questions 99 and 100

    if day <= 50:

        first_question = (
            (day - 1) * 2
        ) + 1

        return [
            first_question,
            first_question + 1
        ]

    # After Day 50:
    #
    # Day 51 = Question 101
    # Day 52 = Question 102
    # etc.

    question_number = (
        100 + (day - 50)
    )

    return [question_number]


# ============================================================
# MAIN AUTOMATION
# ============================================================

def main():

    print()
    print("=" * 50)
    print("100 DAYS OF CODE AUTOMATION")
    print("=" * 50)

    latest_day = get_latest_day()

    next_day = latest_day + 1

    print(
        f"Latest day: Day{latest_day:02d}"
    )

    print(
        f"Next day:   Day{next_day:02d}"
    )

    question_numbers = (
        get_question_numbers_for_day(
            next_day
        )
    )

    print(
        "Questions for today:",
        question_numbers
    )

    # Download question bank

    questions = download_questions()

    # Make sure questions exist BEFORE
    # creating the folder.

    for number in question_numbers:

        if number not in questions:

            raise RuntimeError(
                f"Question {number} was not "
                "found in the question bank."
            )

    # Create DayXX folder

    folder = (
        ROOT /
        f"Day{next_day:02d}"
    )

    if folder.exists():

        raise RuntimeError(
            f"{folder.name} already exists. "
            "Stopping to prevent overwriting."
        )

    folder.mkdir()

    created_files = []

    try:

        for number in question_numbers:

            question_data = (
                questions[number]
            )

            question_text = (
                get_question_text(
                    question_data
                )
            )

            print()
            print("-" * 50)

            print(
                f"Question {number}:"
            )

            print(question_text)

            print("-" * 50)

            # Generate C program

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
                folder /
                f"day{next_day}-{number}.c"
            )

            filename.write_text(
                code,
                encoding="utf-8"
            )

            created_files.append(
                filename
            )

            print(
                f"Created: {filename}"
            )

            # Compile it

            if not compile_program(
                filename
            ):

                raise RuntimeError(
                    f"Question {number} "
                    "failed compilation."
                )

    except Exception:

        print()
        print(
            "Something failed."
        )

        print(
            "Removing incomplete "
            f"{folder.name}..."
        )

        # Remove generated files

        for file in folder.glob("*"):

            file.unlink(
                missing_ok=True
            )

        folder.rmdir()

        raise

    print()
    print("=" * 50)

    print(
        f"Day{next_day:02d} "
        "SUCCESSFULLY CREATED!"
    )

    print(
        "Generated files:"
    )

    for file in created_files:

        print(
            f"  - {file.name}"
        )

    print(
        "All programs compiled successfully."
    )

    print("=" * 50)
    print()


if __name__ == "__main__":
    main()