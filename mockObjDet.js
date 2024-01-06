const fs = require('fs');
var counter = 0;

var imgMap = new Map();
// Function to populate the Map with image data
function populateImageMap() {
    const imageKeys = [];

    for (let i = 1; i <= 50; i++) {
      imageKeys.push(i.toString());
    }
    imageKeys.forEach(key => {
        const imagePath = `public/${key}.jpg`;
        const imageData = fs.readFileSync(imagePath);
        const base64Image = Buffer.from(imageData).toString('base64');
        imgMap.set(key, base64Image);
    });
}

// Call this function to populate the Map
populateImageMap();
function mockObjDet() {
    counter++;
    if (counter === 120) {
        counter = 0;
    }
    let mockObj = {
        x: 12,
        y: 4,
        width: 80,
        height: 120,
        class: 'car'
    }
    const img = imgMap.get(`${(counter % 50) + 1}`)
    let mockFormat = {
        images: [img, img, img],
        objects_top: [mockObj],
        objects_left: [],
        objects_right: [mockObj, mockObj],
    }
    return mockFormat
}

// console.log(mockObjDet());
module.exports = mockObjDet;