/** @type {import('tailwindcss').Config} */

module.exports = {
    content: [
      './src/pages/**/*.{js,ts,jsx,tsx}',
      './src/components/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
      extend: {
        colors: {
          'dolist-darkblue': '#1E2B3D',
          'dolist-cream': '#E8E7E0',
          'dolist-brown': '#362F24',
          'dolist-lightgray': '#848484',
        }
      },
    },
    plugins: [],
}