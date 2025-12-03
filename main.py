from gui.login_screen import LoginScreen
from gui.dashboard import Dashboard

def main():
    login_screen = LoginScreen()
    key = login_screen.run() 

    if key is None:
        print("Login or setup cancelled. Exiting...")
        return

    Dashboard(key)


if __name__ == "__main__":
    main()
