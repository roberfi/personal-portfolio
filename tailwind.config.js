/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "cv_personal_page/*/templates/*.{html, js}"
  ],
  safelist: [
    // List classes used in database fields
    "list-disc",
    "list-inside",
  ],
  plugins: [
    require("daisyui"),
  ],
  daisyui: {
    themes: [
      "luxury",
    ],
  },
}
