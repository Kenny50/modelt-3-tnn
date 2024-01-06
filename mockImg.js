const fs = require('fs');
const Jimp = require('jimp');

const directory = 'public/';

if (!fs.existsSync(directory)) {
  fs.mkdirSync(directory);
}

const createImage = async (number) => {
  const backgroundColor = 0xffcccccc; // Gray background color

  const image = new Jimp(250, 250, backgroundColor); // Increase image size for better visibility of the text

  const font = await Jimp.loadFont(Jimp.FONT_SANS_128_WHITE); // Adjusted font size

  // Get text width and height to properly center it
  const textWidth = Jimp.measureText(font, number.toString());
  const textHeight = Jimp.measureTextHeight(font, number.toString());

  const textX = (image.bitmap.width - textWidth) / 2;
  const textY = (image.bitmap.height - textHeight) / 2;

  image.print(font, textX, textY, {
    text: number.toString()
  });

  // Adding noise to increase complexity
  for (let i = 0; i < image.bitmap.width; i += 2) {
    for (let j = 0; j < image.bitmap.height; j += 2) {
      const color = Jimp.rgbaToInt(255, Math.random() * 255, Math.random() * 255, Math.random() * 255);
      image.setPixelColor(color, i, j);
    }
  }

  const imagePath = `${directory}/${number}.jpg`; // Use JPEG format

  // Function to save the image with a target size (around 200KB)
  const saveImage = async (quality) => {
    await image.quality(quality).writeAsync(imagePath);

    const stats = fs.statSync(imagePath);
    if (stats.size > 200 * 1024) {
      await saveImage(quality); // Decrease quality to reduce size
    }
  };

  // Start saving the image with an initial quality
  await saveImage(100); // High initial quality
};

const generateImages = async () => {
  for (let i = 1; i <= 50; i++) {
    await createImage(i);
  }
};

generateImages()
  .then(() => console.log('Images created successfully!'))
  .catch((err) => console.error('Error creating images:', err));
