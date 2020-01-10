from manifold_test.base_types.transform import pearson_window
import time
import uuid
import random
from loguru import logger
import creme.stats
from manifold.transformers import SmoothPearsonTransformer


# F = -kx - Thats for the force. If we're trying to get the overall

# x = F/-k
# The force will revert the other direction as well.

# Eh, that aint happening.

smooth_pearson = SmoothPearsonTransformer(window=20)
model_id = uuid.uuid4().hex
while True:
    logger.info(smooth_pearson.step(random.randint(0, 1000), model_id=model_id))
    time.sleep(0.001)