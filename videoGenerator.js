import { processAudio } from './audioProcessor';
import { createVisualizer } from './visualizer';
import { generateThumbnail } from './thumbnailCreator';
import ffmpeg from 'fluent-ffmpeg';
import { promises as fs } from 'fs';
import path from 'path';
import os from 'os';

// Video generation module for YouTube automation

// Process audio file to extract beat information, tempo, etc.
export async function processAudio(audioBuffer) {
  try {
    // Save audio buffer to temp file
    const tempDir = os.tmpdir();
    const audioPath = path.join(tempDir, `audio-${Date.now()}.mp3`);
    await fs.writeFile(audioPath, audioBuffer);
    
    // Process audio to extract beat information
    const audioAnalysis = await processAudio(audioPath);
    
    // Clean up temp file
    await fs.unlink(audioPath);
    
    return {
      success: true,
      bpm: audioAnalysis.bpm,
      beats: audioAnalysis.beats,
      duration: audioAnalysis.duration,
      waveform: audioAnalysis.waveform
    };
  } catch (error) {
    console.error('Error processing audio:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Generate video from audio and optional custom images
export async function generateVideo(audioBuffer, audioAnalysis, imageFiles = [], effects = {}, title) {
  try {
    // Save audio buffer to temp file
    const tempDir = os.tmpdir();
    const audioPath = path.join(tempDir, `audio-${Date.now()}.mp3`);
    await fs.writeFile(audioPath, audioBuffer);
    
    // Create temp output path
    const outputPath = path.join(tempDir, `video-${Date.now()}.mp4`);
    
    // Generate visualizer frames based on audio analysis
    const visualizerPath = await createVisualizer(
      audioAnalysis,
      imageFiles,
      effects,
      title,
      tempDir
    );
    
    // Combine visualizer with audio using ffmpeg
    await new Promise((resolve, reject) => {
      ffmpeg()
        .input(visualizerPath)
        .input(audioPath)
        .outputOptions([
          '-c:v libx264',
          '-pix_fmt yuv420p',
          '-c:a aac',
          '-shortest'
        ])
        .output(outputPath)
        .on('end', () => resolve())
        .on('error', (err) => reject(err))
        .run();
    });
    
    // Read the generated video
    const videoBuffer = await fs.readFile(outputPath);
    
    // Clean up temp files
    await fs.unlink(audioPath);
    await fs.unlink(visualizerPath);
    await fs.unlink(outputPath);
    
    return {
      success: true,
      videoBuffer
    };
  } catch (error) {
    console.error('Error generating video:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Create thumbnail from video
export async function createThumbnail(videoBuffer) {
  try {
    // Save video buffer to temp file
    const tempDir = os.tmpdir();
    const videoPath = path.join(tempDir, `video-${Date.now()}.mp4`);
    await fs.writeFile(videoPath, videoBuffer);
    
    // Create temp output path for thumbnail
    const thumbnailPath = path.join(tempDir, `thumbnail-${Date.now()}.jpg`);
    
    // Extract thumbnail from video using ffmpeg
    await new Promise((resolve, reject) => {
      ffmpeg(videoPath)
        .screenshots({
          timestamps: ['50%'],
          filename: path.basename(thumbnailPath),
          folder: path.dirname(thumbnailPath),
          size: '1280x720'
        })
        .on('end', () => resolve())
        .on('error', (err) => reject(err));
    });
    
    // Read the generated thumbnail
    const thumbnailBuffer = await fs.readFile(thumbnailPath);
    
    // Clean up temp files
    await fs.unlink(videoPath);
    await fs.unlink(thumbnailPath);
    
    return {
      success: true,
      thumbnailBuffer
    };
  } catch (error) {
    console.error('Error creating thumbnail:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Generate enhanced thumbnail with text overlay
export async function generateEnhancedThumbnail(thumbnailBuffer, title, effects = {}) {
  try {
    // This would use image manipulation libraries to add text, effects, etc.
    // For now, we'll just return the original thumbnail
    return {
      success: true,
      thumbnailBuffer
    };
  } catch (error) {
    console.error('Error generating enhanced thumbnail:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
