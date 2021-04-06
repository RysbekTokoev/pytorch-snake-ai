# pytorch-snake-ai
 Reinforcement Learning implementation using PyTorch and 'Snake'

Snake game used is a modified version of this gist: <a href='https://gist.github.com/rajatdiptabiswas/bd0aaa46e975a4da5d090b801aba0611'>Snake Game. </a> \
Thanks to <a href='https://gist.github.com/rajatdiptabiswas'>rajadiptabiswas</a> for this.

# Model
Neural net with one hidden layer with ReLu activation (and one output layer).
To update the Q value was used [Bellman Equation](https://en.wikipedia.org/wiki/Bellman_equation) and Mean Squared Error (MSE) for Loss function


# Usage
Simply install all the requirements and run main.py. Example:
```angular2html
pip install -r requirements.txt
python3 main.py
```
!If any troubles with installing pytorch please check https://pytorch.org/get-started/locally/ \
To run the code with pre-trained model run main.py with a path to the model as an argument:
```
python3 main.py model/model.pth
```

# Contacts
Rysbek Tokoev \
[rysbek@tokoev.com](mailto:rysbek@tokoev.com) \
[Linkedin](https://www.linkedin.com/in/rysbek-tokoev-44197919a/) \
[Facebook](https://www.facebook.com/tokoevr/)
