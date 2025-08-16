'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Car, Lock } from 'lucide-react';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // Basic auth - username: admin, password: admin123
    if (username === 'admin' && password === 'admin123') {
      // Simpan token ke localStorage
      localStorage.setItem('authToken', 'authenticated');
      localStorage.setItem('username', username);
      
      // Redirect langsung ke halaman utama
      window.location.href = '/';
    } else {
      setError('Username atau password salah!');
    }
    
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
            <Car className="h-6 w-6 text-blue-600" />
          </div>
          <CardTitle className="text-2xl font-bold">Car Price Predictor</CardTitle>
          <CardDescription>
            Login untuk mengakses dashboard prediksi harga mobil
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                placeholder="Masukkan username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="Masukkan password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            
            <Button 
              type="submit" 
              className="w-full" 
              disabled={isLoading}
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                  Loading...
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Lock className="h-4 w-4" />
                  Login
                </div>
              )}
            </Button>
          </form>
          
          <div className="mt-6 text-center text-sm text-gray-600">
            <p>Demo Credentials:</p>
            <p>Username: <strong>admin</strong></p>
            <p>Password: <strong>admin123</strong></p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

