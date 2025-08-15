import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format currency value with proper rounding and formatting
 * @param value - The numeric value to format
 * @param currency - Currency symbol (default: '$')
 * @param decimals - Number of decimal places (default: 0 for whole numbers)
 * @returns Formatted currency string
 */
export function formatCurrency(
  value: number, 
  currency: string = '$', 
  decimals: number = 0
): string {
  const roundedValue = decimals === 0 
    ? Math.round(value) 
    : Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals);
  
  return `${currency}${roundedValue.toLocaleString()}`;
}

/**
 * Format price with 2 decimal places for cents
 * @param value - The numeric value to format
 * @returns Formatted price string with cents
 */
export function formatPrice(value: number): string {
  return formatCurrency(value, '$', 2);
}

/**
 * Format price as whole number (no cents)
 * @param value - The numeric value to format
 * @returns Formatted price string without cents
 */
export function formatPriceWhole(value: number): string {
  return formatCurrency(value, '$', 0);
}
