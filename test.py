import requests
import json
import re
import time
from datetime import datetime
from moviepy.editor import VideoFileClip
from PIL import Image
import io
import base64
from paddleocr import PaddleOCR
import numpy as np

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Call in a loop to create terminal progress bar
    """
    percent = f"{100 * (iteration / float(total)):.{decimals}f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()

def extract_frames(video_path, start_time, end_time, interval):
    """
    Extracts frames from a video at specified intervals.
    """
    clip = VideoFileClip(video_path)
    frames = []
    for current_time in range(int(start_time), int(end_time), int(interval)):
        frame = clip.get_frame(current_time)
        image = Image.fromarray(frame)
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        byte_data = buffer.getvalue()
        base64_image = base64.b64encode(byte_data).decode('utf-8')
        frames.append((current_time, base64_image, image))
    return frames

def call_image_generation_api(base64_image):
    """
    Calls the image generation API and returns the response.
    """
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            "model": "llava",
            "prompt": "What is in this picture? reply in chinese",
            "images": [base64_image]
        })
        response.raise_for_status()
        data_str = response.text
        json_regex = r'({.*?})'
        matches = re.findall(json_regex, data_str)
        responses = [json.loads(match)['response'] for match in matches]
        return ''.join(responses)
    except requests.RequestException as e:
        print(f"API call failed: {e}")
        return None

def recognize_text(image):
    """
    Recognizes text in the given image using PaddleOCR.
    """
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    
    # Crop the bottom part of the image where subtitles are usually located
    width, height = image.size
    cropped_image = image.crop((0, int(height * 0.8), width, height))  # Adjust the 0.8 factor as needed

    if isinstance(cropped_image, Image.Image):
        cropped_image = np.array(cropped_image)  # Convert PIL image to numpy array
    
    if cropped_image is None:
        raise ValueError("Unable to read the image. Please check the image data.")
    
    result = ocr.ocr(cropped_image, cls=True)
    
    if len(result) == 1 and result[0] == None:
        return None
    
    texts = []
    for line in result:
        for word_info in line:
            text = word_info[1]
            texts.append(text[0])
    print(' '.join(texts))
    return ' '.join(texts)

def format_time(seconds):
    """
    Converts seconds to a formatted string HH:MM:SS.
    """
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def test_image_generation_api(video_path, interval=1, start_time=0, end_time=None):
    """
    Extracts frames from a video at specified intervals, generates image descriptions,
    and saves them in a JSON file with timestamps.
    """
    clip = VideoFileClip(video_path)
    if end_time is None:
        end_time = clip.duration

    start_time = max(0, start_time)
    end_time = min(end_time, clip.duration)

    frames = extract_frames(video_path, start_time, end_time, interval)
    total_frames = len(frames)
    results = []

    for i, (current_time, base64_image, image) in enumerate(frames):
        description = call_image_generation_api(base64_image)
        text = recognize_text(image)
        if description:
            results.append({
                "time": format_time(current_time),
                "description": description,
                "text": text
            })
        print_progress_bar(i + 1, total_frames, prefix='Progress:', suffix='Complete', length=50)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"image_descriptions/image_descriptions_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    return filename

# Example usage:
filename = test_image_generation_api(r"C:\Users\17905\Desktop\未分类\21.mp4", interval=6)
print(f"Results saved to {filename}")
