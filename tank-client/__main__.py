import signal
import sys

from .config import AppConfig

from .app import App

if __name__ == "__main__":
    app = App(AppConfig(AppConfig.parse_args()))

    # Shut down the scheduler when exiting the app
    # atexit.register(stop_application)
    def signal_handler(sig, frame):
        print('You pressed Ctrl+C!', sig, frame)
        app.stop()
        print("Application stopped")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    app.start()
