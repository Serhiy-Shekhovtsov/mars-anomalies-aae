"""Loggers.
"""

from tensorboardX import SummaryWriter


class TBLogger(object):
    """Tensorboard logger.
    """
    def __init__(self, log_dir: str):
        self.log_dir = log_dir
        self.writer = SummaryWriter(self.log_dir)

    def log(self, tag: str, scalar_value, global_step: int) -> None:
        """Stores value.

        tag (str): data identifier.
        scalar_value (???): value to save.
        global_step (int): global step value to record (iteration number, batch number (total) etc).
        """
        self.writer.add_scalar(tag, scalar_value, global_step)

    def log_loss(self, loss, global_step: int) -> None:
        """Logs Loss data.

        loss (type?): loss value.
        global_step (int): global step value to record.
        """
        self.log('data/loss', loss, global_step)

    def close(self) -> None:
        """Exports scalar data to JSON for external processing.
        """
        self.writer.export_scalars_to_json(self.log_dir + '/scalars.json')
        self.writer.close()
