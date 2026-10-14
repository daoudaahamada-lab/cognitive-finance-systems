import {Config} from '@remotion/cli/config';

// Export MP4 : H.264, yuv420p (lisible partout : LinkedIn, Instagram, TikTok, iPhone).
Config.setCodec('h264');
Config.setPixelFormat('yuv420p');
Config.setColorSpace('bt709'); // couleurs fidèles, plage vidéo standard
Config.setCrf(16);
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setOverwriteOutput(true);
