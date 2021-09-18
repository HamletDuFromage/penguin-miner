# penguin-miner
A Club Penguin Rewritten (CPR) mine bot. Supports parallel mining on multiple accounts

## How to use
Install the required dependencies by executing `pip install -r requirements.txt` in your terminal, then run `python penguin-miner.py` in your terminal.

## How it works
Once you select the corners of the game window, the program determines a region of interest. Your penguin then goes to a random spot in that area and mines for 10 seconds (with a random delta up to 3 seconds added or subtracted each time).

You can select multiple game windows to have multiple penguins mining.
