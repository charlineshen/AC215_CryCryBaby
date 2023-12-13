"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py
"""

from google.cloud import storage
import download_from_dac

def main(args=None):
    print("Starting makedirs...")
    download_from_dac.makedirs()
    print("Starting get_dac...")
    download_from_dac.get_dac()
    print("Starting upload...")
    download_from_dac.upload()

if __name__ == "__main__":
    main()
