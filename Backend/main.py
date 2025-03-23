import sys
import subprocess

def run_script(script_name):
    # Run a script using subprocess; adjust "python3" if needed.
    subprocess.run(["python3", script_name])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py [data|train|predict]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "data":
        # Run the data collection script
        run_script("Backend/data_collection.py")
    elif command == "train":
        # Run the training script
        run_script("Backend/train_model.py")
    elif command == "predict":
        # Run the real-time prediction script
        run_script("Backend/realtime_prediction.py")
    else:
        print("Invalid command. Use 'data', 'train', or 'predict'.")
