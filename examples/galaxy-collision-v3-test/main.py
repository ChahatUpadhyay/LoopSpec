"""Galaxy Collision Simulator — Entry Point.

LoopSpec v3 Protocol Test: Independent reproduction of galaxy-collision-sim
Hardware: Ryzen 7 5800H + RTX 3050 (4GB VRAM)
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Launch the Galaxy Collision Simulator."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
