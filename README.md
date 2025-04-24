# GenerativeAgents

## before running, you must ensure an OPENAI_API_KEY is set in a .env file in your cloned directory

Current required commands for package installs:
```
pip install openai
pip install python-dotenv
```

Required font download, navigate to:
```
...\assets\fonts\Pixellari.ttf
```
Then run that .ttf file, all it does is install the font locally on your computer so the OS (and tinker) recognizes it as a font to use in Python.

To run, make the .env (for devs, found in our Google Drive!!), and then move to the terminal to the directory of the parent folder to GenerativeAgents (ie, parentFolder/GenerativeAgents)

Then run this code from the parent folder,
for example being C:\Users\pascal\Desktop\code\parentFolder
NOT C:\Users\pascal\Desktop\code\parentFolder\GenerativeAgents !!

```
python -m GenerativeAgents.ui.initial_screen
```
