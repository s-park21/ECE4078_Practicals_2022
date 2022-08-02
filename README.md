# ECE4078_Practicals_2022 [<img align="right" src="https://deepnote.com/buttons/launch-in-deepnote-white.svg">](https://deepnote.com/workspace/ece4078-7216-bdf57084-6c08-4dea-a555-1d8b5ffa5d2c/project/ECE4078-Practicals-e09a2c46-66e4-4822-9f63-abca8470f17c/%2FECE4078_Practicals_2022%2FWeek01%2FPractical01_PositionAndOrientation.ipynb)
Repository for practicals of unit ECE4078 (Intelligent Robotics) offered in 2022.

# Quick start

To launch this repo in Deepnote and run:
- Click the "Launch with Deepnote" badge in this README.
- Press Duplicate button (If you don't have an account, create one).
- Once it is in your workspace, you can start playing with the notebook.

To do you home work:
- Work on the notebook with `_exercise.ipynb` suffix
- Download it locally to your machine
- Submit the file to Moodle before deadline.

A visual guide is included in this [video](https://youtu.be/zA7RqTRkFPA).

# Homework

### Grading Test Cases

At the end of each notebook with `_exercise` suffix (which is your homework), I already included the a few test cases along with point allocations that we are going to use to grade you (at the end of the notebook). Note that we **may** test against additional test cases when I actually grade your notebook, so passing all the test cases will not guarantee obtaining the points but does increase your chance by a lot.

We use result-based **auto-grading** so there will be no partial mark for your solution!

### Submission

There is only one `_exercise` notebook per week folder, please download that file to your local machine when you feel good about your homework's solution, and submit that to Moodle. 

NOTE: if there are 2 `.ipynb` in your Moodle submission box, you will receive 0. Only submit ONE `.ipynb` file to Moodle and any extra file that is relevant (there will be weeks where we require you to submit your notebook along with other files, such as `.pt` for the weight of neural network). 

# What to do when new content is released

For now, the Deepnote project is linked to the Github repo. There are two ways you can go about getting the new content.

### The messy way

You can click on the badge to get the updated Deepnote Project and click the "Duplicate button" again. The reason why this is messy is you will end up a lot of instances of the project in your Deepnote workspace. 

### The clean way

Use `git`! And hope that the `pull` does not create any conflicts (you can open terminal in Deepnote)! 

If you do not worry about progress, you can always `git stash` and `git pull`

If you do worry about progress, you can:
- Download the notebook you are working on, `git stash` and `git pull` and then copy relevant part from your solution back to the notebook. 
- Fancy things you can do with `merge` and `branch`
- If you find a better system to update content every week and save your progress without having to do complicated merging (to accommodate students with no `git` background, OR using text editor in terminal), please share that with the class! (Or better yet, write a script for that).

### The best way

There will be a better solution that is yet to come (it is a good combination of the messy way and the clean way) because the feature is still a work in progress from Deepnote, it is expected to arrive in late August. In the meantime, use "The messy way" if you don't know how to `git` and use `git` at your own risk. 

# Running the notebook on your local machine

For those of you who don't want to run things on the cloud, feel free to clone this repo and run it locally. Note that this is for people who is already familiar with `jupyter` and `docker`. Feel free to notify me if you experience bugs, support for this is limited though, if I cannot reproduce the error on my end, I will advise you to fix it yourself, or run your notebook on the cloud. 

### Running with `jupyter`

The repo includes `dependencies.txt` that lists all the dependencies (I didn't use `requirements.txt` because Deepnote will actually try to install stuff inside `requirements.txt` which is redundant).

Sometimes the `ipywidgets` will not work properly out of the box, you have to look online yourself on how to enable that in your `jupyter notebook` or `jupyter lab` (It is pretty straightforward).

### Running on docker

The image is public, you can pull it with

```
docker pull tinsirius/ece4078_prac:ubuntu
```
When you launch `docker`, make sure:
- Mount this repo to the container 
- Open port `8080` and a few port immediately after that, such as `8080-8100` for the visualizer. 
- Also, you have to open some ports for your `jupyter` interface too.

Step 2 and 3 can just be replaced with `--net=host` argument if you want to do that.

# Local set up on Windows
There are 3 pieces of software you have to install:
- Docker Desktop
- VSCode (with extensions: Docker and remote-container)
- Git 

## Installing Docker Desktop

### Installing WSL2
As a prerequisite, you have to WSL2 installed, if you are not sure you already installed it, please follow [this guide](https://docs.microsoft.com/en-us/windows/wsl/install-manual) Up to Step 5.  If you encounter any problem, please consult their [troubleshooting website](https://docs.microsoft.com/en-us/windows/wsl/troubleshooting#installation-issues), especially the part about enabling virtualization in your BIOS.

[This](https://youtu.be/cgXZ8Ecrdg0) is a video of my attempt.

### Installing Docker Desktop
If you already have WSL2 installed, consult this [webpage](https://docs.docker.com/desktop/install/windows-install/) for installation (if you do not satisfy the requirement from their website, please use Deepnote). It should be very straightforward, download the `.exe` file and install. 

[This](https://youtu.be/HbMPZl0Hd90) is a video of my attempt

## Installing VScode

[Download](https://code.visualstudio.com/download) VSCode installer to your machine and install it. Open it and install the extensions: 
- Docker
- remote-container

[This](https://youtu.be/AIyzgDLA3RI) is a video of my attempt.

## Putting Docker Desktop and VSCode together

- Run this command in command prompt or powershell (please remember to specify the path to your ECE4078 folder where you have the copy of the repo) `docker run -t -p 8080-8180:8080-8180 -p 8888-8900:8888-8900 -v <PLEASE SPECIFY YOUR PATH HERE>:/root tinsirius/ece4078_prac:ubuntu`
- Attach to VSCode
- Install Jupyter and Python extension on the Docker container
- Get cracking

[This](https://youtu.be/jcNg8gg-19Y) is a video of my attempt.

## How to get new content

Use git or just Download Zip file from Github.

# Local set up on MacOS

Credit to one of our instructor [@Juxi](https://github.com/Juxi) for this instruction. 

If you are on a Apple notebook the steps are slightly different to the videos in the Readme

The easiest way to run the examples and develop your code is by using 
- Git 
- Docker Desktop
- VSCode (with extensions: Docker and remote-container)


## Git: Get the code base

The easiest way to  get the code is to check out the repository with Git. You can either use the GitHub Desktop application or the git command line tool to clone the repository. You can download the application here: https://desktop.github.com/

If you use Git in the terminal, run:

`git clone https://github.com/tinsirius/ECE4078_Practicals_2022.git` 

to create the *ECE4078_Practicals_2022* folder in your local directory.

NB: Remember to `git pull` the repository every week to get the new weekly code examples for the class and practical.


## Installing Docker Desktop
Download and install [Docker Desktop from here https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/).

NB: Chose the correct chip architecture for your notebook - with newer Macs having the Apple Silicon (~575MB download)

Follow the instructions there to install Docker or use the command line:

`sudo hdiutil attach Docker.dmg`

`sudo /Volumes/Docker/Docker.app/Contents/MacOS/install`

`sudo hdiutil detach /Volumes/Docker`

### Pull the ECE4078 ubuntu image
In the Terminal you can get the docker image provided by running

`docker pull tinsirius/ece4078_prac:ubuntu`

After completing the download, the image should then show up in your Docker Dashboard (you can access it by clicking on the whale in the menu bar).


## Installing Visual Studio Code (the IDE)
Final step is to download VS Code [from here: https://code.visualstudio.com/docs?dv=osx](https://code.visualstudio.com/docs?dv=osx) (About a ~300mb download).

Install the application by dragging it from the DMG into the Application folder.

You should then install the `docker` and `remote containers` extensions into VSCode by clicking "View -> Extensions" to search and install thes two.



## Running the Code

Same as with the windows install, you need to (once) link the code repository to the docker image by running:

`docker run -t -p 8080-8180:8080-8180 -p 8888-8900:8888-8900 -v <PLEASE SPECIFY YOUR PATH HERE>:/root tinsirius/ece4078_prac:ubuntu`

Once that has been completed you can attach your VSCode to the running docker container like described in [Tin's video](https://youtu.be/jcNg8gg-19Y).






