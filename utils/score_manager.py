import json
from config.settings import HIGH_SCORE_FILE

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return json.load(f)['high_score']
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump({'high_score': score}, f)
