import subprocess
import sys
import torch

# PLEASE READ THE README FILE !
# PLEASE RUN " pip install -r requirements.txt " TO INSTALL ALL PACKAGES

def run_script(script_name):
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    print(f"Running {script_name}...")
    print(f"Output:\n{result.stdout}")
    if result.stderr:
        print(f"Errors:\n{result.stderr}")


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    run_script('process/process1/4points_in_the_image.py')
    run_script('process/process2/4points_in_the_video.py')
    run_script('process/process3/track_and_save_coordinates.py')
    run_script('process/process4/map_of_the_player.py')
    run_script('process/process5/homographic_poses.py')
    run_script('process/process6/speed_data.py')
    run_script('process/process7/ball_optimization.py')  
    #run_script('process/process8/ball_test.py')
    run_script('process/process9/player_ball_interaction.py')