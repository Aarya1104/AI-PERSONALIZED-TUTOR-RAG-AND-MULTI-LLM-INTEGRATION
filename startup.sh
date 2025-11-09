#!/bin/bash
ollama serve &
sleep 5
ollama pull phi3:mini
ollama pull mistral:7b
python app.py
