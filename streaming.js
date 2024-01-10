const { exec } = require('child_process');

// Path to your images
const imageFolderPath = '/Users/chang/nodejs/modelt-3-tnn/public';

// FFmpeg command to convert images to video and stream it
// const ffmpegCommand = `ffmpeg -framerate 1 -i '${imageFolderPath}/%d.jpg' -c:v libx264 -preset ultrafast -tune zerolatency output.mp4`;
// const ffmpegCommand = `ffmpeg -f image2 -loop 1 -i https://raw.githubusercontent.com/illuspas/resources/master/img/admin_panel_dashboard.png -vcodec libx264 -f flv rtmp://localhost/live/streamKey`;
const ffmpegCommand = `ffmpeg -re -y -f image2 -loop 1 -i '${imageFolderPath}/target.jpg' -vcodec libx264 -f flv -flvflags no_duration_filesize rtmp://localhost/live/streamKey`;
// const ffmpegCommand = `ffmpeg -re -i /Users/chang/nodejs/modelt-3-tnn/static/output.mp4 -c copy -f flv rtmp://localhost/live/streamKey`;

const ffmpegProcess = exec(ffmpegCommand);

ffmpegProcess.stderr.on('data', (data) => {
  console.error(`FFmpeg error: ${data}`);
});

ffmpegProcess.on('close', (code) => {
  console.log(`FFmpeg process exited with code ${code}`);
});
