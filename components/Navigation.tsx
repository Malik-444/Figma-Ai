"use client"

import { useState } from "react"
import { SignInForm } from "./SignInForm"
import { ChatInterface } from "./ChatInterface"
import { Button } from "./ui/button"
import { LogOut, MessageSquare, User } from "lucide-react"
import { Avatar, AvatarFallback } from "./ui/avatar"

export type Page = 'signin' | 'chat'

interface NavigationProps {
  currentPage: Page
  onNavigate: (page: Page) => void
  isAuthenticated: boolean
  userEmail?: string
}

export function Navigation({ currentPage, onNavigate, isAuthenticated, userEmail }: NavigationProps) {
  const handleSignOut = () => {
    onNavigate('signin')
  }

  if (currentPage === 'chat' && isAuthenticated) {
    return (
      <div className="h-screen flex flex-col">
        {/* Top Navigation Bar */}
        <div className="border-b bg-card px-4 py-2 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <MessageSquare className="h-5 w-5" />
            <span>AI Chat</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-muted-foreground">{userEmail}</span>
            <Avatar className="h-8 w-8">
              <AvatarFallback className="text-xs">
                <User className="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
            <Button variant="ghost" size="sm" onClick={handleSignOut}>
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
        
        {/* Chat Interface */}
        <div className="flex-1">
          <ChatInterface />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <SignInForm onSignIn={(email) => onNavigate('chat')} />
      </div>
    </div>
  )
}