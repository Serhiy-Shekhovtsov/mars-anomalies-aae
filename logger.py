"""Loggers.
"""

import os
import torchvision.utils as vutils
from tensorboardX import SummaryWriter


class TBLogger(object):
    """TensorBoard logger.
    """
    def __init__(self, log_dir: str):
        self.log_dir = log_dir
        self.writer = SummaryWriter(self.log_dir)
        self.global_step = 0

    def log_scalar(self, tag: str, scalar_value) -> None:
        """Writes scalar value.

        Args:
            tag (str): data identifier.
            scalar_value (float?): value to save.
        """
        self.writer.add_scalar(tag, scalar_value, self.global_step)

    def log_scalars(self, main_tag: str, tag_scalar_dict: dict) -> None:
        """Writes scalar value.

        Note from official repo: this function also keeps logged scalars in memory. In extreme case it explodes your RAM.

        Args:
            main_tag (str): parent name for the tags.
            tag_scalar_dict (dict): key-value pair storing the tag and corresponding values.
        """
        self.writer.add_scalars(main_tag, tag_scalar_dict, self.global_step)

    def add_loss(self, loss):
        """Increments global step and logs new loss
        
        Args:
            loss (float?): loss value
        """

        self.update_global_step(1)
        self.log_loss(loss)

    def log_loss(self, loss) -> None:
        """Logs Loss data.

        Args:
            loss (float?): loss value.
        """
        self.log_scalar('data/loss', loss)

    def log_losses(self, losses: dict) -> None:
        """Logs several losses values.

        Note: Values logged by this method can be exported to json for external processing.
        Note from official repo: this function also keeps logged scalars in memory. In extreme case it explodes your RAM.

        Args:
            losses (dict): key-value pair storing the losses and corresponding values.

        Example:
            tb_logger.log_losses({'training_loss': 0.1, 'val_loss': 0.2})
        """
        self.log_scalars('losses', losses)

    def log_img(self, tag: str, image_tensor) -> None:
        """Logs image data.

        Args:
            tag (str): image tag.
            image_tensor (torch.Tensor, numpy.array): image data.
        """
        self.writer.add_image(tag, image_tensor, self.global_step)

    def log_img_batch(self, tag: str, image_batch, **kwargs) -> None:
        """Logs batch of images.

        Args:
            tag (str): image tag.
            image_batch (torch.Tensor): batch of images of shape (BCHW).
            **kwargs: other arguments are documented in torchvision.utils.make_grid.
        """
        self.log_img(tag, vutils.make_grid(image_batch, **kwargs))

    def update_global_step(self, step: int) -> None:
        """Updates global step by step.

        Note: `global_step` will be updated by specified `step` incrementally : global_step += step.

        Args:
            step (int): batch size/epoch step/iteration step.

        Usage:
            use this method just right before/after logging step;
            at the start/end of an iteration or an epoch to update global step.
        """
        self.global_step += step

    def close(self, file_name: str = 'scalars.json') -> None:
        """Exports scalar data to JSON file for external processing in log_dir then closes the writer.
           Format: {writer_id : [[timestamp, step, value], ...], ...}

        Args:
            file_name (str): file name for the json file. Default: 'scalars.json'
        """
        self.writer.export_scalars_to_json(os.path.join(self.log_dir, file_name))
        self.writer.close()
