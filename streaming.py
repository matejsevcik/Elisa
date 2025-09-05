import socket, codecs, re, logging
from collections import Counter
from db import flush_to_db
import config


# receive and process data from server
def stream_from_server(host, port, engine):
    decoder = codecs.getincrementaldecoder("utf-8")()
    buffer, counter, processed_bytes = "", Counter(), 0
    word_re = re.compile(r"\b\w+(?:['’]\w+)*\b")

    try:
        # Connect to server
        with socket.create_connection((host, port), timeout=config.SOCKET_TIMEOUT) as s:
            logging.info(f"Connected to {host}:{port}")
            while data := s.recv(4096):  # receive a load 4096 bytes
                # decode received bytes back to text
                buffer += decoder.decode(data)
                processed_bytes += len(data) # how much data has been processed in the current chunk

                # find if the current load of data contains unfinished words at the end
                m = re.search(r"\w+(?:['’]\w+)*$", buffer)
                # store the unfinished word in buffer - to be processed with the next load of data
                to_process, buffer = (buffer[:m.start()], buffer[m.start():]) if m else (buffer, "")

                # count words in the current load of data
                if to_process:
                    counter.update(w.lower() for w in word_re.findall(to_process))

                # if the size of data processed in the current chunk exceeds a configured value,
                # store the counter to database and reset the counter
                if processed_bytes >= config.CHUNK_SIZE:
                    flush_to_db(counter, engine)
                    processed_bytes = 0

        # store data remains at the end of file
        buffer += decoder.decode(b"", final=True)
        if buffer:
            counter.update(w.lower() for w in word_re.findall(buffer))
        if counter:
            flush_to_db(counter, engine)

        logging.info(f"Finished streaming from {host}:{port}")

    except ConnectionRefusedError:
        logging.error(f"Cannot connect to {host}:{port}")
    except socket.timeout:
        logging.error(f"Connection to {host}:{port} timed out")
    except Exception as e:
        logging.error(f"Unexpected error with {host}:{port} - {e}")
