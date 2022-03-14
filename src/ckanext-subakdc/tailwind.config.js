module.exports = {
  content: ['./ckanext/subakdc/**/*.{html,js}', '../ckanext-subakdc-plugins/**/*.{html,js}'],
  important: true,
  theme: {
    fontFamily: {
      'default': ['TeX Gyre Heros', 'Helvetica', 'Arial', 'sans-serif'],
      'body': ['Comfortaa', 'Helvetica', 'Arial', 'sans-serif'],
      'heading': ['TeX Gyre Heros', 'Helvetica', 'Arial', 'sans-serif'],
      'mono': ['Ubuntu Mono', 'monospace']
    },
    extend: {
      colors: {
        'subak-deep-ocean': '#0f2b43',
        'subak-burnt-copper': '#c95e3b',
        'subak-stone-grey': '#eeeeec',
        'subak-meadow-teal': '#1d838b',
        'subak-purple-rain': '#b0566b',
        'subak-marine-blue': '#1b658f',
        'subak-sky-blue': '#3bc8ec'
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}