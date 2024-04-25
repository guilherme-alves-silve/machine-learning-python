# Deep Reinforcement Learning

## Deep Reinforcement Learning with Tensorflow 2.1.0 and Keras-RL2

The Keras-RL2 works with just the Tensorflow 2.1.0, that works with Python 3.7, so, to continue the study of the [course](https://www.udemy.com/course/practical-ai-with-python-and-reinforcement-learning/), follow the steps below:

- Install [miniconda3](https://docs.anaconda.com/free/miniconda/index.html)
- conda create --name myenv python=3.7
- conda activate myenv
- conda install tensorflow==2.1.0 
- pip install gym[classic_control]==0.17.3 matplotlib numpy keras-rl2
- python -m notebook
- Access in your browser the link: http://localhost:8888

### Install custom environment SnakeEnv

- pip install -e gymsnake

## Deep Reinforcement Learning with PyTorch or [Tensorflow](https://www.tensorflow.org/install/pip?hl=pt-br#windows-native) on the GPU

This setup you can use to work with the Mario RL based on the [course](https://www.youtube.com/watch?v=_gmQZToTMac) too.

- Install [miniconda3](https://docs.anaconda.com/free/miniconda/index.html)
- conda create -n rflr_gpu python=3.8
- conda activate rflr_gpu
- conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
- pip install gym-super-mario-bros gym[other]
- pip install torch torchvision torchaudio tensordict torchrl --index-url https://download.pytorch.org/whl/cu118
- python -m pip install "tensorflow<2.11"
- python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
- python -m pip install notebook
