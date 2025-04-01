import os
import shutil
from collections import defaultdict

def organize_files_by_type(source_dir, output_dir='organized_files'):
    """Organize files in a directory by their file extensions"""
    
    if not os.path.exists(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    file_counts = defaultdict(int)
    moved_files = 0
    
    for root, _, files in os.walk(source_dir):
        for filename in files:
            # Skip files in the output directory
            if output_dir in root:
                continue
                
            file_path = os.path.join(root, filename)
            
            _, ext = os.path.splitext(filename)
            ext = ext.lower()[1:] if ext else 'no_extension'
            
            category_dir = os.path.join(output_dir, ext)
            os.makedirs(category_dir, exist_ok=True)
            
            try:
                shutil.move(file_path, os.path.join(category_dir, filename))
                file_counts[ext] += 1
                moved_files += 1
            except Exception as e:
                print(f"Failed to move {filename}: {str(e)}")
    
    # Print summary
    print(f"\nOrganized {moved_files} files:")
    for ext, count in sorted(file_counts.items()):
        print(f"{ext.upper()}: {count} files")
    
    return file_counts

if __name__ == "__main__":
    source = input("Enter directory path to organize: ")
    organize_files_by_type(source)
