module.exports = {
  purge: false,
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      backgroundSize: {
        '50': '100%'
      },
      backgroundImage: {
        'ld-ls': "url('/ld-bg.png')"
      },
      colors: {
        aws: '#FF9900',
        ldblue: '#3DD6F5',
        lddblue: '#405BFF',
        ldred: '#FF386B',
        ldpurple: '#A34FDE',
        ldyellow: '#EBFF38',
        ldgray: '#282828',
        ldgraytext: '#BCBEC0',
        ldhl: '#EBFF38'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
