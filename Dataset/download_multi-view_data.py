import os
import sys
import argparse
import logging

# Configure logging for professional terminal output
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def check_dependencies():
    """
    Verifies if 'gdown' is installed in the current environment.
    Exits with a helpful installation message if missing.
    """
    try:
        import gdown
        return gdown
    except ImportError:
        logging.error("Required dependency 'gdown' is not installed.")
        print("\nFix: Please install it using the following command:")
        print("    pip install gdown\n")
        sys.exit(1)


def download_datasets(folder_url, output_dir):
    """
    Synchronizes the local data directory with the Google Drive shared folder.

    Args:
        folder_url (str): The public URL of the Google Drive folder.
        output_dir (str): Local path where datasets will be stored.
    """
    gdown = check_dependencies()

    # Ensure the target directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Initialized local data directory: {output_dir}")

    logging.info("Connecting to Google Drive remote storage...")
    logging.info(f"Remote URL: {folder_url}")

    try:
        # Download the entire folder recursively
        # remaining_ok=True allows the script to proceed if some files fail
        gdown.download_folder(
            url=folder_url,
            output=output_dir,
            quiet=False,
            remaining_ok=True
        )

        # Verification Phase
        logging.info("=" * 60)
        logging.info("Dataset synchronization complete!")
        logging.info(f"Local Storage Path: {os.path.abspath(output_dir)}")

        # Audit downloaded files
        mat_files = [f for f in os.listdir(output_dir) if f.endswith('.mat')]
        logging.info(f"Available Datasets ({len(mat_files)}): {', '.join(mat_files)}")
        logging.info("=" * 60)

    except Exception as e:
        logging.error(f"Synchronization failed: {e}")
        logging.warning("Check your internet connection and verify that the GDrive folder is public.")


def main():
    """
    Command-line interface for the Multi-view Dataset Downloader.
    """
    parser = argparse.ArgumentParser(
        description="Multi-view Learning Suite: Dataset Downloader",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--url',
        type=str,
        default='https://drive.google.com/drive/folders/1TyiQNOuCH7zn0R55EfxM4mUwB05VsoMf?usp=drive_link',
        help='Google Drive shared folder URL'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='./dataset',
        help='Local directory to save the .mat datasets'
    )

    args = parser.parse_args()
    download_datasets(args.url, args.output)


if __name__ == "__main__":
    main()
