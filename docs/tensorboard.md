# How to use TensorBoard Logger

TensorBoard logger implemented in `logger` module as `TBLogger` class.

## Prerequisites

```bash
$ pip install tensorflow tensorboard tensorboardx
```

## How to Use

### How to Log Loss

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

### How to Use `log_losses`

**NOTE:** Values logged by this method can be exported to json file for external processing.

```python
tb_logger = TBLogger(logdir)

for n_iter in range(...):

    # update global step
    tb_logger.update_global_step(1)  # increase global step by 1 (1 iteration or epoch)
    ...
    output = model(data)
    loss = loss_fn(output, gt)  # compute training loss; gt - ground truth values
    ...
    # log several losses
    tb_logger.log_losses({'training_loss': loss.item(),
                          'validation_loss': val_loss.item()})

# close logger
tb_logger.close()  # Now all the scalars logged by log_losses wil be exported to the json file
```

### How to Log Images and Batches

To add image, simple use `log_img` method:

```python
tb_logger.log_img(tag='data/test_image', image_tensor=img)
```

To store image batch as a grid use `log_img_batch`:

```python
tb_logger.log_img_batch(tag='data/test_batch', image_batch=batch)
```

Here is basic example how to log first batch of images for each epoch:

```python
for epoch in range(n_epochs):

    # update global step
    tb_logger.update_global_step(1)  # increase global step by 1, in this case it's epoch
    ...
    for n_batch, data in enumerate(dataloader):
        ...
        output = model(data)
        loss = loss_fn(output, gt)

        # to store first batch of images every epoch:
        if n_batch == 0:
            # to log batch of images as a grid with 4 images in a row and padding of 10
            tb_logger.log_img_batch(tag='data/test_batch', image_batch=output, nrow=4, padding=10)
        ...
```

## How to Extend

If you want to log scalar values of smth, simply add new method to `TBLogger` class. For example, to log an accuracy:

```python
class TBLogger:
    ...
    def log_acc(self, acc):
        self.log_scalar('data/acc', acc)
```

Where, `'data/acc'` - tag, `acc` - accuracy, scalar value.

**NOTE:** `TBLogger` method `log_scalar` writes only scalar value. Take a look at `log_scalars` for logging multiple values.

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
