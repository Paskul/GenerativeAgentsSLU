# GenerativeAgents

![background](https://cdn.discordapp.com/attachments/272520065176567809/1370799728736075878/background.png?ex=6820d03b&is=681f7ebb&hm=733c85703ec935b5c79b75697036c430487f19ac7481b069768f67f733ab82e1&)

Made for SLU CSCI 3300 - Software Engineering. Built around ideas from Joon Sung Park's initial [Generative Agents paper](https://arxiv.org/abs/2304.03442). We have a twist of adding an "overseer" functionality, and create agent pathfinding decisions through the LLM black box without any shortest path calculation.

## before running, you must ensure an OPENAI_API_KEY is set in a .env file in your cloned directory, AND custom font is installed

Current required commands for package installs. This also assumes you are running on an Anaconda interpreter of Python (to deal with other required packages):
```
pip install openai
pip install python-dotenv
```

Required font download, navigate to:
```
...\assets\fonts\Pixellari.ttf
```
Then run that .ttf file, all it does is install the Pixellari font locally on your computer so the OS (and tinker) recognizes it as a font to use in Python.

To run, make the .env (for devs, found in our Google Drive!!), and then move to the terminal to the directory of the parent folder to GenerativeAgents (ie, parentFolder/GenerativeAgents). For non-devs, examples of how to do this can be found [here](https://learn.griptape.ai/latest/setup/02_openai/)

Then for running, make sure you are in the directory of the parent folder, as an example of
```
C:\Users\pascal\parentFolder
```
NOT
```
C:\Users\pascal\parentFolder\GenerativeAgents
```

Then run this code to start the program:
```
python -m GenerativeAgents.ui.initial_screen
```
