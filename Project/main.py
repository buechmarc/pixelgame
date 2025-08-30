import os
import random

import cv2


class pixalator():
    
    def __init__(self):
        self.pixalate_value = 16

    def set_pixalate_value(self,value):
        self.pixalate_value = max(1, value)

    def pixelate_image(self, image_path):
        # Load the image
        image = cv2.imread(image_path,cv2.IMREAD_UNCHANGED)
        image = cv2.GaussianBlur(image, (3, 3), 0)
        if image.shape[2] == 4:  # if 4 channels (alpha present)
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        # Get original dimensions
        height, width = image.shape[:2]

        # Compute the "pixelated" size
        w, h = (width // self.pixalate_value, height // self.pixalate_value)

        # Resize down to pixel size
        temp = cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)

        # Resize back to original size with nearest neighbor interpolation
        pixelated = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

        return pixelated

def collect_image_paths(root_dir):
    image_paths = []
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(foldername, filename)
                image_paths.append(full_path)
    return image_paths

def main():
    pix = pixalator()
    root_directory = 'images'
    all_images = collect_image_paths(root_directory)
    print(len(all_images))

    def get_random_index():
        return random.randint(0, len(all_images)-1)

    cv2.namedWindow('image')

    step_count = 11
    min_val = 1
    max_val = 128
    step_size = (max_val - min_val) / (step_count - 1)
    pix.set_pixalate_value(max_val)
    image_index = get_random_index()

    fixed_width = 640
    fixed_height = 480

    def on_change(x):
        pix.set_pixalate_value(int(min_val + x * step_size))

    cv2.createTrackbar('pixalate', 'image', step_count-1, step_count - 1, on_change)

    while True:
        pixelated_img = pix.pixelate_image(all_images[image_index])
        resized_image = cv2.resize(pixelated_img, (fixed_width, fixed_height), interpolation=cv2.INTER_LINEAR)
        cv2.imshow('image', resized_image)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC to exit
            break
        elif key == 32 and len(all_images) > 1:
            all_images.pop(image_index)
            image_index = get_random_index()
            pix.set_pixalate_value(max_val)
            cv2.setTrackbarPos('pixalate', 'image', step_count-1)
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
