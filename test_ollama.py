# -- coding: utf-8 --
import ollama
import sys

print('Python version:', sys.version)
print('Testing Ollama connection...')

client = ollama.Client(host='http://127.0.0.1:11434')
response = client.generate(model='phi', prompt='test')
print('Response:', response)