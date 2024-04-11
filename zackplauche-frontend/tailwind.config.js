/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  theme: {
    screens: {
      '2xl': { 'max': '1535px' },
      // => @media (max-width: 1535px) { ... }

      'xl': { 'max': '1279px' },
      // => @media (max-width: 1279px) { ... }

      'lg': { 'max': '1023px' },
      // => @media (max-width: 1023px) { ... }

      'md': { 'max': '767px' },
      // => @media (max-width: 767px) { ... }

      'sm': { 'max': '639px' },
      // => @media (max-width: 639px) { ... }
    },
    fontFamily: {
      'sans': ['Montserrat', 'sans-serif'],
      'serif': ['Bentham', 'serif'],
      'mono': ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', '"Liberation Mono"', '"Courier New"', 'monospace'],
    },
    extend: {
      transitionDuration: {
        DEFAULT: '200ms',
        '400': '400ms',
      },
      transitionTimingFunction: {
        DEFAULT: 'ease',
      },
      letterSpacing: {
        tightest: '-.1em',
      },
      backgroundImage: {
        'batumi': "url('rsz_zack-batumi.jpg')",
        'white-flower': "url('blue-white-flower.jpg')",
      },
      colors: {
        discord: {
          DEFAULT: '#6068f1',
          gray: '#24272a'
        },
        green: {
          DEFAULT: '#21de31',
        },
        blue: {
          light: '#2ec7ff',
          DEFAULT: '#21abde',
          dark: '#004a66',
          darkest: '#0c181e',
        },
        cyan: {
          light: '#48edff',
          DEFAULT: '#00e7ff',
          dark: '#00b1c5',
        },
        red: {
          DEFAULT: '#ff0000',
        }
      },
      spacing: {
        '15': '3.75rem',
      }
    },
  },
  plugins: [
    function ({ addVariant }) {
      addVariant('active-class', '&.active')
    },
    function groupPeer({ addVariant }) {
      let pseudoVariants = [
        // ... Any other pseudo variants you want to support. 
        // See https://github.com/tailwindlabs/tailwindcss/blob/6729524185b48c9e25af62fc2372911d66e7d1f0/src/corePlugins.js#L78
        "checked",
      ].map((variant) =>
        Array.isArray(variant) ? variant : [variant, `&:${variant}`],
      );

      for (let [variantName, state] of pseudoVariants) {
        addVariant(`group-peer-${variantName}`, (ctx) => {
          let result = typeof state === "function" ? state(ctx) : state;
          return result.replace(/&(\S+)/, ":merge(.peer)$1 ~ .group &");
        });
      }
    },
    require('@tailwindcss/typography')
  ],
}
