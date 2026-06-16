import { type FormEvent, useEffect, useMemo, useRef, useState } from 'react'
import { fetchDocuments, logout, sendChat } from '../api/client'
import type { AgentType, ChatMessage, DocumentItem, User } from '../types'
import DocumentPanel from './DocumentPanel'

interface Props {
  user: User
  onLogout: () => void
}

const AGENT_OPTIONS: { value: AgentType; label: string; desc: string }[] = [
  { value: 'supervisor', label: '智能助手', desc: '自动分派文档或电影任务' },
  { value: 'document', label: '文档管理', desc: '查询、创建、更新文档' },
  { value: 'movie', label: '电影发现', desc: '搜索电影、查看详情' },
]

const BASE_SUGGESTIONS: Record<AgentType, string[]> = {
  supervisor: ['帮我搜索指环王并保存到文档', '列出我最近的文档', '有什么好看的科幻电影？'],
  document: ['列出我最近的文档', '帮我写一篇关于春天的短文'],
  movie: ['搜索星际穿越', '推荐几部高分科幻电影', '查询电影 ID 157336 的详情'],
}

export default function ChatPage({ user, onLogout }: Props) {
  const [agentType, setAgentType] = useState<AgentType>('supervisor')
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [threadId, setThreadId] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [docRefreshKey, setDocRefreshKey] = useState(0)
  const [documents, setDocuments] = useState<DocumentItem[]>([])
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    let cancelled = false
    setDocuments([])
    async function loadDocs() {
      try {
        const data = await fetchDocuments()
        if (!cancelled) setDocuments(data)
      } catch {
        if (!cancelled) setDocuments([])
      }
    }
    loadDocs()
    return () => {
      cancelled = true
    }
  }, [user.id, docRefreshKey])

  const suggestions = useMemo(() => {
    const items = [...BASE_SUGGESTIONS[agentType]]
    if (agentType === 'document' && documents.length > 0) {
      const first = documents[0]
      items.push(`查看文档 ${first.id}（${first.title}）的详情`)
    }
    return items
  }, [agentType, documents])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  function startNewChat() {
    setMessages([])
    setThreadId(null)
    setError('')
  }

  async function handleSend(text: string) {
    const trimmed = text.trim()
    if (!trimmed || loading) return

    setInput('')
    setError('')
    setMessages((prev) => [...prev, { role: 'user', content: trimmed }])
    setLoading(true)

    try {
      const result = await sendChat(trimmed, agentType, threadId)
      setThreadId(result.thread_id)
      setMessages((prev) => [...prev, { role: 'assistant', content: result.reply }])
      setDocRefreshKey((k) => k + 1)
    } catch (err) {
      setError(err instanceof Error ? err.message : '发送失败')
    } finally {
      setLoading(false)
    }
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    handleSend(input)
  }

  async function handleLogout() {
    try {
      await logout()
    } finally {
      onLogout()
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="logo-mark small">AI</div>
          <div>
            <strong>Django AI Agent</strong>
            <span className="muted">@{user.username}</span>
          </div>
        </div>

        <div className="agent-selector">
          <h3>Agent 类型</h3>
          {AGENT_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              type="button"
              className={`agent-option ${agentType === opt.value ? 'active' : ''}`}
              onClick={() => {
                setAgentType(opt.value)
                startNewChat()
              }}
            >
              <span>{opt.label}</span>
              <small>{opt.desc}</small>
            </button>
          ))}
        </div>

        <DocumentPanel userId={user.id} refreshKey={docRefreshKey} />

        <div className="sidebar-actions">
          <button type="button" className="ghost-btn" onClick={startNewChat}>
            新对话
          </button>
          <button type="button" className="ghost-btn danger" onClick={handleLogout}>
            退出
          </button>
        </div>
      </aside>

      <main className="chat-main">
        <header className="chat-header">
          <div>
            <h2>{AGENT_OPTIONS.find((o) => o.value === agentType)?.label}</h2>
            <p className="muted">
              {threadId ? `会话 ID: ${threadId.slice(0, 8)}...` : '新会话'}
            </p>
          </div>
        </header>

        <div className="messages">
          {messages.length === 0 && !loading && (
            <div className="empty-state">
              <h3>开始对话</h3>
              <p>选择左侧 Agent 类型，或点击以下快捷问题：</p>
              <div className="suggestions">
                {suggestions.map((s) => (
                  <button key={s} type="button" onClick={() => handleSend(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <div className="message-avatar">{msg.role === 'user' ? '你' : 'AI'}</div>
              <div className="message-bubble">
                <pre>{msg.content}</pre>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="message-avatar">AI</div>
              <div className="message-bubble typing">
                <span />
                <span />
                <span />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {error && <div className="error-banner chat-error">{error}</div>}

        <form className="composer" onSubmit={handleSubmit}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="输入消息，Enter 发送，Shift+Enter 换行"
            rows={2}
            disabled={loading}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSend(input)
              }
            }}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            发送
          </button>
        </form>
      </main>
    </div>
  )
}
