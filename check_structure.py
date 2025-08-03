# -*- coding: utf-8 -*-
import sys
import os

def check_imports():
    print("\nChecking imports...")
    try:
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        print("\nTrying to import bot_interface...")
        from src import bot_interface
        print("✓ bot_interface imported successfully")
        
        print("\nTrying to import model_inference...")
        from src import model_inference
        print("✓ model_inference imported successfully")
        
    except ImportError as e:
        print(f"Import Error: {str(e)}")
        print("\nListing directory contents:")
        for root, dirs, files in os.walk("."):
            print(f"\nDirectory: {root}")
            for file in files:
                if file.endswith('.py'):
                    print(f"  - {file}")

if _name_ == "_main_":
    check_imports()