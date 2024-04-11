/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    fontFamily: {
      'sans': ['Heebo', 'sans-serif'],
    },
    extend: {
      transitionDuration: {
        DEFAULT: '200ms',
      },
      transitionTimingFunction: {
        DEFAULT: 'ease',
      },
      spacing: {
         '15': '3.75rem',
      },
      backgroundImage: {
        'image-random': "url('https://source.unsplash.com/random/1920x1080/')",
        'image-random-dark': "url('https://source.unsplash.com/featured/1920x1080/?dark')",
        'image-random-light': "url('https://source.unsplash.com/featured/1920x1080/?white')",
      }
    },
  },
  plugins: [],
}
