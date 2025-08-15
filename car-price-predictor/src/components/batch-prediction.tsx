'use client';

import React, { useState, useRef } from 'react';
import { Upload, Download, FileText, AlertCircle, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { predictCarPrice } from '@/lib/api';
import { CarData, PredictionResponse } from '@/types/car';
import { formatPriceWhole } from '@/lib/utils';

export function BatchPrediction() {
  const [isLoading, setIsLoading] = useState(false);
  const [predictions, setPredictions] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setIsLoading(true);
    setError(null);
    setPredictions(null);

    try {
      const text = await file.text();
      const lines = text.split('\n');
      const headers = lines[0].split(',').map(h => h.trim());
      
      // Parse CSV data
      const carData: CarData[] = [];
      for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim()) {
          const values = lines[i].split(',').map(v => v.trim());
          const car: Partial<CarData> & { [key: string]: string | number } = {};
          
          headers.forEach((header, index) => {
            const value = values[index];
            if (header === 'car_ID' || header === 'symboling' || 
                header === 'wheelbase' || header === 'carlength' || 
                header === 'carwidth' || header === 'carheight' || 
                header === 'curbweight' || header === 'enginesize' || 
                header === 'boreratio' || header === 'stroke' || 
                header === 'compressionratio' || header === 'horsepower' || 
                header === 'peakrpm' || header === 'citympg' || 
                header === 'highwaympg') {
              car[header] = parseFloat(value) || 0;
            } else {
              car[header] = value;
            }
          });
          
          // Convert carbrand and cartype to CarName for API compatibility
          if (car.carbrand && car.cartype && !car.CarName) {
            car.CarName = `${car.carbrand} ${car.cartype}`;
            // Remove carbrand and cartype to avoid conflicts
            delete car.carbrand;
            delete car.cartype;
          }
          
          // Ensure CarName exists (required by API)
          if (!car.CarName) {
            throw new Error(`Missing CarName for car ID ${car.car_ID}`);
          }
          
          carData.push(car as CarData);
        }
      }

      if (carData.length === 0) {
        throw new Error('No valid data found in CSV file');
      }

      const response = await predictCarPrice(carData);
      setPredictions(response);
    } catch (err) {
      console.error('Error processing file:', err);
      setError('Failed to process CSV file. Please check the format and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const downloadResults = () => {
    if (!predictions) return;

    const csvContent = [
      'car_ID,predicted_price',
      ...predictions.predictions.map((pred, index) => `${index + 1},${Math.round(pred.predicted_price)}`)
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'car_price_predictions.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const handleReset = () => {
    setPredictions(null);
    setError(null);
    setFileName(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-6 w-6" />
          Batch Prediction
        </CardTitle>
        <CardDescription>
          Upload a CSV file with multiple car specifications to get batch price predictions.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* File Upload */}
        <div className="space-y-4">
          <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center">
            <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Upload a CSV file with car specifications
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500 mb-4">
              The CSV should include all required fields: car_ID, symboling, fueltype, etc.
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              className="hidden"
              id="csv-upload"
            />
            <label htmlFor="csv-upload">
              <Button asChild>
                <span>Choose CSV File</span>
              </Button>
            </label>
          </div>

          {fileName && (
            <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
              <FileText className="h-4 w-4" />
              <span>Selected file: {fileName}</span>
            </div>
          )}
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-400">Processing predictions...</p>
          </div>
        )}

        {/* Results */}
        {predictions && (
          <div className="space-y-4">
            <div className="bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400" />
                <h3 className="font-semibold text-green-800 dark:text-green-200">
                  Predictions Complete
                </h3>
              </div>
              <p className="text-green-700 dark:text-green-300">
                Successfully predicted prices for {predictions.predictions.length} cars.
              </p>
            </div>

            {/* Results Table */}
            <div className="border rounded-lg overflow-hidden">
              <div className="bg-gray-50 dark:bg-gray-800 px-4 py-3 border-b">
                <h4 className="font-semibold text-gray-900 dark:text-white">
                  Prediction Results
                </h4>
              </div>
              <div className="max-h-64 overflow-y-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-900 dark:text-white">
                        Car ID
                      </th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-900 dark:text-white">
                        Predicted Price
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    {predictions.predictions.map((prediction, index) => (
                      <tr key={index} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                        <td className="px-4 py-2 text-sm text-gray-900 dark:text-white">
                          {index + 1}
                        </td>
                        <td className="px-4 py-2 text-sm font-medium text-green-600 dark:text-green-400">
                          {formatPriceWhole(prediction.predicted_price)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Download Button */}
            <div className="flex gap-4">
              <Button onClick={downloadResults} className="flex items-center gap-2">
                <Download className="h-4 w-4" />
                Download Results (CSV)
              </Button>
              <Button variant="outline" onClick={handleReset}>
                Upload Another File
              </Button>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400" />
              <h3 className="font-semibold text-red-800 dark:text-red-200">
                Error
              </h3>
            </div>
            <p className="text-red-700 dark:text-red-300">{error}</p>
            <Button
              variant="outline"
              size="sm"
              onClick={handleReset}
              className="mt-3"
            >
              Try Again
            </Button>
          </div>
        )}

        {/* Instructions */}
        <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <h4 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">
            CSV Format Requirements
          </h4>
          <ul className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
            <li>• Include all required fields: car_ID, symboling, CarName (or carbrand+cartype), fueltype, etc.</li>
            <li>• Use comma as delimiter</li>
            <li>• First row should contain headers</li>
            <li>• Maximum 100 cars per batch</li>
            <li>• Ensure all numeric fields contain valid numbers</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}
