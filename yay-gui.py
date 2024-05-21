import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QLineEdit, QListWidget, QInputDialog

import subprocess

class YayGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Yay GUI")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for packages...")
        self.search_input.returnPressed.connect(self.search_packages)
        layout.addWidget(self.search_input)

        self.package_list = QListWidget()
        layout.addWidget(self.package_list)

        self.output_label = QLabel("Output:")
        layout.addWidget(self.output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.install_button = QPushButton("Install")
        self.install_button.clicked.connect(self.install_package)
        layout.addWidget(self.install_button)

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_package)
        layout.addWidget(self.remove_button)

    def search_packages(self):
        search_term = self.search_input.text()
        self.package_list.clear()
        try:
            output = subprocess.check_output(f"yay -Ss {search_term}", shell=True, universal_newlines=True)
            packages = output.split("\n")[5:-2]  # Skip header and footer lines
            self.package_list.addItems(packages)
        except subprocess.CalledProcessError as e:
            self.output_text.setPlainText(f"Error: {e.output}")

    def install_package(self):
        selected_packages = [item.text() for item in self.package_list.selectedItems()]
        if selected_packages:
            package_names = " ".join(selected_packages)
            package_names = package_names.split(" ")[0]
            #print(package_names)
            self.run_yay_command(f"yay -S {package_names}", "Installation completed.")

    def remove_package(self):
        package_name, ok = QInputDialog.getText(self, "Remove Package", "Enter package name:")
        if ok:
            self.run_yay_command(f"yay -R {package_name}", "Removal completed.")

    def run_yay_command(self, command, success_message):
        try:
            output = subprocess.check_output(command, shell=True, universal_newlines=True)
            self.output_text.setPlainText(output + "\n" + success_message)
        except subprocess.CalledProcessError as e:
            self.output_text.setPlainText(f"Error: {e.output}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    yay_gui = YayGUI()
    yay_gui.show()
    sys.exit(app.exec_())
