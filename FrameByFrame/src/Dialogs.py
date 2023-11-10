from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow


class Dialogs:
    @staticmethod
    def encoding_finished_dialog():
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Encoding Finished")
        msgBox.setText("Encoding process has finished.")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    @staticmethod
    def open_file_dialog(title: str):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        selected_file, _ = QFileDialog.getOpenFileName(
            None, title, "", "Video Files (*.mp4 *.avi *.mkv)", options=options
        )

        return selected_file

    @staticmethod
    def select_directory_dialog():
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
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
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return reply == QMessageBox.Yes
