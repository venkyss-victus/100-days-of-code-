import os
import re
import subprocess
from pathlib import Path

import requests
from google import genai


# ============================================================
# CONFIG
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

    return max(days) if days else 0


# ============================================================
# DOWNLOAD QUESTION BANK
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

    print(f"Found {len(questions)} questions.")

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
        "Could not find question text."
    )


# ============================================================
# DETERMINE QUESTIONS FOR EACH DAY
# ============================================================

def get_question_numbers_for_day(day):

    # Day01 -> Questions 1, 2
    # Day02 -> Questions 3, 4
    # ...
    # Day45 -> Questions 89, 90
    # Day46 -> Questions 91, 92
    # ...
    # Day50 -> Questions 99, 100

    if day <= 50:
        first_question = ((day - 1) * 2) + 1

        return [
            first_question,
            first_question + 1
        ]

    # After Day50:
    # Day51 -> Question 101
    # Day52 -> Question 102
    # etc.

    return [100 + (day - 50)]


# ============================================================
# GENERATE C SOLUTION
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

1. Return ONLY valid C source code.
2. Do not use Markdown code fences.
3. Put the question at the beginning inside a C block comment.
4. Use simple beginner-friendly C.
5. Use standard C compatible with GCC C11.
6. Prefer simple loops, conditions, arrays, strings and functions.
7. Avoid unnecessarily advanced techniques.
8. Read required input from stdin.
9. Print only the output required by the problem.
10. Use understandable variable names.
11. main() must return 0.
12. Do not put explanations outside the C program.

The beginning should look like:

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
            "Gemini returned an empty response."
        )

    code = response.text.strip()

    # Remove accidental Markdown code fences.

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
# COMPILE C PROGRAM
# ============================================================

def compile_program(source_file):

    executable = source_file.with_suffix("")

    print(f"Compiling {source_file.name}...")

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
        print("COMPILATION FAILED:")
        print(result.stderr)

        executable.unlink(
            missing_ok=True
        )

        return False

    executable.unlink(
        missing_ok=True
    )

    print(
        f"{source_file.name} compiled successfully."
    )

    return True


# ============================================================
# CLEAN UP FAILED DAY
# ============================================================

def remove_day_folder(folder):

    if not folder.exists():
        return

    for file in folder.iterdir():
        if file.is_file():
            file.unlink()

    folder.rmdir()


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 50)
    print("100 DAYS OF CODE AUTOMATION")
    print("=" * 50)

    latest_day = get_latest_day()
    next_day = latest_day + 1

    print(f"Latest day: Day{latest_day:02d}")
    print(f"Next day:   Day{next_day:02d}")

    question_numbers = (
        get_question_numbers_for_day(next_day)
    )

    print(
        f"Questions for today: {question_numbers}"
    )

    # --------------------------------------------------------
    # Download questions
    # --------------------------------------------------------

    questions = download_questions()

    # Make sure required questions exist.

    for number in question_numbers:

        if number not in questions:

            raise RuntimeError(
                f"Question {number} was not found "
                "in the question bank."
            )

    # --------------------------------------------------------
    # Create next Day folder
    # --------------------------------------------------------

    day_folder = (
        ROOT /
        f"Day{next_day:02d}"
    )

    if day_folder.exists():

        raise RuntimeError(
            f"{day_folder.name} already exists. "
            "Refusing to overwrite existing work."
        )

    day_folder.mkdir()

    created_files = []

    # --------------------------------------------------------
    # Generate programs
    # --------------------------------------------------------

    try:

        for number in question_numbers:

            question_data = questions[number]

            question_text = (
                get_question_text(
                    question_data
                )
            )

            print()
            print("-" * 50)
            print(f"Question {number}")
            print(question_text)
            print("-" * 50)

            code = generate_solution(
                number,
                question_text
            )

            # Your existing naming format:
            #
            # Day46/
            # ├── day46-91.c
            # └── day46-92.c

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
                f"Created {filename.name}"
            )

            # ------------------------------------------------
            # Compile test
            # ------------------------------------------------

            if not compile_program(filename):

                raise RuntimeError(
                    f"Question {number} "
                    "failed to compile."
                )

    except Exception:

        print()
        print(
            f"Generation failed. "
            f"Removing incomplete Day{next_day:02d}."
        )

        remove_day_folder(day_folder)

        raise

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print()
    print("=" * 50)

    print(
        f"Day{next_day:02d} successfully created!"
    )

    print()

    for file in created_files:
        print(f"Created: {file.name}")

    print()
    print("All programs compiled successfully.")

    print("=" * 50)
    print()


if __name__ == "__main__":
    main()