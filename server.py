import os
import socket
import sys
import logging
import config


def run_server(filename, host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))  # binding host and port
            server_socket.listen(1)
            server_socket.settimeout(5)  # check for keyboard interrupt
            logging.info(f"Serving '{filename}' on {host}:{port}")

            while True:
                try:
                    conn, addr = server_socket.accept()  # accept connection from client
                    logging.info(f"Client connected from {addr}")
                    with conn, open(filename, "r", encoding="utf-8") as f:
                        for line in f:
                            conn.sendall(line.encode("utf-8"))  # encode and send each line of the file
                    logging.info("File transfer complete")
                except socket.timeout:
                    continue  # allows keyboard interrupt, will reconnect if no error occurs
                except BrokenPipeError:
                    logging.warning("Client disconnected unexpectedly")
                except Exception as e:
                    logging.error(f"Error during file transfer: {e}")

    except KeyboardInterrupt:
        logging.info("Server stopped by user")
        sys.exit(0)
    except OSError as e:
        logging.error(f"Socket error: {e}")


def get_params():
    # Check the command line arguments
    if len(sys.argv) != 3:
        logging.error("Incorrect command line arguments")
        sys.exit(1)

    # Check port
    try:
        port = int(sys.argv[2])
    except ValueError:
        logging.error("Port must be an integer")
        sys.exit(1)

    # Check if file exists
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        logging.error(f"File '{filename}' does not exist. Exiting.")
        sys.exit(1)

    # Load host address from configuration
    host = config.HOST

    return filename, host, port


def main():
    filename, host, port = get_params()
    run_server(filename, host, port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Client encountered an unexpected error: {e}")
        sys.exit(1)
