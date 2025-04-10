CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  youtube_credentials TEXT,
  settings TEXT
);

CREATE TABLE audio_files (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  filename TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  status TEXT NOT NULL,
  metadata TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE videos (
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

CREATE TABLE analytics (
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

CREATE TABLE promotions (
  id TEXT PRIMARY KEY,
  video_id TEXT NOT NULL,
  platform TEXT NOT NULL,
  status TEXT NOT NULL,
  post_id TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (video_id) REFERENCES videos(id)
);
