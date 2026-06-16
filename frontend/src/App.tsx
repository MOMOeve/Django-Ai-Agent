import { useEffect, useState } from 'react'
import { ensureCsrf, getMe } from './api/client'
import ChatPage from './components/ChatPage'
import LoginForm from './components/LoginForm'
import type { User } from './types'

export default function App() {
  const [user, setUser] = useState<User | null>(null)
  const [booting, setBooting] = useState(true)

  useEffect(() => {
    async function boot() {
      try {
        await ensureCsrf()
        const me = await getMe()
        setUser(me)
      } catch {
        setUser(null)
      } finally {
        setBooting(false)
      }
    }
    boot()
  }, [])

  if (booting) {
    return (
      <div className="boot-screen">
        <div className="logo-mark">AI</div>
        <p>加载中...</p>
      </div>
    )
  }

  if (!user) {
    return <LoginForm onLogin={setUser} />
  }

  return <ChatPage key={user.id} user={user} onLogout={() => setUser(null)} />
}
