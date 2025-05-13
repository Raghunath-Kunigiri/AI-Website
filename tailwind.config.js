/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./*.html",
        "./src/**/*.{html,js}"
    ],
    theme: {
        extend: {
            colors: {
                primary: '#4f46e5',
                secondary: '#7c3aed'
            }
        }
    },
    plugins: []
}