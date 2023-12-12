"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py
"""

from google.cloud import storage
import preprocessing

def main(args=None):
    print("Starting makedirs...")
    preprocessing.makedirs()
    print("Starting download...")
    preprocessing.download()
    print("Starting preprocessing...")
    preprocessing.preprocessing()
    print("Starting upload...")
    preprocessing.upload()

if __name__ == "__main__":
    main()
