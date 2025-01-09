import json
import os
import random

working_dir = os.path.dirname(os.path.abspath(__file__))
correct_data_f = os.path.join(working_dir, 'correct.txt')
incorrect_data_f = os.path.join(working_dir, 'incorrect.txt')
verify_f = os.path.join(working_dir, 'verify.txt')
training_data_f = os.path.join(working_dir, 'training_data.jsonl')
validation_data_f = os.path.join(working_dir, 'validation_data.jsonl')

def create_data(source_file_path, classification):
    with open(source_file_path, 'r') as f_read, open(training_data_f, 'a') as f_training, open(validation_data_f, 'a') as f_validation:
        for line in f_read:
            new_json = {
                'messages': [
                    {'role': 'system', 'content': 'Data classification'},
                    {'role': 'user', 'content': line.strip()},
                    {'role': 'assistant', 'content': classification}
                ]
            }
            if random.random() < 0.1:
                f_validation.write(f'{json.dumps(new_json)}\n')
            else:
                f_training.write(f'{json.dumps(new_json)}\n')

if not os.path.exists(training_data_f) and not os.path.exists(validation_data_f):
    print('files not found, creating...')
    create_data(correct_data_f, 'CORRECT')
    create_data(incorrect_data_f, 'INCORRECT')
    print('files created')
else: 
    print('training and/or validation data files already exist, use them or delete them both and rerun this script to create new ones')