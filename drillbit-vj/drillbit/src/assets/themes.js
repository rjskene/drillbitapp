const dark = {
  dark: true,
  colors: {
    background: '#21262d',
    surface: '#2c323c',
    // 'surface-01dp': '#1C2636',
    // 'surface-02dp': '#212B3A',
    // 'surface-03dp': '#232D3C',
    // 'surface-04dp': '#26303E',
    // 'surface-06dp': '#2A3442',
    // 'surface-08dp': '#2D3644',
    // 'surface-12dp': '#313B49',
    // 'surface-16dp': '#343D4B',
    // 'surface-24dp': '#363F4D',
    'on-background': '#FFFFFF',
    'on-surface': '#FFFFFF',
    primary: '#273862',
    'primary-variant-1': '#3a5ba9',
    'primary-variant-2': '#dae2ff',
    secondary: '#80ba56',
    error: '#CF6679',
  }
}

export default {
  defaultTheme: 'dark',
  variations: {
    colors: ['surface'],
    lighten: 10
  },
  themes: {
    dark
  }
}