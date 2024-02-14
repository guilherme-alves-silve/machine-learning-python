# Deep Reinforcement Learning with Tensorflow 2.1.0 and Keras-RL2

The Keras-RL2 works with just the Tensorflow 2.1.0, that works with Python 3.7, so, to continue the study of the [course](https://www.udemy.com/course/practical-ai-with-python-and-reinforcement-learning/), follow the steps below:

- Install [miniconda3](https://docs.anaconda.com/free/miniconda/index.html)
- conda create --name myenv python=3.7
- conda activate myenv
- conda install tensorflow==2.1.0 
- pip install gym[classic_control]==0.17.3 matplotlib numpy keras-rl2
- python -m notebook
- Access in your browser the link: http://localhost:8888

## Install custom environment SnakeEnv

- pip install -e gymsnake
