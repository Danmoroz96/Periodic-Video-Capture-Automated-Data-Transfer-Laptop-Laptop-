# Periodic-Video-Capture-Automated-Data-Transfer-Laptop-Laptop-
I will build an automated large-data IoT pipeline on Windows. It demonstrates how edge devices collect, send, and manage large files in a real IoT system.


# IoT Video Pipeline Lab

## Roles and Setup
* **Sender:** Laptop A (Localhost)

* **Receiver:** Laptop A (Localhost)


* **Note:** This lab was adapted to run entirely on a single laptop within VS Code. The network transfer was simulated using the internal loopback address, which perfectly mimics an edge device communicating over a network.

## Network Configuration

* **Receiver IP Address:** `127.0.0.1` (Localhost)
* **Port:** `5001`

## System Verification
* **Did the automated system work?** Yes. The system successfully recorded, buffered locally, transferred over the simulated network, and saved the files.

* **Were videos deleted only after confirmation?** Yes. The `sender.py` script waits for the `b"OK"` signal from the receiver before executing `os.remove(filepath)`. If the receiver is offline, the file remains safely buffered in the local `videos` folder.

## Problems Encountered and Fixes
**Problem:** A "Race Condition" (`[WinError 32]`). The `sender.py` script checked the folder so quickly that it attempted to grab and send the `.mp4` file while OpenCV (`recorder.py`) was still actively recording and locking the file.


**Fix:** I implemented a custom `is_file_locked()` helper function in `sender.py`. It uses `os.rename()` to check if the OS has locked the file. If locked, the sender skips the file and waits for the next loop. Once OpenCV releases the file, the sender safely grabs and transfers it.

