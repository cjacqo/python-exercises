
# Excersise 1.1

This exercise walks through the basic steps of setting up python, creating/copying working environments, how to install packages and how to run python scripts in the terminal.

* **Step 1: Installing python (macOS)**

With homebrew installed, run the following commands:

`brew install && brew upgrad`

`brew install python`

If you are using Z Shell (macOS 10.15 and higher) run the following command:

`echo 'export PATH="/usr/local/opt/python/bin:$PATH"' >> ~/.zshrc`

* **Step 2: Installing virtual environments**

Virtual environments allow you to create individual, isolated directories which allow you to do "clean installs" and control what packages are used for what directory. Keeping your packages separate is useful for a number of reasons, primarily concerning compatibility.

To set up a virtual environment, first install the virtual environment package:

`pip install virtualenvwrapper`

Then, configure your terminal (still working in macOS 10.15 and higher). Before modifying, create a backup:

`sudo cp ~/.zshrc ~.zshrc-backup`

Next, you'll need to verify the location of your "virtualenvwrapper.sh" file by using the `which` command:

`which virtualenvwrapper.sh /usr/local/bin/virtualenvwrapper.sh`

Once found, you can now add it to PATH. Using the **nano** command line editor:

`sudo nano ~/.zshrc`

Scroll all the way down with your arrow keys and add the following line at the end of the document:

`export PATH="/home/<your username>/.local/bin:$PATH"`

Press **Ctrl + X** to close the file, then press **Y** and **Enter**. Close the current terminal and open another one, then retry the `which` command to locate the "virtualenvwrapper.sh" file:

`which virtualenvwrapper.sh /home/username/.local/bin/virtualenvwrapper.sh`

Finally, modify your shell startup file:

`sudo nano ~/.zshrc`

Then, add the following lines at the bottom of the file:

`export VIRTUALENVWRAPPER_PYTHON=$(which python)`

`source $(which virtualenvwrapper.sh)`

Close the editor with **Ctrl + X**, type **Y** and press **Enter**, then reload your modified shell startup file.

* **Step 3: Creating a new virtual environment**

To create a new virtual environment, run the following command, but replacing <environment name> with a name of your choice:

`mkvirtualenv <environment name>`

* **Step 4: Running your first python script**

Navigate to the directory of choice and create a python file:

`cd <directory of choice>`
`touch file.py`

Open the file in your code editor of choice and write a simple line of code to print "Hello World!"

`print("Hello World!")`

In your terminal, navigate to the directory of the file you just created, then run the following line:

`python file.py`

You should see "Hello World!" printed in your terminal.