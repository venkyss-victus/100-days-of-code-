import os
import re

# Paste your raw question data here
DATA = """
Day 41
🔤
Q81 (Strings)
📋
Print each character of a string on a new line.
Show Sample Test Cases

Day 42
🔤
Q83 (Strings)
📋
Count vowels and consonants in a string.
Show Sample Test Cases
Input 1:
hello
Output 1:
Vowels=2, Consonants=3

🔤
Q84 (Strings)
📋
Convert a lowercase string to uppercase without using built-in functions.
Show Sample Test Cases
"""

def process_questions():
    # Split the data by "Day " to handle each day's folder
    days = DATA.split("Day ")
    
    for day_block in days:
        if not day_block.strip():
            continue
            
        lines = day_block.split("\n")
        day_number = lines[0].strip()
        folder_name = f"Day{day_number}"
        
        # Regex to find Q[Number], the Topic, and the Question Text
        pattern = r'Q(\d+)\s\((.*?)\)\n📋\n(.*?)(?=\n\S|\nDay|\Z)'
        questions = re.findall(pattern, day_block, re.DOTALL)
        
        for q_num, q_type, q_text in questions:
            # Clean up the question text
            clean_text = q_text.split("Show Sample Test Cases")[0].strip()
            
            # Look in the parent directory (../) since your script is in /Automation
            target_dir = f"../{folder_name}"
            
            if os.path.exists(target_dir):
                for filename in os.listdir(target_dir):
                    # Match the question number to the file (e.g., -81.c)
                    if f"-{q_num}." in filename:
                        file_path = os.path.join(target_dir, filename)
                        
                        with open(file_path, 'r') as f:
                            content = f.read()
                            
                        # Add the comment if it doesn't already exist
                        if not content.startswith("/*"):
                            comment = f"/*\n  Q{q_num} ({q_type}): {clean_text}\n*/\n\n"
                            with open(file_path, 'w') as f:
                                f.write(comment + content)
                            print(f"Successfully added comment to {filename}")
            else:
                print(f"Could not find folder: {folder_name}")

if __name__ == "__main__":
    process_questions()