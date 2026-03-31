/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#f9f9f9',
        primary: '#FFE01B',
        danger: '#FF3B30',
        success: '#34C759',
        border: '#000000'
      },
      boxShadow: {
        'neo': '6px 6px 0px #000',
        'neo-sm': '4px 4px 0px #000',
        'neo-hover': '2px 2px 0px #000',
      },
      borderWidth: {
        '4': '4px',
      },
      fontFamily: {
        sans: ['Space Grotesk', 'Outfit', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
