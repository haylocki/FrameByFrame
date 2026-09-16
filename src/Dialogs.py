from PyQt6.QtWidgets import QFileDialog, QMessageBox, QMainWindow


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
