import threading
from sqlalchemy.orm import sessionmaker
import logging
import sys
import config

from db import init_db, WordCount
from streaming import stream_from_server


def main():
    # initialize database
    engine = init_db(config.DB_NAME)

    # create threads (each connects to a different server)
    threads = [
        threading.Thread(target=stream_from_server, args=(host, port, engine))
        for host, port in config.SERVERS
    ]

    for t in threads:
        t.start()

    # wait until all threads finish
    for t in threads:
        t.join()

    # retrieve results - the 5 most common words
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        results = session.query(WordCount).order_by(WordCount.count.desc()).limit(5).all()
        if not results:
            logging.warning("No words were counted.")
        else:
            print("Top 5 most common words:")
            for row in results:
                print(f"{row.word}: {row.count}")
    except Exception as e:
        logging.error(f"Failed to query database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Client stopped by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Client encountered an unexpected error: {e}")
        sys.exit(1)
