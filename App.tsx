"use client"

import { useState, useEffect } from "react"
import { Navigation, Page } from "./components/Navigation"
import { TrayManager } from "./components/TrayManager"

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('signin')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [userEmail, setUserEmail] = useState<string>()
  const [showTrayDemo, setShowTrayDemo] = useState(false)
  const [unreadMessages, setUnreadMessages] = useState(0)

  // Mock notification system
  useEffect(() => {
    if (isAuthenticated) {
      // Simulate receiving new messages every 30 seconds
      const interval = setInterval(() => {
        if (Math.random() > 0.7) { // 30% chance of new message
          setUnreadMessages(prev => prev + 1)
          
          // Mock desktop notification
          if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('New AI Chat Message', {
              body: 'You have a new message from your AI assistant',
              icon: '/favicon.ico'
            })
          }
        }
      }, 30000)

      return () => clearInterval(interval)
    }
  }, [isAuthenticated])

  // Request notification permission on first load
  useEffect(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission()
    }
  }, [])

  const handleNavigation = (page: Page) => {
    setCurrentPage(page)
    
    if (page === 'chat') {
      setIsAuthenticated(true)
    } else if (page === 'signin') {
      setIsAuthenticated(false)
      setUserEmail(undefined)
      setUnreadMessages(0)
    }
  }

  const handleSignIn = (email: string) => {
    setUserEmail(email)
    handleNavigation('chat')
    
    // Show tray demo after sign in
    setTimeout(() => {
      setShowTrayDemo(true)
    }, 2000)
  }

  // Mock keyboard shortcuts for tray functionality
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl/Cmd + Shift + T to toggle tray demo
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
        e.preventDefault()
        setShowTrayDemo(!showTrayDemo)
      }
      
      // Escape to close tray demo
      if (e.key === 'Escape' && showTrayDemo) {
        setShowTrayDemo(false)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [showTrayDemo])

  return (
    <div className="h-screen">
      <Navigation
        currentPage={currentPage}
        onNavigate={handleNavigation}
        isAuthenticated={isAuthenticated}
        userEmail={userEmail}
      />

      {/* System Tray Demo */}
      <TrayManager
        isVisible={showTrayDemo}
        onClose={() => setShowTrayDemo(false)}
        unreadMessages={unreadMessages}
      />

      {/* Desktop Integration Instructions */}
      {isAuthenticated && (
        <div className="fixed bottom-4 left-4 max-w-xs">
          <div className="bg-card border rounded-lg p-3 shadow-lg">
            <p className="text-xs text-muted-foreground mb-2">
              <strong>Tray Integration:</strong> Press Ctrl+Shift+T (Cmd+Shift+T on Mac) to see tray demo
            </p>
            <p className="text-xs text-muted-foreground">
              For real desktop app functionality, consider using Electron or Tauri
            </p>
          </div>
        </div>
      )}
    </div>
  )
}