# import launch_api.py call from quizzer backend
import sys
import subprocess
import os
import threading
import time

def install_dependencies():
    """Install required dependencies for Quizzer."""
    dependencies = [
        'fastapi',
        'ruamel.yaml',
        'uvicorn',
        'typing',
        'datetime',
    ]
    for dependency in dependencies:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dependency])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {dependency}: {e}")

# print(os.path.abspath("./quizzer"))
def print_working_directory():
    subprocess.run(["pwd"])
    
    
def launch_quizzer_gui():
        # Run pwd command and capture the output
    output = subprocess.run(["pwd"], capture_output=True, text=True)

    # Check the return code (0 for success)
    if output.returncode == 0:
    # Print the working directory from the standard output
        print(output.stdout)
    else:
        print("Error running pwd command")
    os.chdir("frontend-py")
    subprocess.run(["python3", "gui_interface.py"])
    
    
def launch_api():
    print("called")
    subprocess.run(["uvicorn", "api:app", "--reload"])
    
    

def main():
    sys.path.insert(0, os.path.abspath("./quizzer"))
    sys.path.insert(0, os.path.abspath("./frontend-py"))
    api_thread = threading.Thread(target=launch_api)
    quizzer_thread = threading.Thread(target=launch_quizzer_gui)

    print_working_directory()
    os.chdir("quizzer")
    api_thread.start()
    print_working_directory()
    os.chdir("..")
    print_working_directory()
    print("launched and waiting")
    time.sleep(3)
    print("starting quizzer now")
    quizzer_thread.start()
    print_working_directory()


if __name__ == "__main__": 
    install_dependencies()
    main()