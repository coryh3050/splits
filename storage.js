import { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import { v4 as uuidv4 } from 'uuid';

// Initialize S3 client (using Cloudflare R2 which is S3-compatible)
const s3Client = new S3Client({
  region: 'auto',
  endpoint: process.env.R2_ENDPOINT,
  credentials: {
    accessKeyId: process.env.R2_ACCESS_KEY_ID,
    secretAccessKey: process.env.R2_SECRET_ACCESS_KEY,
  },
});

const BUCKET_NAME = process.env.R2_BUCKET_NAME || 'youtube-automation';

// Storage paths
const STORAGE_PATHS = {
  AUDIO: 'audio',
  VIDEO: 'video',
  THUMBNAIL: 'thumbnail',
  IMAGE: 'image'
};

// Storage operations for the YouTube automation web application

// Upload a file to storage
export async function uploadFile(fileBuffer, fileName, contentType, folder, userId) {
  try {
    // Create a unique file path including user ID for isolation
    const uniqueFileName = `${uuidv4()}-${fileName}`;
    const key = `${folder}/${userId}/${uniqueFileName}`;
    
    const params = {
      Bucket: BUCKET_NAME,
      Key: key,
      Body: fileBuffer,
      ContentType: contentType
    };
    
    const command = new PutObjectCommand(params);
    await s3Client.send(command);
    
    return {
      success: true,
      storagePath: key,
      fileName: uniqueFileName
    };
  } catch (error) {
    console.error('Error uploading file:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Get a file from storage
export async function getFile(storagePath) {
  try {
    const params = {
      Bucket: BUCKET_NAME,
      Key: storagePath
    };
    
    const command = new GetObjectCommand(params);
    const response = await s3Client.send(command);
    
    // Convert stream to buffer
    const chunks = [];
    for await (const chunk of response.Body) {
      chunks.push(chunk);
    }
    
    return {
      success: true,
      data: Buffer.concat(chunks),
      contentType: response.ContentType
    };
  } catch (error) {
    console.error('Error getting file:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Generate a pre-signed URL for direct browser access
export async function getPresignedUrl(storagePath, expiresIn = 3600) {
  try {
    const params = {
      Bucket: BUCKET_NAME,
      Key: storagePath
    };
    
    const command = new GetObjectCommand(params);
    const url = await getSignedUrl(s3Client, command, { expiresIn });
    
    return {
      success: true,
      url
    };
  } catch (error) {
    console.error('Error generating presigned URL:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Delete a file from storage
export async function deleteFile(storagePath) {
  try {
    const params = {
      Bucket: BUCKET_NAME,
      Key: storagePath
    };
    
    const command = new DeleteObjectCommand(params);
    await s3Client.send(command);
    
    return {
      success: true
    };
  } catch (error) {
    console.error('Error deleting file:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// List files in a folder
export async function listFiles(folder, userId) {
  try {
    const prefix = `${folder}/${userId}/`;
    
    const params = {
      Bucket: BUCKET_NAME,
      Prefix: prefix
    };
    
    const command = new ListObjectsV2Command(params);
    const response = await s3Client.send(command);
    
    const files = response.Contents?.map(item => ({
      key: item.Key,
      size: item.Size,
      lastModified: item.LastModified,
      fileName: item.Key.split('/').pop()
    })) || [];
    
    return {
      success: true,
      files
    };
  } catch (error) {
    console.error('Error listing files:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Helper functions for specific file types

// Upload audio file
export async function uploadAudioFile(fileBuffer, fileName, contentType, userId) {
  return uploadFile(fileBuffer, fileName, contentType, STORAGE_PATHS.AUDIO, userId);
}

// Upload video file
export async function uploadVideoFile(fileBuffer, fileName, contentType, userId) {
  return uploadFile(fileBuffer, fileName, contentType, STORAGE_PATHS.VIDEO, userId);
}

// Upload thumbnail image
export async function uploadThumbnail(fileBuffer, fileName, contentType, userId) {
  return uploadFile(fileBuffer, fileName, contentType, STORAGE_PATHS.THUMBNAIL, userId);
}

// Upload custom image for video
export async function uploadCustomImage(fileBuffer, fileName, contentType, userId) {
  return uploadFile(fileBuffer, fileName, contentType, STORAGE_PATHS.IMAGE, userId);
}

// Get audio file
export async function getAudioFile(storagePath) {
  return getFile(storagePath);
}

// Get video file
export async function getVideoFile(storagePath) {
  return getFile(storagePath);
}

// Get thumbnail image
export async function getThumbnail(storagePath) {
  return getFile(storagePath);
}

// Get custom image
export async function getCustomImage(storagePath) {
  return getFile(storagePath);
}

// Get presigned URL for audio file
export async function getAudioPresignedUrl(storagePath) {
  return getPresignedUrl(storagePath);
}

// Get presigned URL for video file
export async function getVideoPresignedUrl(storagePath) {
  return getPresignedUrl(storagePath);
}

// Get presigned URL for thumbnail
export async function getThumbnailPresignedUrl(storagePath) {
  return getPresignedUrl(storagePath);
}

// Get presigned URL for custom image
export async function getCustomImagePresignedUrl(storagePath) {
  return getPresignedUrl(storagePath);
}

// List audio files for a user
export async function listAudioFiles(userId) {
  return listFiles(STORAGE_PATHS.AUDIO, userId);
}

// List video files for a user
export async function listVideoFiles(userId) {
  return listFiles(STORAGE_PATHS.VIDEO, userId);
}

// List thumbnail images for a user
export async function listThumbnails(userId) {
  return listFiles(STORAGE_PATHS.THUMBNAIL, userId);
}

// List custom images for a user
export async function listCustomImages(userId) {
  return listFiles(STORAGE_PATHS.IMAGE, userId);
}
