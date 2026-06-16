import type { AgentType, DocumentItem, User } from '../types'

const API_BASE = '/api'

function getCsrfToken(): string | null {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/)
  return match ? decodeURIComponent(match[1]) : null
}

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers)
  if (!(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json')
  }
  const csrf = getCsrfToken()
  if (csrf && options.method && options.method !== 'GET') {
    headers.set('X-CSRFToken', csrf)
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: 'include',
  })

  if (!response.ok) {
    let detail = '请求失败'
    try {
      const data = await response.json()
      detail = data.detail || detail
    } catch {
      // ignore parse errors
    }
    throw new Error(detail)
  }

  if (response.status === 204) {
    return undefined as T
  }
  return response.json()
}

export async function ensureCsrf(): Promise<void> {
  await request('/auth/csrf/')
}

export async function getMe(): Promise<User> {
  return request<User>('/auth/me/')
}

export async function login(username: string, password: string): Promise<User> {
  await ensureCsrf()
  return request<User>('/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export async function logout(): Promise<void> {
  await request('/auth/logout/', { method: 'POST' })
}

export async function sendChat(
  message: string,
  agentType: AgentType,
  threadId?: string | null,
): Promise<{ reply: string; thread_id: string }> {
  return request('/chat/', {
    method: 'POST',
    body: JSON.stringify({
      message,
      agent_type: agentType,
      thread_id: threadId ?? null,
    }),
  })
}

export async function fetchDocuments(): Promise<DocumentItem[]> {
  return request<DocumentItem[]>('/documents/')
}
