import { sql } from '@vercel/postgres';
import { v4 as uuidv4 } from 'uuid';

// Database initialization and operations for the YouTube automation web application

// Create database tables
export async function initializeDatabase() {
  try {
    // Create users table
    await sql`
      CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        youtube_credentials TEXT,
        settings TEXT
      );
    `;

    // Create audio_files table
    await sql`
      CREATE TABLE IF NOT EXISTS audio_files (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        filename TEXT NOT NULL,
        storage_path TEXT NOT NULL,
        status TEXT NOT NULL,
        metadata TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
      );
    `;

    // Create videos table
    await sql`
      CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        audio_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        youtube_id TEXT,
        title TEXT NOT NULL,
        description TEXT,
        thumbnail_path TEXT,
        video_path TEXT NOT NULL,
        status TEXT NOT NULL,
        upload_time TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (audio_id) REFERENCES audio_files(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
      );
    `;

    // Create analytics table
    await sql`
      CREATE TABLE IF NOT EXISTS analytics (
        id TEXT PRIMARY KEY,
        video_id TEXT NOT NULL,
        views INTEGER DEFAULT 0,
        likes INTEGER DEFAULT 0,
        comments INTEGER DEFAULT 0,
        watch_time INTEGER DEFAULT 0,
        data TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (video_id) REFERENCES videos(id)
      );
    `;

    // Create promotions table
    await sql`
      CREATE TABLE IF NOT EXISTS promotions (
        id TEXT PRIMARY KEY,
        video_id TEXT NOT NULL,
        platform TEXT NOT NULL,
        status TEXT NOT NULL,
        post_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (video_id) REFERENCES videos(id)
      );
    `;

    return { success: true, message: 'Database initialized successfully' };
  } catch (error) {
    console.error('Error initializing database:', error);
    return { success: false, error: error.message };
  }
}

// User operations
export async function createUser(userData) {
  try {
    const id = uuidv4();
    const { email, name, youtube_credentials, settings } = userData;
    
    const result = await sql`
      INSERT INTO users (id, email, name, youtube_credentials, settings)
      VALUES (${id}, ${email}, ${name}, ${JSON.stringify(youtube_credentials || null)}, ${JSON.stringify(settings || null)})
      RETURNING *;
    `;
    
    return { success: true, user: result.rows[0] };
  } catch (error) {
    console.error('Error creating user:', error);
    return { success: false, error: error.message };
  }
}

export async function getUserById(userId) {
  try {
    const result = await sql`
      SELECT * FROM users WHERE id = ${userId};
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'User not found' };
    }
    
    return { success: true, user: result.rows[0] };
  } catch (error) {
    console.error('Error getting user:', error);
    return { success: false, error: error.message };
  }
}

export async function updateUser(userId, userData) {
  try {
    const { email, name, youtube_credentials, settings } = userData;
    
    const result = await sql`
      UPDATE users
      SET 
        email = COALESCE(${email}, email),
        name = COALESCE(${name}, name),
        youtube_credentials = COALESCE(${JSON.stringify(youtube_credentials || null)}, youtube_credentials),
        settings = COALESCE(${JSON.stringify(settings || null)}, settings)
      WHERE id = ${userId}
      RETURNING *;
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'User not found' };
    }
    
    return { success: true, user: result.rows[0] };
  } catch (error) {
    console.error('Error updating user:', error);
    return { success: false, error: error.message };
  }
}

