/** @type {import('tailwindcss').Config} */
module.exports = {
  mode:'jit',
  content: [
    "./templates/**/*.{html,js}",
    "./templates/*.{html,js}"
  ],
  theme: {
    extend: {
      aspectRatio: {
        "16/9": [16, 9],
        "9/16": [9, 16],
        "4/3": [4, 3],
        "3/4": [3, 4],
        "21/9": [21, 9],
        "9/21": [9, 21],
        "1/1": [1, 1],
        "2/3": [2, 3],
        "3/2": [3, 2],
        "3/5": [3, 5],
        "5/3": [5, 3],
      },
      font: {
        'quote': ["'Josefin Sans', sans-serif"],
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui"),require('@tailwindcss/forms')],
  daisyui: {
    styled: true,
    themes: true,
    base: true,
    utils: true,
    logs: true,
    rtl: false,
    darkTheme: "dracula",
  },
}
