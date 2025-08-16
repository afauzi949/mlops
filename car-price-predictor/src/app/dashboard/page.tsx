'use client';

import { ProtectedRoute } from '@/components/protected-route';
import { useAuth } from '@/lib/auth-context';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Car, LogOut, User, BarChart3 } from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const { username, logout } = useAuth();

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center gap-3">
                <Car className="h-8 w-8 text-blue-600" />
                <h1 className="text-xl font-bold text-gray-900">Car Price Predictor</h1>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <User className="h-4 w-4" />
                  <span>Welcome, {username}!</span>
                </div>
                <Button variant="outline" onClick={logout} size="sm">
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </Button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Single Prediction Card */}
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Car className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <CardTitle>Single Prediction</CardTitle>
                    <CardDescription>Prediksi harga satu mobil</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600 mb-4">
                  Masukkan spesifikasi mobil untuk mendapatkan prediksi harga yang akurat.
                </p>
                <Link href="/">
                  <Button className="w-full">
                    Mulai Prediksi
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Batch Prediction Card */}
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <BarChart3 className="h-6 w-6 text-green-600" />
                  </div>
                  <div>
                    <CardTitle>Batch Prediction</CardTitle>
                    <CardDescription>Prediksi harga multiple mobil</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600 mb-4">
                  Upload file CSV untuk prediksi harga multiple mobil sekaligus.
                </p>
                <Link href="/batch">
                  <Button className="w-full">
                    Batch Prediction
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Stats Card */}
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <BarChart3 className="h-6 w-6 text-purple-600" />
                  </div>
                  <div>
                    <CardTitle>Statistics</CardTitle>
                    <CardDescription>Statistik prediksi</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Total Predictions</span>
                    <span className="font-semibold">1,234</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Accuracy</span>
                    <span className="font-semibold text-green-600">95.2%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Model Version</span>
                    <span className="font-semibold">v1.0.0</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
