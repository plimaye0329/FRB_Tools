import subprocess
import argparse

def run_commands_from_file(commands_file, common_path):
    with open(commands_file, 'r') as file:
        commands = file.readlines()
    
    for command in commands:
        command = command.strip()  # Remove any leading/trailing whitespace
        if command:
            # Replace <common_path> placeholder with the actual common path
            command = command.replace('<common_path>', common_path)
            
            print(f"Executing: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Success: {command}")
            else:
                print(f"Error: {result.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute a list of commands from a file with placeholders.")
    parser.add_argument('commands_file', type=str, help='Path to the file containing commands.')
    parser.add_argument('common_path', type=str, help='Common path to replace in commands.')
    args = parser.parse_args()

    run_commands_from_file(args.commands_file, args.common_path)

