# YouTube Automation App Deployment Guide

This document provides instructions for deploying the YouTube Automation application to production.

## Prerequisites

Before deploying, ensure you have the following:

1. A Cloudflare account for Workers, D1 database, and R2 storage
2. Node.js and npm installed
3. Wrangler CLI installed (`npm install -g wrangler`)
4. YouTube API credentials
5. (Optional) Social media API credentials for promotion features

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Authentication
JWT_SECRET=your_jwt_secret_key

# YouTube API
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
YOUTUBE_REDIRECT_URI=https://your-domain.com/api/auth/youtube/callback

# Storage (Cloudflare R2)
R2_ACCESS_KEY_ID=your_r2_access_key_id
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key
R2_ENDPOINT=https://your-account.r2.cloudflarestorage.com
R2_BUCKET_NAME=youtube-automation-storage

# Social Media APIs (Optional)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
```

## Deployment Steps

1. **Login to Cloudflare**

   ```bash
   wrangler login
   ```

2. **Create D1 Database**

   ```bash
   wrangler d1 create youtube_automation_db
   ```

   Update the `database_id` in `wrangler.toml` with the ID returned from this command.

3. **Create R2 Bucket**

   ```bash
   wrangler r2 bucket create youtube-automation-storage
   ```

4. **Apply Database Migrations**

   ```bash
   wrangler d1 execute youtube_automation_db --file=./migrations/0001_initial.sql
   ```

5. **Build the Application**

   ```bash
   npm run build
   ```

6. **Deploy to Cloudflare Workers**

   ```bash
   wrangler deploy
   ```

7. **Configure Custom Domain (Optional)**

   In the Cloudflare dashboard:
   - Go to Workers & Pages
   - Select your deployed application
   - Go to Custom Domains
   - Add your domain (e.g., youtube-automation.yourdomain.com)

## Post-Deployment Steps

1. **Verify Deployment**

   Visit your application URL to ensure it's working correctly.

2. **Set Up YouTube API Credentials**

   - Go to the Google Cloud Console
   - Create OAuth credentials for the YouTube Data API
   - Add authorized redirect URIs
   - Update the environment variables with your credentials

3. **Configure Social Media Integrations (Optional)**

   Set up API credentials for any social media platforms you want to use for promotion.

## Troubleshooting

- **Database Connection Issues**: Verify your D1 database ID in wrangler.toml
- **Storage Access Problems**: Check R2 credentials and bucket name
- **API Errors**: Ensure all API keys and secrets are correctly set in environment variables
- **Deployment Failures**: Check Cloudflare Workers logs for detailed error messages

## Maintenance

- Regularly backup your D1 database
- Monitor storage usage in your R2 bucket
- Keep API credentials secure and rotate them periodically
- Update dependencies to maintain security and performance
