import fnmatch
import os
import sys
from multiprocessing import cpu_count
from PyQt6 import QtWidgets
from PyQt6.QtCore import QCoreApplication, QProcess, QEvent, pyqtSlot
from PyQt6.QtWidgets import QApplication, QSpinBox
from PyQt6.QtGui import QGuiApplication
from PyQt6 import uic
from Copy_Images import Copy_Images
from Dialogs import Dialogs
from Gui_Values import Gui_Values
from Image import Image
from Png_To_Video import Png_To_Video
from Scratch_Remover import Scratch_Remover
from Settings import Settings
from Ssim import Ssim
from Video_To_Png import Video_To_Png

IDENTICAL = 1.0
GUI_CONTROLS_HEIGHT = 200
MINIMUM_IMAGE_SIZE = 14

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = f"{self.current_dir}/FrameByFrame.ui"
        self.current_dir = os.path.dirname(self.current_dir)
        uic.loadUi(ui_file_path, self)
        self.png_to_video = Png_To_Video()
        self.copy_images = Copy_Images()
        self.dialogs = Dialogs()
        self.scratch_remover = Scratch_Remover()
        self.gui_values = Gui_Values()
        self.settings = Settings(self.current_dir)
        self.ssim = Ssim()
        self.video_to_png = Video_To_Png()
        self.editing_image = Image(self.left_image_frame, self.left_image_label)
        self.previous_image = Image(self.right_image_frame, self.right_image_label)
        self.next_image = Image(self.right_image_frame, self.right_image_label)
        self.init_ui()
        self.connect_signals()
        self.show()

    def init_ui(self) -> None:
        self.loading_image = False
        self.slider = False
        self.image_dir = None
        self.image_counter = 1
        self.total_images = 1
        self.copy_from_image = 0
        self.copy_to_image = 0
        self.scanning = False
        self.converting = False
        self.ignore_spinbox_signals = False
        self.enable_enhancement = False
        self.subprocess_proc = None
        self.window_border = 10
        self.desktop = QGuiApplication.primaryScreen().geometry()
        self.screen_width = self.desktop.width() - self.window_border
        self.screen_height = self.desktop.height() - self.window_border
        self.threads_spinbox.setMaximum(cpu_count())
        self.enable_buttons_list = [
            self.enhancement_checkbox,
            self.white_balance_checkbox,
            self.contrast_spinbox,
            self.brightness_spinbox,
            self.phi_spinbox,
            self.theta_spinbox,
            self.compress_spinbox,
            self.previous,
            self.image_slider,
            self.remove_scratch,
            self.action_convert_from_video,
            self.action_convert_to_video,
            self.preset_combo_box,
            self.chroma_combo_box,
            self.crf_spinbox,
            self.threads_spinbox,
            self.scaling_combo_box,
            self.action_image_directory,
            self.crop_top_spinbox,
            self.crop_bottom_spinbox,
            self.crop_left_spinbox,
            self.crop_right_spinbox,
            self.action_quit,
            self.action_image_directory,
        ]
        self.disable_buttons_list = [
            self.previous,
            self.copy,
            self.undo_copy,
            self.next,
            self.image_slider,
            self.copy_from,
            self.copy_to,
            self.remove_scratch,
            self.scan,
            self.contrast_spinbox,
            self.brightness_spinbox,
            self.phi_spinbox,
            self.theta_spinbox,
            self.compress_spinbox,
            self.enhancement_checkbox,
            self.white_balance_checkbox,
            self.action_convert_from_video,
            self.action_convert_to_video,
            self.preset_combo_box,
            self.chroma_combo_box,
            self.crf_spinbox,
            self.threads_spinbox,
            self.scaling_combo_box,
            self.crop_top_spinbox,
            self.crop_bottom_spinbox,
            self.crop_left_spinbox,
            self.crop_right_spinbox,
        ]
        self.spinbox_values = {
            self.contrast_spinbox: "alpha",
            self.brightness_spinbox: "beta",
            self.phi_spinbox: "phi",
            self.theta_spinbox: "theta",
            self.compress_spinbox: "compress",
            self.crop_top_spinbox: "top",
            self.crop_bottom_spinbox: "bottom",
            self.crop_left_spinbox: "left",
            self.crop_right_spinbox: "right",
        }

    def connect_signals(self) -> None:
        self.png_to_video.finished_signal.connect(self.encoding_finished)
        self.image_slider.valueChanged.connect(self.slider_value_change)
        self.image_slider.sliderReleased.connect(self.slider_released)
        self.action_image_directory.triggered.connect(self.select_images_dir)
        self.action_convert_from_video.triggered.connect(self.select_video)
        self.action_convert_to_video.triggered.connect(self.convert_png_to_video)
        self.action_quit.triggered.connect(self.quit_application)
        self.contrast_spinbox.valueChanged.connect(self.spinbox_changed)
        self.brightness_spinbox.valueChanged.connect(self.spinbox_changed)
        self.phi_spinbox.valueChanged.connect(self.spinbox_changed)
        self.theta_spinbox.valueChanged.connect(self.spinbox_changed)
        self.compress_spinbox.valueChanged.connect(self.spinbox_changed)
        self.white_balance_checkbox.stateChanged.connect(self.white_balance_clicked)
        self.png_to_video.progress_signal.connect(self.update_progress_bar)
        self.video_to_png.progress_signal.connect(self.update_progress_bar)
        self.next.clicked.connect(self.load_next_image)
        self.previous.clicked.connect(self.previous_pressed)
        self.copy.clicked.connect(self.copy_pressed)
        self.copy_from.clicked.connect(self.copy_from_pressed)
        self.copy_to.clicked.connect(self.copy_to_pressed)
        self.undo_copy.clicked.connect(self.undo_pressed)
        self.remove_scratch.clicked.connect(self.remove_scratch_pressed)
        self.scan.clicked.connect(self.scan_images)
        self.enhancement_checkbox.stateChanged.connect(
            self.enhancement_checkbox_clicked
        )
        self.crop_top_spinbox.valueChanged.connect(
            lambda value: self.crop_spinbox(
                self.crop_top_spinbox,
                self.crop_bottom_spinbox,
                self.editing_image.picture.shape[0],
            )
        )
        self.crop_bottom_spinbox.valueChanged.connect(
            lambda value: self.crop_spinbox(
                self.crop_bottom_spinbox,
                self.crop_top_spinbox,
                self.editing_image.picture.shape[0],
            )
        )
        self.crop_left_spinbox.valueChanged.connect(
            lambda value: self.crop_spinbox(
                self.crop_left_spinbox,
                self.crop_right_spinbox,
                self.editing_image.picture.shape[1],
            )
        )
        self.crop_right_spinbox.valueChanged.connect(
            lambda value: self.crop_spinbox(
                self.crop_right_spinbox,
                self.crop_left_spinbox,
                self.editing_image.picture.shape[1],
            )
        )

    def pass_widget_values_to_class(self) -> None:
        self.gui_values.alpha = self.contrast_spinbox.value()
        self.gui_values.beta = self.brightness_spinbox.value()
        self.gui_values.chroma = self.chroma_combo_box.currentText()
        self.gui_values.compress = self.compress_spinbox.value()
        self.gui_values.crf = str(self.crf_spinbox.value())
        self.gui_values.crop_bottom = self.crop_bottom_spinbox.value()
        self.gui_values.crop_left = self.crop_left_spinbox.value()
        self.gui_values.crop_right = self.crop_right_spinbox.value()
        self.gui_values.crop_top = self.crop_top_spinbox.value()
        self.gui_values.phi = self.phi_spinbox.value()
        self.gui_values.preset = self.preset_combo_box.currentText()
        self.gui_values.scaling = self.scaling_combo_box.currentText()
        self.gui_values.ssim_threshold = self.ssim_threshold.value()
        self.gui_values.theta = self.theta_spinbox.value()
        self.gui_values.chroma_index = self.chroma_combo_box.currentIndex()
        self.gui_values.preset_index = self.preset_combo_box.currentIndex()
        self.gui_values.scaling_index = self.scaling_combo_box.currentIndex()
        self.gui_values.white_balance = self.white_balance_checkbox.isChecked()
        self.gui_values.enable_enhancement = self.enhancement_checkbox.isChecked()
        self.gui_values.threads = self.threads_spinbox.value()

    def receive_widget_values_from_class(self) -> None:
        self.contrast_spinbox.setValue(self.gui_values.alpha)
        self.brightness_spinbox.setValue(self.gui_values.beta)
        self.compress_spinbox.setValue(self.gui_values.compress)
        self.crf_spinbox.setValue(int(self.gui_values.crf))
        self.crop_bottom_spinbox.setValue(self.gui_values.crop_bottom)
        self.crop_left_spinbox.setValue(self.gui_values.crop_left)
        self.crop_right_spinbox.setValue(self.gui_values.crop_right)
        self.crop_top_spinbox.setValue(self.gui_values.crop_top)
        self.phi_spinbox.setValue(self.gui_values.phi)
        self.ssim_threshold.setValue(self.gui_values.ssim_threshold)
        self.theta_spinbox.setValue(self.gui_values.theta)
        self.preset_combo_box.setCurrentIndex(self.gui_values.preset_index)
        self.chroma_combo_box.setCurrentIndex(self.gui_values.chroma_index)
        self.scaling_combo_box.setCurrentIndex(self.gui_values.scaling_index)
        self.white_balance_checkbox.setChecked(self.gui_values.white_balance)
        self.enhancement_checkbox.setChecked(self.gui_values.enable_enhancement)
        self.threads_spinbox.setValue(self.gui_values.threads)

    def load_settings(self) -> None:
        self.ignore_spinbox_signals = True
        self.gui_values = self.settings.load(self.gui_values)
        self.receive_widget_values_from_class()
        self.ssim.load(self.image_dir, self.total_images)
        self.ignore_spinbox_signals = False

    def save_settings(self) -> None:
        self.pass_widget_values_to_class()
        self.settings.save(self.gui_values)
        self.ssim.save(self.image_dir)

    pyqtSlot(int)

    def update_progress_bar(self, percentage: int) -> None:
        if percentage > self.previous_percentage:
            self.previous_percentage = percentage
            self.progress_bar.setValue(percentage)

    pyqtSlot()

    def encoding_finished(self) -> None:
        self.converting = False
        self.progress_bar.setValue(0)
        self.enable_buttons()

    def convert_png_to_video(self) -> None:
        self.pass_widget_values_to_class()
        self.converting = True
        self.previous_percentage = 0
        self.disable_buttons()
        if not self.png_to_video.convert_png_to_video(
            self.gui_values,
            self.dialogs,
            self.image_dir,
            self.current_dir,
            self.total_images,
            self.ssim,
            self,
        ):
            self.converting = False
            self.enable_buttons()

    def crop_spinbox(
        self, spinbox1: QSpinBox, spinbox2: QSpinBox, dimension: int
    ) -> None:
        if not self.ignore_spinbox_signals:
            if dimension - spinbox1.value() - spinbox2.value() > MINIMUM_IMAGE_SIZE:
                self.ssim.set(self.image_counter, 0)
            else:
                self.ignore_spinbox_signals = True
                spinbox1.setValue(spinbox1.value() - 1)
                self.ignore_spinbox_signals = False

            self.load_images()

    def spinbox_changed(self) -> None:
        if not self.ignore_spinbox_signals:
            self.load_images()
            self.ssim.set(self.image_counter, 0)

    def update_ssim(self) -> None:
        if not self.slider:
            current_ssim = self.ssim.calculate(
                self.image_counter,
                self.editing_image.picture,
                self.next_image.picture,
            )
            self.ssim.set(self.image_counter, current_ssim)
            self.current_ssim_value.setText(f"{current_ssim:.4f}")

        self.slider = False

    def enhance_image(self, image: Image, image_number: int) -> None:
        image.crop(self.gui_values)

        if self.enable_enhancement:
            image.colour_enhance(self.gui_values)

        if self.gui_values.white_balance:
            image.white_balance()

        image.display()
        image.display_image_number(image_number)

    def remove_scratch_pressed(self) -> None:
        self.editing_image.load(self.image_counter, self.image_dir)
        self.next_image.load(self.image_counter + 1, self.image_dir)
        # If we are on the first frame, we cannot copy from the previous frame
        if self.image_counter > 2:
            self.previous_image.load(self.image_counter - 1, self.image_dir)
        else:
            self.previous_image.load(self.image_counter, self.image_dir)

        if self.scratch_remover.edit_image(
            self.editing_image.picture,
            self.previous_image.picture,
            self.next_image.picture,
            QGuiApplication.primaryScreen().size(),
        ):
            file_path_to_copy_from = f"{self.image_dir}{self.image_counter:06d}.png"
            self.copy_images.backup_image(file_path_to_copy_from, self.backup_dir)
            self.editing_image.save(self.image_counter, self.image_dir)
            self.ssim.set(self.image_counter, 0)

        self.load_images()
        self.update_ssim()
        self.enable_buttons()

    def copy_pressed(self) -> None:
        self.copy_from_image = 0

        self.copy_images.copy_images(
            self.image_counter,
            self.image_dir,
            self.backup_dir,
            self.copy_from_image,
            self.copy_to_image,
            self.ssim,
        )

        if self.image_counter < self.total_images:
            self.image_counter += 1

        self.copy_from_image = 0
        self.load_images()
        self.enable_buttons()

    def copy_from_pressed(self) -> None:
        self.copy_from_image = self.image_counter
        self.copy_to.setEnabled(True)

    def copy_to_pressed(self) -> None:
        self.copy_to_image = self.image_counter
        self.disable_buttons()
        self.copy_images.copy_images(
            self.image_counter,
            self.image_dir,
            self.backup_dir,
            self.copy_from_image,
            self.copy_to_image,
            self.ssim,
        )
        self.image_counter = self.copy_to_image
        self.copy_from_image = 0
        self.copy_to_image = 0
        self.load_images()
        self.enable_buttons()

    def previous_pressed(self) -> None:
        self.load_previous_image()
        self.enable_buttons()

    def undo_pressed(self) -> None:
        self.copy_images.undo(self.image_counter, self.image_dir, self.backup_dir)
        self.undo_copy.setEnabled(self.enable_undo())
        self.ssim.set(self.image_counter - 1, 0)
        self.load_images()

    def enable_undo(self) -> bool:
        backup_filename = f"{self.backup_dir}{self.image_counter:06d}_001.png"

        return os.path.isfile(backup_filename)

    def enhancement_checkbox_clicked(self) -> None:
        self.enable_enhancement = self.enhancement_checkbox.isChecked()
        self.load_images()

    def white_balance_clicked(self) -> None:
        self.load_images()

    def resize_window(self) -> None:
        self.move(0, 0)
        self.adjustSize()
        self.resize(self.screen_width, self.height() + GUI_CONTROLS_HEIGHT)

    def select_video(self) -> None:
        selected_file = self.dialogs.open_file_dialog("Select Video File")
        if selected_file:
            self.disable_buttons()
            self.pass_widget_values_to_class()
            self.converting = True
            self.previous_percentage = 0
            self.total_images = self.video_to_png.convert_video_to_png(
                self.image_dir, self, selected_file
            )
            self.ssim.clear_values(self.total_images)
            self.image_slider.setMaximum(self.total_images - 1)
            self.image_counter = 1
            self.converting = False
            self.progress_bar.setValue(0)
            self.image_slider.setValue(1)
            self.load_images()
            self.resize_window()
            self.enable_buttons()

    def select_images_dir(self) -> None:
        selected_dir = self.dialogs.select_directory_dialog()
        if selected_dir:
            self.backup_dir = f"{selected_dir}/backup/"
            self.image_dir = f"{selected_dir}/"
            os.makedirs(self.backup_dir, exist_ok=True)
            self.load_settings()

            self.total_images = (
                len(fnmatch.filter(os.listdir(self.image_dir), "*.png")) - 1
            )
            if self.total_images > 1:
                if not self.ssim.load(self.image_dir, self.total_images):
                    self.ssim.clear_values(self.total_images)

                self.load_images()
                self.image_slider.setMaximum(self.total_images)
                self.action_convert_to_video.setEnabled(True)
                self.enable_buttons()

            self.action_convert_from_video.setEnabled(True)

            self.resize_window()

    def disable_buttons(self) -> None:
        for button in self.disable_buttons_list:
            button.setEnabled(False)

        if self.scanning:
            self.action_quit.setEnabled(False)
            self.action_image_directory.setEnabled(False)

        if self.converting:
            self.action_image_directory.setEnabled(False)

    def enable_buttons(self) -> None:
        self.scan.setEnabled(self.image_counter < self.total_images)

        if not self.scanning and not self.converting:
            for button in self.enable_buttons_list:
                button.setEnabled(not self.scanning and not self.converting)

            self.copy_to.setEnabled(self.copy_from_image > 0)
            self.next.setEnabled(self.image_counter < self.total_images)
            self.copy.setEnabled(
                bool(
                    self.image_counter < self.total_images + 1
                )
            )
            self.copy_from.setEnabled(self.total_images > 1)
            self.undo_copy.setEnabled(self.enable_undo())

    def load_images(self) -> None:
        if self.total_images > 1 and not self.ignore_spinbox_signals:
            self.pass_widget_values_to_class()
            self.editing_image.load(self.image_counter, self.image_dir)
            self.next_image.load(self.image_counter + 1, self.image_dir)
            self.enhance_image(self.editing_image, self.image_counter)
            self.enhance_image(self.next_image, self.image_counter + 1)
            self.update_ssim()
            QCoreApplication.processEvents()

    def stop_scanning(self):
        self.scanning = False
        self.load_images()
        self.enable_buttons()

    def scan_images(self) -> None:
        if self.scanning:
            self.stop_scanning()
        else:
            self.scanning = True
            self.disable_buttons()

        while (
            self.scanning
            and self.image_counter < self.total_images
            and (
                self.ssim.get(self.image_counter) < self.ssim_threshold.value()
                or self.ssim.get(self.image_counter) == IDENTICAL
            )
        ):
            self.load_next_image()

        self.stop_scanning()

    def update_image_counter(self, delta: int) -> None:
        self.loading_image = True
        self.image_counter += delta
        self.load_images()
        self.image_slider.setValue(self.image_counter)
        self.loading_image = False

    def load_next_image(self) -> None:
        if self.image_counter < self.total_images and not self.loading_image:
            self.update_image_counter(1)

    def load_previous_image(self) -> None:
        if self.image_counter > 1 and not self.scanning and not self.loading_image:
            self.update_image_counter(-1)

    def slider_value_change(self, value: int) -> None:
        self.image_counter = value
        self.slider = True
        self.enable_buttons()
        self.load_images()

    def slider_released(self) -> None:
        self.image_counter = self.image_slider.value()
        self.load_images()
        self.enable_buttons()

    def closing_down(self) -> None:
        if self.image_dir != None:
            self.save_settings()
            self.ssim.save(self.image_dir)

        if self.subprocess_proc is not None:
            if self.subprocess_proc.state() == QProcess.Running:
                self.subprocess_proc.terminate()
                self.subprocess_proc.wait_for_finished()

    def quit_application(self):
        self.closing_down()
        QApplication.instance().quit()

    def event(self, event):
        if event.type() == QEvent.Type.Close:
            self.closing_down()
            event.accept()

        return super().event(event)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Create QApplication instance
    ui = Ui()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

