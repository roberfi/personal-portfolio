/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "cv_personal_page/templates/*.html",
    "cv_personal_page/frontend/**/*.js",
    "cv_personal_page/*/templates/*.html",
  ],
  safelist: [
    // List classes used in database fields
    "list-disc",
    "list-inside",
  ],
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        cv_personal_page: {
          primary: "#fdba74",
          secondary: "#93c5fd",
          accent: "#f97316",
          neutral: "#111827",
          "base-100": "#4b5563",
          info: "#0ea5e9",
          success: "#4ade80",
          warning: "#fef08a",
          error: "#f87171",
        },
      },
    ],
  },
};
