/** @type {import('tailwindcss').Config} */


/*

Messing around with tailwind snowfall animation.
Something to revisit once the core functionality is complete.

*/
module.exports = {
    content: [
      "./src/**/*.{js,jsx}",
    ],
    theme: {
      extend: {
        animation: {
          'snow-slow': 'snowfall 35s linear infinite',
          'snow-medium': 'snowfall 20s linear infinite',
          'snow-fast': 'snowfall 10s linear infinite',
        },
        keyframes: {
          snowfall: {
            '0%': {
              transform: 'translateY(-100vh) translateX(-5vw)',
            },
            '50%': {
              transform: 'translateY(0vh) translateX(5vw)',
            },
            '100%': {
              transform: 'translateY(100vh) translateX(-5vw)',
            }
          }
        },
      },
    },
    plugins: [],
  }