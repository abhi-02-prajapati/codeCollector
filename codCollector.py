import os
import chardet
from tqdm import tqdm

# ✅ Default supported extensions
ALLOWED_EXTENSIONS = [
    ".py", ".java", ".cpp", ".c", ".kt", ".toml", ".js", ".html", ".md", ".css"
]

def is_text_file(file_path, blocksize=512):
    try:
        with open(file_path, 'rb') as f:
            raw = f.read(blocksize)
            result = chardet.detect(raw)
            return bool(result['encoding'])
    except:
        return False

def read_file_content(file_path):
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()
            result = chardet.detect(raw)
            encoding = result['encoding']
            return raw.decode(encoding, errors='replace') if encoding else None
    except Exception as e:
        return f"[Error reading file: {e}]"

def collect_all_files(root_folder):
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for fname in filenames:
            if not fname.startswith('.'):
                full_path = os.path.join(dirpath, fname)
                if os.path.isfile(full_path):
                    all_files.append(full_path)
    return all_files

def format_file_output(full_path, file_name, content):
    return f"""
================================================================================
📂 File Path: {full_path}
📝 File Name: {file_name}
--------------------------------------------------------------------------------
{content.strip() if content else "[EMPTY OR UNREADABLE FILE]"}
"""

def main():
    print("\n📁 Project Code Exporter – Prepare your codebase for AI analysis\n")

    output_name = input("Enter name for the output file (without extension): ").strip()
    if not output_name:
        output_name = "Project_Code_Export"
    output_file = output_name + ".txt"

    project_folder = input("Enter full path of your project folder: ").strip()
    if not os.path.isdir(project_folder):
        print("❌ Error: Invalid folder path.")
        return

    # Ask user to extend allowed extensions
    print("\n🔧 Default allowed file types:")
    print(", ".join(ALLOWED_EXTENSIONS))
    choice = input("Do you want to add more extensions? (y/n): ").lower().strip()

    if choice == 'y':
        extra = input("Enter additional extensions (comma-separated, e.g. .xml,.gradle): ").strip()
        if extra:
            additional_exts = [ext.strip() if ext.startswith('.') else f".{ext.strip()}" for ext in extra.split(',')]
            ALLOWED_EXTENSIONS.extend(additional_exts)

    print(f"\n🔍 Scanning folder: {project_folder}")
    print(f"📦 Accepted extensions: {', '.join(sorted(set(ALLOWED_EXTENSIONS)))}\n")

    all_files = collect_all_files(project_folder)
    collected_entries = []

    for file_path in tqdm(all_files, desc="Processing files", unit="file"):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ALLOWED_EXTENSIONS and is_text_file(file_path):
            content = read_file_content(file_path)
            collected_entries.append(format_file_output(file_path, os.path.basename(file_path), content))

    try:
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("\n".join(collected_entries))
        print(f"\n✅ Export complete! Output saved to: {output_file}")
    except Exception as e:
        print(f"❌ Failed to save output: {e}")

if __name__ == "__main__":
    main()
