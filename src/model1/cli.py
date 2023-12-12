"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py
"""

from google.cloud import storage
import model1

def main(args=None):
    print("Starting makedirs...")
    model1.makedirs()
    print("Starting download...")
    model1.download()
    print("Starting load_data...")
    X, y = model1.load_data()
    print("Starting model1 training...")
    model1.model1(X, y)
    print("Starting upload...")
    model1.upload()

if __name__ == "__main__":
    main()