#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple wrapper to run NajaScript using the working interpreter
"""

import sys
import os
from interpreter_working import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_naja.py <filename>")
        return

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        interpreter = Interpreter(debug=False)
        interpreter.interpret(source)
    
    except Exception as e:
        print(f"Error executing script: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 