import json

def load_all_data():
    try:
        with open("data/answers.json","r",encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {"File not found."}
    except json.JSONDecodeError:
        return {"Error reading JSON file."}

def get_topic_content(subject,topic):
    try:
        with open("data/answers.json","r",encoding='utf-8') as f:
            data = json.load(f)
            return(data.get(subject,{}).get(topic,[]))
    except FileNotFoundError:
        return [{"q": "File not found.", "a": {"Normal": "", "Telugu": ""}, "keywords": []}]
    except json.JSONDecodeError:
        return [{"q": "Error reading JSON file.", "a": {"Normal": "", "Telugu": ""}, "keywords": []}]

def find_best_match(doubt,content_list):
    doubt = doubt.lower()
    best_match=None
    max_matches=0
    for item in content_list:
        matches = sum(1 for keywords in item.get("keywords",[]) if keywords.lower() in doubt)
        if matches > max_matches:
            max_matches = matches
            best_match = item
    if max_matches < 1:
        return None
    return best_match