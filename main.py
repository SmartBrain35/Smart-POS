from PySide6.QtWidgets import QApplication
from controllers.login import LoginController

def main():
    app = QApplication([])

    controller = LoginController()
    controller.login_view.show()  

    app.exec()
    
if __name__ == "__main__":
    main()
