from datasets import load_dataset
import json

def download_data(num_samples=5000):
    dataset = load_dataset("open_subtitles", lang1="en", lang2="vi", split="train[:5000]")
    
    list_data = []
    for data in dataset:
        list_data.append(data)
    with open('example_data.json','w') as f:
        json.dump(list_data, f, indent=4)

if __name__ == '__main__':
    download_data()