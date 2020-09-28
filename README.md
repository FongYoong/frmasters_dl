# frmasters_dl (**Incomplete**)

* Note: The script's development is **halted** because FrontEnd Masters can somehow detect Selenium's involvement and prevent CloudFront key pairs from being distributed.

* `frmasters_dl.py` uses Selenium to log into [Frontend Masters](https://frontendmasters.com/login) with credentials stored in `session/credentials.txt` and attempt to download a video from a link specified in the `target_url` variable.

* A typical Frontend Masters' video comprises of small `.ts` chunks which must be joined together. FFMPEG is utilised by the script to achieve this. With the required CloudFront keys, a "playlist" file with the extension `.m3u8` can be retrieved and this file contains all the required metadata to obtain the `.ts` chunks.

* `session/credentials.txt` must contain the username/email in the first line and the password in the second line.

* The login cookies are pickled and stored in `session/cookies.pkl` for convenience.

***

# Installation

* Only tested on Python 3.8.1 and Windows 10. Adjustments such as changing **\\** to **/** if running on Bash etc must considered.

1. Create a virtual environment with [venv](https://docs.python.org/3/tutorial/venv.html) as follows:
```bash
virtualenv venv
```
2. Activate the environment:
```bash
venv\Scripts\activate.bat
```
3. Install dependencies:
```bash
pip install requirements.txt
```
4. Run the script for fun:
```bash
python frmasters_dl.py
```