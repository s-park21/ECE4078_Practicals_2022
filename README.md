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
