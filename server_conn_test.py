import os


def main():
    print("Hello from GitHub Actions!")
    host = os.environ.get("HOST")

    if not token:
        raise RuntimeError("HOST env var is not set!")
    print("Host = " + host)

    if __name__ == "__main__":
        main()
