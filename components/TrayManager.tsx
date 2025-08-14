"use client"

import { useState, useEffect } from "react"
import { Button } from "./ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { Badge } from "./ui/badge"
import { Monitor, Apple, MessageSquare, Settings, X } from "lucide-react"

interface TrayManagerProps {
  isVisible: boolean
  onClose: () => void
  unreadMessages: number
}

export function TrayManager({ isVisible, onClose, unreadMessages }: TrayManagerProps) {
  const [platform, setPlatform] = useState<'windows' | 'mac' | 'unknown'>('unknown')

  useEffect(() => {
    // Detect platform (in a real app, this would be handled by the desktop framework)
    const userAgent = window.navigator.userAgent.toLowerCase()
    if (userAgent.includes('mac')) {
      setPlatform('mac')
    } else if (userAgent.includes('win')) {
      setPlatform('windows')
    }
  }, [])

  if (!isVisible) return null

  const PlatformIcon = platform === 'mac' ? Apple : Monitor

  // Mock tray menu items
  const trayMenuItems = [
    {
      label: 'Open Chat',
      icon: MessageSquare,
      action: () => {
        console.log('Opening chat from tray')
        onClose()
      }
    },
    {
      label: 'Settings',
      icon: Settings,
      action: () => console.log('Opening settings from tray')
    }
  ]

  return (
    <div className="fixed inset-0 bg-black/20 z-50 flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <PlatformIcon className="h-5 w-5" />
              <CardTitle>System Tray Integration</CardTitle>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
          <CardDescription>
            Desktop tray functionality for {platform === 'mac' ? 'macOS' : 'Windows'}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="p-4 bg-muted rounded-lg">
            <h4 className="text-sm font-medium mb-2">Tray Features (Mock)</h4>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Minimize to system tray</li>
              <li>• Show notification badges</li>
              <li>• Quick access menu</li>
              <li>• Background operation</li>
            </ul>
          </div>

          {unreadMessages > 0 && (
            <div className="flex items-center justify-between p-3 bg-primary/10 rounded-lg">
              <span className="text-sm">Unread messages</span>
              <Badge variant="default">{unreadMessages}</Badge>
            </div>
          )}

          <div className="space-y-2">
            <h4 className="text-sm font-medium">Tray Menu</h4>
            {trayMenuItems.map((item, index) => (
              <Button
                key={index}
                variant="ghost"
                className="w-full justify-start"
                onClick={item.action}
              >
                <item.icon className="h-4 w-4 mr-2" />
                {item.label}
              </Button>
            ))}
          </div>

          <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg">
            <p className="text-xs text-amber-800">
              <strong>Note:</strong> This is a web application. For real tray functionality, 
              you would need to build this as a desktop app using Electron, Tauri, or similar frameworks.
            </p>
          </div>

          <div className="text-xs text-muted-foreground space-y-2">
            <p><strong>For Windows:</strong> Use libraries like 'node-notifier' with Electron</p>
            <p><strong>For macOS:</strong> Use NSStatusItem with native app or Electron's Tray API</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}