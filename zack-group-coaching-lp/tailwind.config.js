/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    fontFamily: {
      'serif': ['Bentham', 'serif'],
      'sans': ['Quicksand', 'sans-serif'],

    },
    // make desktop first 
    screens: {
        'sm': {'max': '639px'},
        'md': {'max': '767px'},
        'lg': {'max': '1023px'},
        'xl': {'max': '1279px'},
        '2xl': {'max': '1535px'},
    },
    extend: {},
  },
  plugins: [],
}

