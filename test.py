import matplotlib.pyplot as plt
from torchvision import io

from output import colorize

test_img = io.read_image('random.png', io.ImageReadMode.GRAY)
pred_img = colorize(test_img.unsqueeze(0)).squeeze()

# Visualize the result
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(test_img.permute(1, 2, 0).numpy(), cmap='gray')
plt.title('Input SAR Image (grayscale)')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(pred_img.permute(1, 2, 0).numpy())
plt.title('Output Optical Image (RGB)')
plt.axis('off')

plt.show()
