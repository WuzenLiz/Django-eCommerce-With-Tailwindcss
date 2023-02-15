/** @type {import('tailwindcss').Config} */
module.exports = {
  mode:'jit',
  content: [
    "./**/templates/**/*.{html,js}",
    "./**/templates/*.{html,js}"
  ],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
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
