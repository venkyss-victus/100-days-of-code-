import os
import glob
import subprocess

def get_clipboard_text():
    return subprocess.check_output(['pbpaste'], text=True)

def add_comment_to_c_file(day_folder, q_num, question_text):
    search_pattern = os.path.join(day_folder, f"*{q_num.replace('Q', '')}*.c")
    matching_files = glob.glob(search_pattern)
    
    if matching_files:
        target_file = matching_files[0]
        comment = f"/*\n * {q_num}: {question_text}\n */\n\n"
        
        with open(target_file, 'r') as f:
            existing_content = f.read()
            
        if not existing_content.startswith("/*"):
            with open(target_file, 'w') as f:
                f.write(comment + existing_content)
            print(f"SUCCESS: Added comment to {target_file}")
    else:
        print(f"WARNING: No .c file found for {q_num} in {day_folder}")

def process_questions():
    data = get_clipboard_text()
    current_day = None
    
    lines = [line.strip() for line in data.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        # Remove markdown hashes for easier matching
        clean_line = lines[i].replace('#', '').strip()
        
        if clean_line.startswith("Day "):
            current_day = clean_line.replace(" ", "")
            print(f"Found {current_day}...")
            i += 1
            continue
            
        if clean_line.startswith("Q") and "(" in clean_line:
            current_q_num = clean_line.split()[0]
            i += 1
            
            # Skip icons or formatting lines
            while i < len(lines) and lines[i] in ["📋", "```", "🔢", "🔲"]:
                i += 1
                
            if i < len(lines):
                question_text = lines[i]
                # Skip if it accidentally grabbed a label instead of the question
                if "Sample Test Cases" not in question_text and not question_text.startswith("Input"):
                    if current_day and os.path.exists(current_day):
                        add_comment_to_c_file(current_day, current_q_num, question_text)
                i += 1
            continue
            
        i += 1

if __name__ == "__main__":
    process_questions()