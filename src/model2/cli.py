"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py
"""

from google.cloud import storage
import model2

def main(args=None):
    print("Starting makedirs...")
    model2.makedirs()
    print("Starting download...")
    model2.download()
    print("Starting load_data...")
    X, y = model2.load_data()
    print("Starting model1 training...")
    model2.model2(X, y)
    print("Starting upload...")
    model2.upload()

if __name__ == "__main__":
    main()