export interface User {
  id: number
  username: string
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export type AgentType = 'document' | 'movie' | 'supervisor'

export interface DocumentItem {
  id: number
  title: string
  content: string
  created_at: string
  updated_at: string
}
