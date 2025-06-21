import os
import pandas as pd
from PIL import Image
from torchvision import transforms
import tqdm


def augment_and_save(original_image_path, output_dir, num_versions=4):
    """
    Loads an image, applies different sets of augmentations, and saves
    the new versions. Returns a list of the new filenames.
    """
    try:
        # Open the original image
        image = Image.open(original_image_path)
    except Exception as e:
        print(f"Could not open {original_image_path}. Skipping. Error: {e}")
        return []

    # Get the base filename without extension
    base_filename = os.path.splitext(os.path.basename(original_image_path))[0]

    new_filenames = []

    # --- Define Augmentation Pipelines ---
    # NOTE: We do NOT use ToTensor() or Normalize() here because we are saving
    #       to a standard image format (like JPG/PNG). These steps are for
    #       the training pipeline only.

    # Pipeline 1: Horizontal Flip + Rotation
    augment_v1 = transforms.Compose(
        [
            transforms.RandomHorizontalFlip(p=1.0),  # Always flip horizontally
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
        ]
    )

    # Pipeline 2: Vertical Flip + Affine Transform (Shear)
    augment_v2 = transforms.Compose(
        [
            transforms.RandomVerticalFlip(p=1.0),  # Always flip vertically
            transforms.RandomAffine(degrees=0, shear=10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
        ]
    )

    # --- NEW: Pipeline 3: Perspective Transform + Grayscale ---
    # This creates a "zoomed-in" or "skewed" look and converts to grayscale
    augment_v3 = transforms.Compose(
        [
            transforms.RandomPerspective(distortion_scale=0.2, p=1.0),
            transforms.Grayscale(
                num_output_channels=3
            ),  # Keep 3 channels for model compatibility
        ]
    )

    # --- NEW: Pipeline 4: Center Crop + Hue Adjustment ---
    # This forces the model to learn from the center of the image with a different color cast
    augment_v4 = transforms.Compose(
        [  # Resize back to standard size
            transforms.ColorJitter(hue=0.2, saturation=0.3),
        ]
    )

    pipelines = [augment_v1, augment_v2, augment_v3, augment_v4]

    for i, pipeline in enumerate(pipelines[:num_versions]):
        augmented_image = pipeline(image)
        new_filename = f"{base_filename}_aug_{i + 1}.jpg"
        output_path = os.path.join(output_dir, new_filename)

        # Save the new image
        augmented_image.save(output_path)
        new_filenames.append(new_filename)

    return new_filenames


def create_augmented_dataset(original_csv_path, image_dir, output_csv_path):
    """
    Reads the original labels, generates augmented images for each entry,
    and creates a new CSV file with all original and augmented data.
    """
    print("Reading original labels...")
    df = pd.read_csv(original_csv_path)

    # Create a list to hold all data (original + augmented)
    new_data = []

    print("Starting augmentation process...")
    # Use tqdm for a progress bar
    for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        original_filename = row["image"]
        label = row["state"]

        # 1. Add the original image to our new list
        new_data.append({"image": original_filename, "state": label})

        # 2. Generate and save augmented versions
        original_image_path = os.path.join(image_dir, original_filename)
        augmented_filenames = augment_and_save(
            original_image_path, image_dir, num_versions=4
        )

        # 3. Add augmented image info to our new list
        for fname in augmented_filenames:
            new_data.append({"image": fname, "state": label})

    print("Creating new augmented CSV file...")
    # Create a new DataFrame and save it
    new_df = pd.DataFrame(new_data)
    new_df.to_csv(output_csv_path, index=False)

    print("Augmentation complete!")
    print(f"Original dataset size: {len(df)} images.")
    print(f"New augmented dataset size: {len(new_df)} images.")
    print(f"New labels file saved to: {output_csv_path}")


if __name__ == "__main__":
    # --- Configuration ---
    ORIGINAL_LABELS_CSV = "data/labels.csv"
    IMAGE_DIRECTORY = "data/images"
    AUGMENTED_LABELS_CSV = "data/labels_augmented.csv"

    # --- Run the script ---
    create_augmented_dataset(ORIGINAL_LABELS_CSV, IMAGE_DIRECTORY, AUGMENTED_LABELS_CSV)