export async function deleteUser(userId) {
  try {
    const result = await sql`
      DELETE FROM users WHERE id = ${userId} RETURNING *;
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'User not found' };
    }
    
    return { success: true, user: result.rows[0] };
  } catch (error) {
    console.error('Error deleting user:', error);
    return { success: false, error: error.message };
  }
}

// Audio file operations
export async function createAudioFile(fileData) {
  try {
    const id = uuidv4();
    const { user_id, filename, storage_path, status, metadata } = fileData;
    
    const result = await sql`
      INSERT INTO audio_files (id, user_id, filename, storage_path, status, metadata)
      VALUES (${id}, ${user_id}, ${filename}, ${storage_path}, ${status}, ${JSON.stringify(metadata || null)})
      RETURNING *;
    `;
    
    return { success: true, audioFile: result.rows[0] };
  } catch (error) {
    console.error('Error creating audio file:', error);
    return { success: false, error: error.message };
  }
}

export async function getAudioFilesByUserId(userId) {
  try {
    const result = await sql`
      SELECT * FROM audio_files WHERE user_id = ${userId} ORDER BY created_at DESC;
    `;
    
    return { success: true, audioFiles: result.rows };
  } catch (error) {
    console.error('Error getting audio files:', error);
    return { success: false, error: error.message };
  }
}

export async function getAudioFileById(fileId) {
  try {
    const result = await sql`
      SELECT * FROM audio_files WHERE id = ${fileId};
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'Audio file not found' };
    }
    
    return { success: true, audioFile: result.rows[0] };
  } catch (error) {
    console.error('Error getting audio file:', error);
    return { success: false, error: error.message };
  }
}

export async function updateAudioFile(fileId, fileData) {
  try {
    const { status, metadata } = fileData;
    
    const result = await sql`
      UPDATE audio_files
      SET 
        status = COALESCE(${status}, status),
        metadata = COALESCE(${JSON.stringify(metadata || null)}, metadata)
      WHERE id = ${fileId}
      RETURNING *;
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'Audio file not found' };
    }
    
    return { success: true, audioFile: result.rows[0] };
  } catch (error) {
    console.error('Error updating audio file:', error);
    return { success: false, error: error.message };
  }
}

export async function deleteAudioFile(fileId) {
  try {
    const result = await sql`
      DELETE FROM audio_files WHERE id = ${fileId} RETURNING *;
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'Audio file not found' };
    }
    
    return { success: true, audioFile: result.rows[0] };
  } catch (error) {
    console.error('Error deleting audio file:', error);
    return { success: false, error: error.message };
  }
}

// Video operations
export async function createVideo(videoData) {
  try {
    const id = uuidv4();
    const { 
      audio_id, 
      user_id, 
      youtube_id, 
      title, 
      description, 
      thumbnail_path, 
      video_path, 
      status, 
      upload_time 
    } = videoData;
    
    const result = await sql`
      INSERT INTO videos (
        id, audio_id, user_id, youtube_id, title, description, 
        thumbnail_path, video_path, status, upload_time
      )
      VALUES (
        ${id}, ${audio_id}, ${user_id}, ${youtube_id}, ${title}, ${description}, 
        ${thumbnail_path}, ${video_path}, ${status}, ${upload_time}
      )
      RETURNING *;
    `;
    
    return { success: true, video: result.rows[0] };
  } catch (error) {
    console.error('Error creating video:', error);
    return { success: false, error: error.message };
  }
}

export async function getVideosByUserId(userId) {
  try {
    const result = await sql`
      SELECT * FROM videos WHERE user_id = ${userId} ORDER BY created_at DESC;
    `;
    
    return { success: true, videos: result.rows };
  } catch (error) {
    console.error('Error getting videos:', error);
    return { success: false, error: error.message };
  }
}

export async function getVideoById(videoId) {
  try {
    const result = await sql`
      SELECT * FROM videos WHERE id = ${videoId};
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'Video not found' };
    }
    
    return { success: true, video: result.rows[0] };
  } catch (error) {
    console.error('Error getting video:', error);
    return { success: false, error: error.message };
  }
}

export async function updateVideo(videoId, videoData) {
  try {
    const { 
      youtube_id, 
      title, 
      description, 
      thumbnail_path, 
      status, 
      upload_time 
    } = videoData;
    
    const result = await sql`
      UPDATE videos
      SET 
        youtube_id = COALESCE(${youtube_id}, youtube_id),
        title = COALESCE(${title}, title),
        description = COALESCE(${description}, description),
        thumbnail_path = COALESCE(${thumbnail_path}, thumbnail_path),
        status = COALESCE(${status}, status),
        upload_time = COALESCE(${upload_time}, upload_time)
      WHERE id = ${videoId}
      RETURNING *;
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'Video not found' };
    }
    
    return { success: true, video: result.rows[0] };
  } catch (error) {
    console.error('Error updating video:', error);
    return { success: false, error: error.message };
  }
}

