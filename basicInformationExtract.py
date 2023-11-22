import re

pattern = r'(.*?):\s*(\S[^\n]*)(?=\s*$)'

# Find all matches in the text
matches = re.findall(pattern, pdf_text, re.MULTILINE)

# Convert matches to a dictionary for easier access
information_dict = {match[0].strip(): match[1].strip() for match in matches}

# Print out the organized information
for key, value in information_dict.items():
    print(f"{key}: {value}")