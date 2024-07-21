import os
import shutil
import subprocess

# Configuration
GITHUB_REPO_URL = 'https://github.com/SirPoopit/balls_bot.git'
CLONE_DIR = 'balls_bot'
BALLS_SCRIPT = 'balls_bot.py'

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}\n{result.stderr}")
        exit(1)
    return result.stdout

def clone_or_pull_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        print("Pulling latest changes...")
        run_command(f'cd {clone_dir} && git pull')
    else:
        print("Cloning repository...")
        run_command(f'git clone {repo_url} {clone_dir}')

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
            exit(1)

def main():
    # Clone or pull the repository
    clone_or_pull_repo(GITHUB_REPO_URL, CLONE_DIR)
    
    # Clear the current directory (excluding the script itself)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        if item_path != os.path.abspath(__file__):
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f'Failed to delete {item_path}. Reason: {e}')
                exit(1)

    # Copy the contents of the cloned repository to the current directory
    for item in os.listdir(CLONE_DIR):
        s = os.path.join(CLONE_DIR, item)
        d = os.path.join(current_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)

    # Run the test script
    print("Running test script...")
    run_command(f'python {BALLS_SCRIPT}')

if __name__ == "__main__":
    main()