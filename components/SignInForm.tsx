"use client"

import { useState } from "react"
import { useForm } from "react-hook-form@7.55.0"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Label } from "./ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { Alert, AlertDescription } from "./ui/alert"
import { Separator } from "./ui/separator"
import { Eye, EyeOff, Mail, Lock } from "lucide-react"

interface SignInFormData {
  email: string
  password: string
}

interface SignInFormProps {
  onSignIn?: (email: string) => void
}

// Microsoft Logo SVG Component
const MicrosoftIcon = () => (
  <svg width="16" height="16" viewBox="0 0 23 23" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M1 1H11V11H1V1Z" fill="#F25022"/>
    <path d="M12 1H22V11H12V1Z" fill="#7FBA00"/>
    <path d="M1 12H11V22H1V12Z" fill="#00A4EF"/>
    <path d="M12 12H22V22H12V12Z" fill="#FFB900"/>
  </svg>
)

export function SignInForm({ onSignIn }: SignInFormProps) {
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isMicrosoftLoading, setIsMicrosoftLoading] = useState(false)
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<SignInFormData>()

  const onSubmit = async (data: SignInFormData) => {
    setIsLoading(true)
    
    // Simulate API call
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Mock validation - in real app this would be handled by authentication service
      if (data.email === "demo@example.com" && data.password === "password123") {
        onSignIn?.(data.email)
      } else {
        setError("root", {
          message: "Invalid email or password. Try demo@example.com / password123"
        })
      }
    } catch (error) {
      setError("root", {
        message: "An error occurred. Please try again."
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleMicrosoftSignIn = async () => {
    setIsMicrosoftLoading(true)
    
    try {
      // Simulate Microsoft OAuth flow
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Mock successful Microsoft sign-in
      onSignIn?.("user@microsoft.com")
    } catch (error) {
      setError("root", {
        message: "Microsoft sign-in failed. Please try again."
      })
    } finally {
      setIsMicrosoftLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="space-y-1">
        <CardTitle className="text-center">Welcome back</CardTitle>
        <CardDescription className="text-center">
          Sign in to your account to continue
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Microsoft SSO Button */}
        <Button
          variant="outline"
          className="w-full"
          onClick={handleMicrosoftSignIn}
          disabled={isMicrosoftLoading || isLoading}
        >
          <MicrosoftIcon />
          {isMicrosoftLoading ? "Signing in..." : "Continue with Microsoft"}
        </Button>

        {/* Divider */}
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <Separator className="w-full" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-card px-2 text-muted-foreground">
              Or continue with email
            </span>
          </div>
        </div>

        {/* Traditional Email/Password Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {errors.root && (
            <Alert variant="destructive">
              <AlertDescription>{errors.root.message}</AlertDescription>
            </Alert>
          )}
          
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                id="email"
                type="email"
                placeholder="Enter your email"
                className="pl-9"
                {...register("email", {
                  required: "Email is required",
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: "Invalid email address"
                  }
                })}
              />
            </div>
            {errors.email && (
              <p className="text-sm text-destructive">{errors.email.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                className="pl-9 pr-9"
                {...register("password", {
                  required: "Password is required",
                  minLength: {
                    value: 6,
                    message: "Password must be at least 6 characters"
                  }
                })}
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <Eye className="h-4 w-4 text-muted-foreground" />
                )}
              </Button>
            </div>
            {errors.password && (
              <p className="text-sm text-destructive">{errors.password.message}</p>
            )}
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="remember"
                className="h-4 w-4 rounded border border-input bg-background"
              />
              <Label htmlFor="remember" className="text-sm font-normal">
                Remember me
              </Label>
            </div>
            <Button variant="link" className="px-0 text-sm">
              Forgot password?
            </Button>
          </div>

          <Button 
            type="submit" 
            className="w-full" 
            disabled={isLoading || isMicrosoftLoading}
          >
            {isLoading ? "Signing in..." : "Sign in"}
          </Button>

          <div className="text-center text-sm">
            Don't have an account?{" "}
            <Button variant="link" className="px-0">
              Sign up
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}