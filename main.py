from web_server.app import start_server


def start_process() -> None:
    """Start main process after pre-start checks."""
    print("Starting main process...")
    start_server()


if __name__ == "__main__":
    # pre_start_checks()
    start_process()
