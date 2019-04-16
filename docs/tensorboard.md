# How to use TensorBoard logger

TensorBoard logger implemented in `logger` module as `TBLogger` class.

## Prerequisites

```bash
$ pip install tensorflow tensorboard tensorboardx
```

## How to Use

Here is a basic example how to log loss values during training using already implemented method called `log_loss`.
**NOTE:** Values logged by this method cannot be exported to json for external processing.

```python
from logger import TBLogger

# specify logdir
logdir = './logs/run1'

# initialize logger
tb_logger = TBLogger(logdir)

# training loop starts here
for n_iter in range(...):

     # update global step
    tb_logger.update_global_step(1)  # increase global step by 1 (1 iteration or epoch)
    ...
    output = model(data)
    loss = loss_fn(output, gt)  # compute training loss; gt - ground truth values
    
    # to log loss value:
    tb_logger.log_loss(loss.item())  # loss.item() - float loss value

# close logger
tb_logger.close()
```

With novel `log_losses` method.

**NOTE:** Values logged by this method can be exported to json file for external processing.

```python
tb_logger = TBLogger(logdir)

for n_iter in range(...):

    # update global step
    tb_logger.update_global_step(1)  # increase global step by 1 (1 iteration or epoch)
    ...
    output = model(data)
    loss = loss_fn(output, gt)  # compute training loss; gt - ground truth values

    # log several losses
    tb_logger.log_losses({'training_loss': loss.item()})

# close logger
tb_logger.close()  # Now all the scalars logged by log_losses wil be exported to the json file
```


## How to Extend

If you want to log scalar values of smth, simply add new method to `TBLogger` class. For example, to log an accuracy:

```python
class TBLogger:
    ...
    def log_acc(self, acc, global_step):
        self.log('data/acc', acc, global_step)
```

Where, `acc` - accuracy, scalar value; `global_step` - number of epoch/iteration/batch; `'data/acc'` - tag.

**NOTE:** `TBLogger` method `log` writes only scalar value. Currently only single scalar values are supported.  

## How to Launch

```bash
$ tensorboard --logdir logs/
```

Open the following link in your browser (by default):

```bash
http://localhost:6006/
```

## More

[Tensorboard for PyTorch](https://github.com/lanpa/tensorboardX)
