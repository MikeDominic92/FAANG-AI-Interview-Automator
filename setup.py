from setuptools import setup
import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "sys", "os", "PyQt6", "websockets", "asyncio", "json",
        "openai", "whisper", "torch", "numpy", "sounddevice"
    ],
    "excludes": [],
    "include_files": [
        ("backend", "backend"),
    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Interview AI Assistant",
    version="1.0",
    description="AI-powered Interview Assistant",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "app.py",
            base=base,
            target_name="Interview AI Assistant.exe",
            icon="icon.ico"
        )
    ]
)
