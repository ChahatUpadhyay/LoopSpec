"""
Launch the galaxy collision simulation GUI.

Run this script to start the PyQt6 application with vispy rendering.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication


def main():
    """Main entry point for simulation GUI."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
