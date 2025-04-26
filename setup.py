#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
import shutil
from pathlib import Path

# Create desktop entry for Linux
def create_desktop_entry():
    desktop_entry = """[Desktop Entry]
Name=NajaScript
Comment=NajaScript Programming Language Interpreter
Exec=najascript
Icon=/usr/share/najascript/assets/najascript_icon.png
Terminal=true
Type=Application
Categories=Development;IDE;
"""
    desktop_file_path = Path("najascript.desktop")
    with open(desktop_file_path, "w") as f:
        f.write(desktop_entry)
    return str(desktop_file_path)

desktop_file = create_desktop_entry()

setup(
    name="najascript",
    version="1.0.0",
    description="NajaScript Programming Language Interpreter",
    author="NajaScript Team",
    author_email="contact@najascript.com",
    url="https://najascript.com",
    packages=find_packages(),
    py_modules=["najascript", "lexer", "parser_naja", "interpreter", "naja_bytecode", "naja_llvm", "ast_nodes"],
    entry_points={
        "console_scripts": [
            "najascript=najascript:main",
        ],
    },
    data_files=[
        ("share/applications", [desktop_file]),
        ("share/najascript/assets", [
            os.path.join("assets", file) 
            for file in os.listdir("assets") 
            if os.path.isfile(os.path.join("assets", file))
        ]),
        ("share/najascript/modules", [
            os.path.join("modules", file) 
            for file in os.listdir("modules") 
            if os.path.isfile(os.path.join("modules", file))
        ]),
    ],
    include_package_data=True,
    install_requires=[
        "llvmlite",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Interpreters",
    ],
    python_requires=">=3.7",
) 