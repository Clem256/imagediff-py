import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from core import compare_images, render_heatmap
from ui.components import ImageCard


class ImageDiffApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Binary Image Diff & Heatmap (PyQt6)")
        self.setFixedSize(1020, 680)

        self.path_a: str | None = None
        self.path_b: str | None = None

        self._apply_dark_theme()
        self._build_ui()

    def _apply_dark_theme(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #181818;
            }
            QLabel {
                color: #f0f0f0;
                font-family: sans-serif;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #333333;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #2563eb;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #ffffff;
                width: 14px;
                margin-top: -4px;
                margin-bottom: -4px;
                border-radius: 7px;
            }
        """
        )

    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # Header Title
        title_lbl = QLabel("Binary Space Partitioning Diff")
        title_lbl.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_lbl)

        # 3 Preview Cards: Image A | Heatmap | Image B
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)

        self.card_a = ImageCard("Image A", on_browse=self._browse_a)
        cards_layout.addWidget(self.card_a)

        self.card_diff = ImageCard("Diff / Heatmap")
        cards_layout.addWidget(self.card_diff)

        self.card_b = ImageCard("Image B", on_browse=self._browse_b)
        cards_layout.addWidget(self.card_b)

        main_layout.addLayout(cards_layout)

        # Parameters Box
        controls_layout = QGridLayout()
        controls_layout.setHorizontalSpacing(24)
        controls_layout.setVerticalSpacing(6)

        # Slider: min_block
        self.min_block_lbl = QLabel("min_block : 6")
        self.min_block_lbl.setStyleSheet("font-weight: bold;")
        self.slider_min_block = QSlider(Qt.Orientation.Horizontal)
        self.slider_min_block.setRange(2, 64)
        self.slider_min_block.setValue(6)
        self.slider_min_block.valueChanged.connect(
            lambda v: self.min_block_lbl.setText(f"min_block : {v}")
        )
        controls_layout.addWidget(self.min_block_lbl, 0, 0)
        controls_layout.addWidget(self.slider_min_block, 1, 0)

        # Slider: tolerance
        self.tolerance_lbl = QLabel("tolerance : 40")
        self.tolerance_lbl.setStyleSheet("font-weight: bold;")
        self.slider_tolerance = QSlider(Qt.Orientation.Horizontal)
        self.slider_tolerance.setRange(0, 255)
        self.slider_tolerance.setValue(40)
        self.slider_tolerance.valueChanged.connect(
            lambda v: self.tolerance_lbl.setText(f"tolerance : {v}")
        )
        controls_layout.addWidget(self.tolerance_lbl, 0, 1)
        controls_layout.addWidget(self.slider_tolerance, 1, 1)

        main_layout.addLayout(controls_layout)

        # Action Button
        self.run_btn = QPushButton("Run Comparison")
        self.run_btn.setFixedHeight(42)
        self.run_btn.setStyleSheet("font-size: 15px; margin-top: 6px;")
        self.run_btn.clicked.connect(self._run_diff)
        main_layout.addWidget(self.run_btn)

        # Results Label
        self.result_lbl = QLabel("Select two images to start analysis")
        self.result_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_lbl.setStyleSheet("color: #888888; font-size: 15px;")
        main_layout.addWidget(self.result_lbl)

    def _browse_a(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image A",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        if file_path:
            self.path_a = file_path
            self.card_a.set_image(file_path)

    def _browse_b(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image B",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        if file_path:
            self.path_b = file_path
            self.card_b.set_image(file_path)

    def _run_diff(self) -> None:
        if not self.path_a or not self.path_b:
            self.result_lbl.setText("Please select both images first.")
            self.result_lbl.setStyleSheet("color: #f87171; font-size: 15px;")
            return

        min_block = self.slider_min_block.value()
        tolerance = float(self.slider_tolerance.value())

        try:
            res = compare_images(
                self.path_a,
                self.path_b,
                min_block_size=min_block,
                tolerance=tolerance,
            )

            sim = res.similarity_percentage
            color = "#4ade80" if sim >= 90.0 else ("#fbbf24" if sim >= 70.0 else "#ef4444")
            self.result_lbl.setText(
                f"Similarity: {sim:.2f}%  |  Leaves: {res.leaf_count}  |  Depth: {res.max_depth}"
            )
            self.result_lbl.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: bold;")

            heatmap_img = render_heatmap(res)
            self.card_diff.set_image(heatmap_img)

        except Exception as err:
            self.result_lbl.setText(f"Error: {err}")
            self.result_lbl.setStyleSheet("color: #f87171; font-size: 15px;")


def run() -> None:
    app = QApplication(sys.argv)
    window = ImageDiffApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
