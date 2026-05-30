/**
 * Sample TypeScript file that triggers the lint-on-save hook.
 *
 * When this file is saved in Kiro, the "Lint on Save" hook (fileEdited event)
 * will automatically run: npx eslint --fix {file}
 *
 * This file intentionally contains minor style issues that ESLint would fix:
 * - Inconsistent quotes
 * - Missing semicolons
 * - Trailing spaces
 */

// Example: a utility function with minor style issues
function calculateDiscount(price: number, percentage: number): number {
  if (percentage < 0 || percentage > 100) {
    throw new Error("Percentage must be between 0 and 100")
  }

  const discount = price * (percentage / 100)
  return price - discount
}

// Example: an async function with inconsistent formatting
const fetchUserData = async (userId: string) => {
  const baseUrl = "https://api.example.com"
  const response = await fetch(`${baseUrl}/users/${userId}`)

  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.status}`)
  }

  return response.json()
}

// Example: interface with optional fields
interface UserProfile {
  id: string
  name: string
  email: string
  role?: "admin" | "user" | "viewer"
  lastLogin?: Date
}

// Example: function using the interface
function formatUserDisplay(user: UserProfile): string {
  const role = user.role ?? "user"
  return `${user.name} (${role}) - ${user.email}`
}

export { calculateDiscount, fetchUserData, formatUserDisplay }
export type { UserProfile }
