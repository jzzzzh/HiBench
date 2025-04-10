import os
import shutil

def merge_folders(src, dst):
    for root, _, files in os.walk(src):
        relative_path = os.path.relpath(root, src)
        target_dir = os.path.join(dst, relative_path)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            
            if not os.path.exists(dst_file):
                shutil.move(src_file, dst_file)
            else:
                print(f"file exist: {dst_file}")

dst = "./Results" 
src = "./Results-new"

merge_folders(src, dst)