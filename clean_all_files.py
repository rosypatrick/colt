"""
Script to thoroughly clean all markdown files in the scraped_data directory,
removing all instances of unwanted text fragments.
"""

import os
import glob
import re
from pathlib import Path

def clean_file(file_path):
    """Clean a markdown file by removing all unwanted text fragments."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # List of specific text fragments to remove
        unwanted_fragments = [
            "Colt was founded by Jack O'Hea in 1931 and has been pioneering ventilation solutions ever since.",
            "- AboutColtColt was founded by Jack O'Hea in 1931 and has been pioneering ventilation solutions ever since.",
            "AboutColtColt was founded by Jack O'Hea in 1931 and has been pioneering ventilation solutions ever since.",
            "Jack O'Hea in 1931",
            "pioneering ventilation solutions ever since",
            "with over 85 years of climate control experience",
            "making us the longest-standing company in the field",
            "We've expanded from factory solutions to diverse building types",
            "Colt has been manufacturing and installing external solutions",
            "for almost two decades",
            "We are experts in screening and ventilation louvre panels",
            "screening whilst maintaining rain defence",
            "With decades of experience in smoke control system maintenance",
            "Colt is a trusted leader in the field",
            "We've refined our expertise across various building types",
            "ensuring safety, compliance, and reliability",
            "Explore our Resources area for downloads",
            "knowledge articles, case studies, and additional design services",
            "Access expert insights and tools to support your projects"
        ]
        
        # Remove each fragment
        for fragment in unwanted_fragments:
            if fragment in content:
                content = content.replace(fragment, "")
        
        # Use regex to remove any remaining instances with different formatting
        patterns = [
            r'Colt was founded by Jack O\'Hea in 1931.*?ventilation solutions ever since\.',
            r'AboutColt.*?ventilation solutions ever since\.',
            r'- AboutColt.*?ventilation solutions ever since\.',
            r'Climate Control Experts.*?factory solutions to diverse building types\.',
            r'Louvre Experts.*?maintaining rain defence\.',
            r'Smoke Control System Maintenance Experts.*?compliance, and reliability\.',
            r'Colt UK.*?support your projects\.'
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Clean up excessive whitespace and newlines
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r' {2,}', ' ', content)
        content = content.strip()
        
        # Check if content was changed
        if content != original_content:
            # Write the cleaned content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned {file_path}")
            return True
        else:
            print(f"No changes needed for {file_path}")
            return False
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return False

def main():
    """Process all markdown files in the scraped_data directory and its subdirectories."""
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
    print("Done. Please restart the server for changes to take effect.")

if __name__ == "__main__":
    main()
