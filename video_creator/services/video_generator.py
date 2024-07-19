import os
import cv2
import numpy as np
import io

def generate_video(settings):
    fps = 24
    video_resolution = tuple(map(int, settings['resolution'].split('x')))
    total_frames = int(settings['duration'] * fps)

    bg_color = tuple(int(settings['background_color'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))[::-1]
    ft_color = tuple(int(settings['font_color'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))[::-1]

    if settings['include_stripe']:
        st_color = tuple(int(settings['stripe_color'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))[::-1]
    else:
        st_color = None

    font = cv2.FONT_HERSHEY_COMPLEX
    text_size = cv2.getTextSize(settings['text'], font, settings['font_scale'], settings['thickness'])[0]
    text_width, text_height = text_size

    if st_color:
        stripe_height = text_height + 20

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter('temp.mp4', fourcc, fps, video_resolution)

    for frame_num in range(total_frames):
        frame = np.full((video_resolution[1], video_resolution[0], 3), bg_color, dtype=np.uint8)

        if st_color:
            stripe_y1 = (video_resolution[1] // 2) - (stripe_height // 2)
            stripe_y2 = (video_resolution[1] // 2) + (stripe_height // 2)
            frame[stripe_y1:stripe_y2, :] = st_color

        x_pos = int(video_resolution[0] - (frame_num / total_frames) * (video_resolution[0] + text_width))
        y_pos = (video_resolution[1] // 2) + (text_height // 2) - 5

        cv2.putText(frame, settings['text'], (x_pos, y_pos), font, settings['font_scale'], ft_color, settings['thickness'])
        video_writer.write(frame)

    video_writer.release()
    video_stream = io.BytesIO()
    video_stream.write(open('temp.mp4', 'rb').read())
    video_stream.seek(0)
    os.remove('temp.mp4')
    return video_stream