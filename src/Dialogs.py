from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QProgressDialog


class Dialogs:
    @staticmethod
    def encoding_finished_dialog():
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Encoding Finished")
        msgBox.setText("Encoding process has finished.")
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    @staticmethod
    def open_file_dialog(title: str):
        selected_file, _ = QFileDialog.getOpenFileName(
            None, title, "", "Video Files (*.mp4 *.avi *.mkv)"
        )
        return selected_file
    
    @staticmethod
    def select_directory_dialog():
        options = QFileDialog.Option.ShowDirsOnly
        selected_dir = QFileDialog.getExistingDirectory(
            None, "Select Image Directory", "", options=options
        )
        
        return selected_dir

    @staticmethod
    def overwrite_dialog(window: QMainWindow):
        reply = QMessageBox.question(
            window,
            "Images Exist",
            "Images already exist. Do you want to overwrite?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes

    @staticmethod
    def insufficient_memory_dialog(required_gb: float, available_gb: float) -> None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Insufficient Memory")
        msg_box.setText(
            f"At least {required_gb:.0f} GB of free RAM is required to start "
            f"processing, but only {available_gb:.2f} GB is currently available. "
            f"Please close other applications and try again."
        )
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    @staticmethod
    def copying_frames_dialog(window: QMainWindow) -> QProgressDialog:
        progress_dialog = QProgressDialog("Copying Frames", None, 0, 100, window)
        progress_dialog.setWindowTitle("Copying Frames")
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setCancelButton(None)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.show()
        return progress_dialog
