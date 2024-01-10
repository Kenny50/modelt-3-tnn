const fs = require('fs');
const Jimp = require('jimp');

const directory = 'public/';

if (!fs.existsSync(directory)) {
  fs.mkdirSync(directory);
}

const backgroundColor = 0xffcccccc; // Gray background color
const imageSize = 250;
let currentNumber = 1;

const fontLoadPromise = Jimp.loadFont(Jimp.FONT_SANS_128_WHITE);

const updateImage = async () => {
  const image = new Jimp(imageSize, imageSize, backgroundColor);

  const font = await fontLoadPromise;

  const number = currentNumber.toString();
  const textWidth = Jimp.measureText(font, number);
  const textHeight = Jimp.measureTextHeight(font, number);

  const textX = (imageSize - textWidth) / 2;
  const textY = (imageSize - textHeight) / 2;

  image.print(font, textX, textY, {
    text: number
  });

  for (let i = 0; i < imageSize; i += 2) {
    for (let j = 0; j < imageSize; j += 2) {
      const color = Jimp.rgbaToInt(255, Math.random() * 255, Math.random() * 255, Math.random() * 255);
      image.setPixelColor(color, i, j);
    }
  }

  const imagePath = `${directory}/target.jpg`;

  const saveImage = async (quality) => {
    await image.quality(quality).writeAsync(imagePath);
    const stats = fs.statSync(imagePath);
    if (stats.size > 200 * 1024) {
      await saveImage(quality);
    }
  };

  await saveImage(100);
};

// Call the function to create and start updating the image
updateImage(); // Initial image creation

const interval = setInterval(() => {
  currentNumber = (currentNumber % 99) + 1; // Loop from 1 to 99
  updateImage(); // Update the image with the new number
}, 100);

// Stop the interval after a certain time (for example, after 10 seconds)
// setTimeout(() => {
//   clearInterval(interval);
// }, 10000); // Adjust the duration as needed
