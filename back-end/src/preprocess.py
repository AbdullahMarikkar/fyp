import cv2
import os
import pandas as pd
from torchvision import transforms


def load_labels(csv_path):
    """Load labels from CSV with only the filename as the key."""
    df = pd.read_csv(csv_path)
    return {row["image"]: row["state"] for _, row in df.iterrows()}


def preprocess_image(image_path):
    """Load and preprocess the image."""
    img = cv2.imread(image_path)
    img = cv2.resize(img, (299, 299))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Apply transformations
    transform = transforms.Compose(
        [
            transforms.ToPILImage(),
            # transforms.Grayscale(num_output_channels=3),  # Convert to grayscale (but keep 3 channels)
            transforms.RandomHorizontalFlip(),  # Randomly flip horizontally
            transforms.RandomVerticalFlip(),  # Randomly flip vertically
            transforms.RandomRotation(
                degrees=15
            ),  # Randomly rotate by up to 15 degrees
            transforms.ColorJitter(
                brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1
            ),  # Adjust color
            transforms.RandomResizedCrop(size=299, scale=(0.8, 1.0)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    img = transform(img)
    return img


def histogram_equalization(img, save_dir=None, filename=None):
    """Enhance image using histogram equalization."""
    img_np = img.permute(1, 2, 0).numpy() * 255.0
    img_np = img_np.astype("uint8")

    img_yuv = cv2.cvtColor(img_np, cv2.COLOR_RGB2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)

    # Save the enhanced image if save_dir is provided
    if save_dir and filename:
        os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist
        save_path = os.path.join(save_dir, filename)
        cv2.imwrite(
            save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        )  # Save in BGR format

    # Plot the enhanced image
    # plt.figure(figsize=(8, 8))
    # plt.imshow(img)
    # plt.title(f"Enhanced Image: {filename}")
    # plt.axis('off')
    # plt.show()

    transform = transforms.ToTensor()
    return transform(img)


def gaussian_blur(
    img_tensor, kernel_size=(3, 3), sigma=0.5, save_dir=None, filename=None
):
    # Convert tensor to numpy array in RGB format
    img_np = img_tensor.permute(1, 2, 0).numpy() * 255.0
    img_np = img_np.astype("uint8")

    # Apply Gaussian blur
    blurred_img = cv2.GaussianBlur(img_np, kernel_size, sigmaX=sigma)

    # Optionally save
    if save_dir and filename:
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"blurred_{filename}")
        cv2.imwrite(save_path, cv2.cvtColor(blurred_img, cv2.COLOR_RGB2BGR))

    # Convert back to tensor
    transform = transforms.ToTensor()
    return transform(blurred_img)
