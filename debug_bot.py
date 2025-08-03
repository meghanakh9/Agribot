# -- coding: utf-8 --
import sys
import os
import ollama

def check_environment():
    print("Environment Check:")
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
    print(f"OLLAMA_HOST: {os.environ.get('OLLAMA_HOST')}")
    print(f"Current working directory: {os.getcwd()}")
    
def test_ollama():
    print("\nOllama Test:")
    client = ollama.Client(host='http://127.0.0.1:11434')
    response = client.generate(model='phi', prompt='test')
    print(f"Model response: {response}")

def import_bot():
    print("\nImporting bot interface:")
    from src import bot_interface
    print("Bot interface imported successfully")
    return bot_interface

if _name_ == "_main_":
    try:
        check_environment()
        test_ollama()
        bot_module = import_bot()
        print("\nInitializing bot...")
        bot = bot_module.BotInterface()
        print("Testing bot query...")
        response = bot.process_query("What is the best crop for Punjab weather?")
        print(f"Bot response: {response}")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print("\nTraceback:")
        traceback.print_exc()