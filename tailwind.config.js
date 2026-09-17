/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html"],
  theme: {
    extend: {
      colors: {
        accent: {
          DEFAULT: '#FF3B00',
          hover: '#E03400',
          subtle: 'rgba(255, 59, 0, 0.12)',
          border: 'rgba(255, 59, 0, 0.3)',
        },
        studio: {
          bg: '#FFFFFF',
          surface: '#FAFAFA',
          subtle: '#F4F4F3',
          dark: '#0A0A0A',
          card: '#141414',
          border: '#E8E8E8',
          borderDark: '#222222',
        }
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        heading: ['"Plus Jakarta Sans"', 'sans-serif'],
        mono: ['"Space Grotesk"', 'sans-serif'],
      }
    }
  },
  plugins: [],
}
