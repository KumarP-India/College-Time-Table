# College Time Table

This is a simple terminal app that reads a dataset of tasks sorted by priority, based on mood and the available time. The logic is that I've included all possible work I can do, sorted them by priority, and grouped them according to how many hours I should spend or they require. The app displays them in order, so I don't have to remember everything.

### How to Install

Clone the repository:

```bash
git clone https://github.com/KumarP-India/College-Time-Table.git
cd College-Time-Table
```

Install the required libraries:

```bash
pip install rich InquirerPy
```

### How to Run

Although you could create a bash or batch file and make it executable, for this app, simply running the Python file is better.

Navigate to the directory in the terminal and run it using your Python interpreter:

```bash
python main.py
```

## About My Dataset

All the events in the dataset are related to different areas of college life. You can view the diagram I created during this process here: [https://github.com/user-attachments/files/16881521/Time.Table.pdf]

The next step was to merge and group the tasks based on the hours needed. This was the result. Terminology: `0` means that when these tasks are available, they take precedence over everything else. `1` and `2` correspond to tasks requiring 1 and 2 hours, while `3` refers to tasks needing 3 or 4 hours. The maximum duration was 4 hours. You can see the file here: [https://github.com/user-attachments/files/16881539/Time.Table.-.Hour.pdf]

Finally, I needed to merge tasks across smaller durations. For example, if I have 3 hours available, I should be able to do tasks that take 1, 2, or 3 hours. If I strictly assign 1-hour tasks only for 1-hour slots then it would be unfair to have more time as it would make them not considered. Here’s the final result, which directly reflects what's in the [Dataset.json](Dataset.json). When I can't run this program, I refer to this PDF: [https://github.com/user-attachments/files/16881607/Time.Table.-.Hour.events.pdf]

