import cv2
import numpy as np
import argparse
import os

def combine_video_and_image(video_path, image_path, output_path, crop_bottom=0, image_position='bottom'):
    # Read the video
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise Exception("Error opening video file")

    # Get video properties
    video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_height = original_height - crop_bottom
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Read and resize the image to match video width
    image = cv2.imread(image_path)
    if image is None:
        raise Exception("Error opening image file")
    
    # Calculate the height to maintain aspect ratio
    aspect_ratio = image.shape[1] / image.shape[0]
    image_height = int(video_width / aspect_ratio)
    image = cv2.resize(image, (video_width, image_height))

    # Create video writer
    combined_height = video_height + image_height
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (video_width, combined_height))

    # Process each frame
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Crop the frame if specified
        if crop_bottom > 0:
            frame = frame[0:video_height, :]
        
        # Combine image and frame vertically based on position setting
        if image_position == 'top':
            combined = np.vstack((image, frame))
        else:
            combined = np.vstack((frame, image))
        out.write(combined)

    # Release everything
    video.release()
    out.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine video and image into a single video')
    parser.add_argument('--video', default='input/video.mp4', help='Path to input video file')
    parser.add_argument('--image', default='input/image.png', help='Path to input image file')
    parser.add_argument('--output', default='output/output.mp4', help='Path to output video file')
    parser.add_argument('--crop-bottom', type=int, default=0, help='Number of pixels to crop from bottom of video')
    parser.add_argument('--image-position', choices=['top', 'bottom'], default='bottom', help='Position of image relative to video (top or bottom)')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        combine_video_and_image(args.video, args.image, args.output, args.crop_bottom, args.image_position)
        print("Video processing completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
