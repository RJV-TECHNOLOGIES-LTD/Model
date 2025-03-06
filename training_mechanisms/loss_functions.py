import torch.nn.functional as F
import logging

def compute_loss(output, target):
    """
    Compute Mean Squared Error (MSE) loss.

    :param output: Model predictions.
    :param target: Ground truth labels.
    :return: Computed loss.
    """
    try:
        loss = F.mse_loss(output, target)
        return loss
    except Exception as e:
        logging.error(f"Loss computation failed: {e}")
        raise
