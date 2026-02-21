/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#f8fafc', // Very subtle light gray-blue background common in modern SaaS
        surface: '#ffffff',
        border: '#e2e8f0',
        primary: '#0f172a',
        muted: '#64748b'
      }
    },
  },
  plugins: [],
}
