import moviepy.editor as mp
import whisper
from translate import Translator
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Step 1: Extract Audio from Video
video_path = "./video_orig/Vídeo do WhatsApp de 2024-07-07 à(s) 17.02.15_43a42bc7.mp4"
audio_path = "./video_translated/extracted_audio.wav"
video_clip = mp.VideoFileClip(video_path)
video_clip.audio.write_audiofile(audio_path)

# Step 2: Transcribe Audio with Timestamps using Whisper
model = whisper.load_model("base")
result = model.transcribe(audio_path, language="pt")
segments = result['segments']

# Step 3: Translate Text to English
translator = Translator(to_lang="en")
for segment in segments:
    segment['text_en'] = translator.translate(segment['text'])

# Step 4: Generate SRT File
def format_time(seconds):
    ms = int((seconds % 1) * 1000)
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

srt_path = "./subtitle/transcription.srt"
with open(srt_path, "w") as srt_file:
    for i, segment in enumerate(segments, start=1):
        start = format_time(segment['start'])
        end = format_time(segment['end'])
        text = segment['text_en']
        srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")

srt_en_path = "./subtitle/transcription_en.srt"
# Step 5: Add Subtitles to Video
video = VideoFileClip(video_path)
subtitles = pysrt.open(srt_en_path)

def create_subtitle_clip(subtitle, video):
    text = subtitle.text
    start_time = subtitle.start.ordinal / 1000
    end_time = subtitle.end.ordinal / 1000
    duration = end_time - start_time
    # Create the text clip with the specified font size and position it at the bottom
    text_clip = (TextClip(text, fontsize=30, color='black', font='Times-Bold', method='caption', size=video.size)
                 .set_duration(duration)
                 .set_start(start_time)
                 .set_position(('center', 'bottom')))
    return text_clip

subtitle_clips = [create_subtitle_clip(sub, video) for sub in subtitles]
final_video = CompositeVideoClip([video, *subtitle_clips])
final_video_path = "./final/final_video_with_subtitles.mp4"
final_video.write_videofile(final_video_path, codec='libx264', fps=video.fps)