#!/bin/bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama
ollama serve &> /dev/null &
