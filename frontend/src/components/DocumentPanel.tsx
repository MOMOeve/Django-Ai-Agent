import { useEffect, useState } from 'react'
import { fetchDocuments } from '../api/client'
import type { DocumentItem } from '../types'

interface Props {
  userId: number
  refreshKey: number
}

export default function DocumentPanel({ userId, refreshKey }: Props) {
  const [documents, setDocuments] = useState<DocumentItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false
    setDocuments([])
    async function load() {
      setLoading(true)
      setError('')
      try {
        const data = await fetchDocuments()
        if (!cancelled) setDocuments(data)
      } catch (err) {
        if (!cancelled) {
          setDocuments([])
          setError(err instanceof Error ? err.message : '加载失败')
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [userId, refreshKey])

  return (
    <div className="document-panel">
      <h3>我的文档</h3>
      {loading && <p className="muted">加载中...</p>}
      {error && <p className="error-text">{error}</p>}
      {!loading && !error && documents.length === 0 && (
        <p className="muted">暂无文档，可通过对话创建</p>
      )}
      <ul className="document-list">
        {documents.map((doc) => (
          <li key={doc.id} className="document-item">
            <strong>{doc.title}</strong>
            <span className="doc-preview">
              {doc.content?.slice(0, 60) || '（无内容）'}
              {(doc.content?.length ?? 0) > 60 ? '...' : ''}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
