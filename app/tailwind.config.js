/** @type {import('tailwindcss').Config} */

module.exports = {
  plugins: [
    // ...
    require('@tailwindcss/forms'),
  ],
    content: [
      './src/pages/**/*.{js,ts,jsx,tsx}',
      './src/components/**/*.{js,ts,jsx,tsx}',
    ],
    darkMode: 'class',
    theme: {
      extend: {
        colors: {
          'dolist-darkblue': '#1E2B3D',
          'dolist-bg-dark': '#233041',
          'dolist-bg-light': '#ffffff',
          'dolist-cream': '#E8E7E0',
          'dolist-brown': '#362F24',
          'dolist-lightgray': '#848484',
          'dolist-gray': '#666464',
          'dolist-green': '#069B15',
        }
      },
      fontFamily: {
        'std': ['Inter', 'sans-serif']
      },
    },
    plugins: [
      require('@tailwindcss/forms'),
    ],
}