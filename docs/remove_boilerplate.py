"""
Script to remove boilerplate text from all markdown files in the scraped_data directory.
"""

import os
import glob
import re
from pathlib import Path

# The text to remove
BOILERPLATE_TEXT = """We use cookies on our website colt.info/gb/en. Some of these cookies are essential while others help us to improve our website and personalise your experience. Please note, that if you do not accept functional and analytical cookies, some parts of our site may not work. For more information about the cookies we use please view our Privacy Policy.

Colt pioneered natural ventilation in the 1930s, with over 85 years of climate control experience, making us the longest-standing company in the field. We've expanded from factory solutions to diverse building types.

Colt has been manufacturing and installing external solutions for almost two decades. We are experts in screening and ventilation louvre panels and screening whilst maintaining rain defence.

With decades of experience in smoke control system maintenance, Colt is a trusted leader in the field. We've refined our expertise across various building types, ensuring safety, compliance, and reliability.

Explore our Resources area for downloads, knowledge articles, case studies, and additional design services. Access expert insights and tools to support your projects.

Colt was founded by Jack O'Hea in 1931 and has been pioneering ventilation solutions ever since."""

# Also remove these phrases that appear elsewhere in the files
ADDITIONAL_PHRASES = [
    "Climate Control ExpertsColt pioneered natural ventilation in the 1930s, with over 85 years of climate control experience, making us the longest-standing company in the field. We've expanded from factory solutions to diverse building types.",
    "Louvre ExpertsColt has been manufacturing and installing external solutions for almost two decades. We are experts in screening and ventilation louvre panels and screening whilst maintaining rain defence.",
    "Smoke Control System Maintenance ExpertsWith decades of experience in smoke control system maintenance, Colt is a trusted leader in the field. We've refined our expertise across various building types, ensuring safety, compliance, and reliability.",
    "Colt UKExplore our Resources area for downloads, knowledge articles, case studies, and additional design services. Access expert insights and tools to support your projects.",
    "ColtColt was founded by Jack O'Hea in 1931 and has been pioneering ventilation solutions ever since."
]

def clean_file(file_path):
    """Remove boilerplate text from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the main boilerplate text
        if BOILERPLATE_TEXT in content:
            content = content.replace(BOILERPLATE_TEXT, "")
            print(f"Removed boilerplate text from {file_path}")
        
        # Remove additional phrases
        for phrase in ADDITIONAL_PHRASES:
            if phrase in content:
                content = content.replace(phrase, "")
                print(f"Removed phrase from {file_path}")
        
        # Write the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return False

def main():
    """Process all markdown files in the scraped_data directory."""
    data_directory = "scraped_data"
    
    # Find all markdown files in the data directory and its subdirectories
    md_files = glob.glob(os.path.join(data_directory, "**/*.md"), recursive=True)
    
    if not md_files:
        print(f"No markdown files found in {data_directory}")
        return
    
    print(f"Found {len(md_files)} markdown files")
    
    # Process each markdown file
    success_count = 0
    for md_file in md_files:
        if clean_file(md_file):
            success_count += 1
    
    print(f"Successfully cleaned {success_count} out of {len(md_files)} files")

if __name__ == "__main__":
    main()
