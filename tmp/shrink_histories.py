import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def shrink_history_file(dir_path, filename):
    file_path = os.path.join(dir_path, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Shrinking {file_path}...")
    original_size = os.path.getsize(file_path) / (1024 * 1024)
    print(f"  Original size: {original_size:.2f} MB")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    shrunk_data = {}
    for seed_key, seed_data in data.items():
        shrunk_data[seed_key] = {}
        
        # We only keep 'episode_rewards' and 'epsilons'
        # Downsample by a factor of 50
        for key in ['episode_rewards', 'epsilons']:
            if key in seed_data:
                shrunk_data[seed_key][key] = seed_data[key][::50]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(shrunk_data, f, separators=(',', ':')) # Compact JSON formatting

    new_size = os.path.getsize(file_path) / (1024 * 1024)
    print(f"  New size: {new_size:.2f} MB (Reduced by {(1 - new_size/original_size)*100:.1f}%)")

def main():
    directories = [
        os.path.join(PROJECT_ROOT, 'results'),
        os.path.join(PROJECT_ROOT, 'results_100k')
    ]
    files = [
        'q_learning_history.json',
        'sarsa_history.json',
        'double_q_learning_history.json'
    ]
    for d in directories:
        if os.path.exists(d):
            for f in files:
                shrink_history_file(d, f)

if __name__ == '__main__':
    main()
