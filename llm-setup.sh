#!/bin/bash
ollama pull tinyllama
ollama serve &> /dev/null &
