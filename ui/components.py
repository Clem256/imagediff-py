from typing import Callable, Optional

from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class ImageCard(QFrame):
    """Reusable card widget showing an image preview and an optional browse button."""

    def __init__(
            self,
            title: str,
            on_browse: Optional[Callable[[], None]] = None,
            preview_size: tuple[int, int] = (280, 180),
            parent=None,
    ):
        super().__init__(parent)
        self.preview_size = preview_size

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet( """ ImageCard {  background-color: #2b2b2b; border: 1px solid #3d3d3d; border-radius: 8px;
            } QLabel { color: #e0e0e0;} """ )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header title
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(self.title_label)

        # Preview area
        self.preview_label = QLabel("Empty")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFixedSize(*preview_size)
        self.preview_label.setStyleSheet( """background-color: #1e1e1e;border-radius: 6px;color: #777777; """)
        layout.addWidget(self.preview_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Browse button or empty placeholder spacer
        if on_browse:
            self.browse_btn = QPushButton("Browse...")
            self.browse_btn.setFixedWidth(110)
            self.browse_btn.clicked.connect(on_browse)
            layout.addWidget(self.browse_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            spacer = QLabel("")
            spacer.setFixedHeight(30)
            layout.addWidget(spacer)

    def set_image(self, image_or_path: str | Image.Image) -> None:
        """Render a file path or a direct PIL.Image in the preview box."""
        if isinstance(image_or_path, str):
            pixmap = QPixmap(image_or_path)
        else:
            # Convert PIL -> QImage
            rgb_image = image_or_path.convert("RGB")
            data = rgb_image.tobytes("raw", "RGB")
            q_image = QImage( data,  rgb_image.width, rgb_image.height, rgb_image.width * 3, QImage.Format.Format_RGB888,)
            pixmap = QPixmap.fromImage(q_image)

        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.preview_size[0],
                self.preview_size[1],
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.preview_label.setPixmap(scaled_pixmap)
            self.preview_label.setText("")
        else:
            self.preview_label.setText("Invalid image")
