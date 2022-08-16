const colors = require('tailwindcss/colors')
module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        cabin: ["Cabin", "sans-serif"],
        lato: ["Lato", "sans-serif"]
       },
       colors: {
        amablue: {
          first: '#005EB8',
          second: '#00A9E0',
          third: '#9BCAEC',
        }
      }
    }
  },
  variants: {
    extend: {},
  },
  plugins: [require('@tailwindcss/forms')],
}
