import { NextResponse } from 'next/server';
import { v4 as uuidv4 } from 'uuid';

// Mock database for development
let users = [];
let audioFiles = [];
let videos = [];
let analytics = [];
let promotions = [];

// API Routes

// User endpoints
export async function GET(request) {
  return NextResponse.json({ users });
}

export async function POST(request) {
  const data = await request.json();
  
  const newUser = {
    id: uuidv4(),
    email: data.email,
    name: data.name,
    created_at: new Date().toISOString(),
    youtube_credentials: data.youtube_credentials || null,
    settings: data.settings || null
  };
  
  users.push(newUser);
  
  return NextResponse.json({ user: newUser });
}

// Helper function to get user by ID
export async function getUserById(userId) {
  return users.find(user => user.id === userId);
}

// Helper function to update user
export async function updateUser(userId, userData) {
  const index = users.findIndex(user => user.id === userId);
  
  if (index !== -1) {
    users[index] = { ...users[index], ...userData };
    return users[index];
  }
  
  return null;
}

// Helper function to delete user
export async function deleteUser(userId) {
  const index = users.findIndex(user => user.id === userId);
  
  if (index !== -1) {
    const deletedUser = users[index];
    users = users.filter(user => user.id !== userId);
    return deletedUser;
  }
  
  return null;
}
