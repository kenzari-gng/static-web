import os
import shutil
import sys
from gencontent import generate_pages_recursive



def copy_directory(src, dst):
        """Recursively copies all contents from src to dst."""
        # Ensure the target directory exists
        if not os.path.exists(dst):
            os.makedirs(dst)

        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)

            if os.path.isdir(src_path):
                # Recurse into subdirectories
                copy_directory(src_path, dst_path)
            else:
                # Copy individual files
                shutil.copy2(src_path, dst_path)

def copy_from_static_to_public():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(base_dir, "static")
    public_dir = os.path.join(base_dir, "docs")

    # Clear existing public directory
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    # Copy recursively without copytree
    copy_directory(static_dir, public_dir)


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    copy_from_static_to_public()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    from_path = os.path.join(base_dir, "content")
    template_path = os.path.join(base_dir, "template.html")
    dest_path = os.path.join(base_dir, "docs")

    generate_pages_recursive(from_path, template_path, dest_path, basepath)


if __name__ == "__main__":
    main()