export async function deleteVideo(videoId) {
  try {
    const result = await sql`
      DELETE FROM videos WHERE id = ${videoId} RETURNING *;
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'Video not found' };
    }
    
    return { success: true, video: result.rows[0] };
  } catch (error) {
    console.error('Error deleting video:', error);
    return { success: false, error: error.message };
  }
}

// Analytics operations
export async function createOrUpdateAnalytics(analyticsData) {
  try {
    const { video_id, views, likes, comments, watch_time, data } = analyticsData;
    
    // Check if analytics already exist for this video
    const existingResult = await sql`
      SELECT * FROM analytics WHERE video_id = ${video_id};
    `;
    
    if (existingResult.rows.length > 0) {
      // Update existing analytics
      const result = await sql`
        UPDATE analytics
        SET 
          views = ${views},
          likes = ${likes},
          comments = ${comments},
          watch_time = ${watch_time},
          data = ${JSON.stringify(data || null)},
          updated_at = CURRENT_TIMESTAMP
        WHERE video_id = ${video_id}
        RETURNING *;
      `;
      
      return { success: true, analytics: result.rows[0] };
    } else {
      // Create new analytics
      const id = uuidv4();
      
      const result = await sql`
        INSERT INTO analytics (id, video_id, views, likes, comments, watch_time, data)
        VALUES (${id}, ${video_id}, ${views}, ${likes}, ${comments}, ${watch_time}, ${JSON.stringify(data || null)})
        RETURNING *;
      `;
      
      return { success: true, analytics: result.rows[0] };
    }
  } catch (error) {
    console.error('Error creating/updating analytics:', error);
    return { success: false, error: error.message };
  }
}

export async function getAnalyticsByVideoId(videoId) {
  try {
    const result = await sql`
      SELECT * FROM analytics WHERE video_id = ${videoId};
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'Analytics not found' };
    }
    
    return { success: true, analytics: result.rows[0] };
  } catch (error) {
    console.error('Error getting analytics:', error);
    return { success: false, error: error.message };
  }
}

export async function getAnalyticsByUserId(userId) {
  try {
    const result = await sql`
      SELECT a.* 
      FROM analytics a
      JOIN videos v ON a.video_id = v.id
      WHERE v.user_id = ${userId};
    `;
    
    return { success: true, analytics: result.rows };
  } catch (error) {
    console.error('Error getting analytics by user:', error);
    return { success: false, error: error.message };
  }
}

// Promotion operations
export async function createPromotion(promotionData) {
  try {
    const id = uuidv4();
    const { video_id, platform, status, post_id } = promotionData;
    
    const result = await sql`
      INSERT INTO promotions (id, video_id, platform, status, post_id)
      VALUES (${id}, ${video_id}, ${platform}, ${status}, ${post_id})
      RETURNING *;
    `;
    
    return { success: true, promotion: result.rows[0] };
  } catch (error) {
    console.error('Error creating promotion:', error);
    return { success: false, error: error.message };
  }
}

export async function getPromotionsByVideoId(videoId) {
  try {
    const result = await sql`
      SELECT * FROM promotions WHERE video_id = ${videoId} ORDER BY created_at DESC;
    `;
    
    return { success: true, promotions: result.rows };
  } catch (error) {
    console.error('Error getting promotions:', error);
    return { success: false, error: error.message };
  }
}

export async function updatePromotion(promotionId, promotionData) {
  try {
    const { status, post_id } = promotionData;
    
    const result = await sql`
      UPDATE promotions
      SET 
        status = COALESCE(${status}, status),
        post_id = COALESCE(${post_id}, post_id)
      WHERE id = ${promotionId}
      RETURNING *;
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'Promotion not found' };
    }
    
    return { success: true, promotion: result.rows[0] };
  } catch (error) {
    console.error('Error updating promotion:', error);
    return { success: false, error: error.message };
  }
}

export async function deletePromotion(promotionId) {
  try {
    const result = await sql`
      DELETE FROM promotions WHERE id = ${promotionId} RETURNING *;
    `;
    
    if (result.rows.length === 0) {
      return { success: false, error: 'Promotion not found' };
    }
    
    return { success: true, promotion: result.rows[0] };
  } catch (error) {
    console.error('Error deleting promotion:', error);
    return { success: false, error: error.message };
  }
}
