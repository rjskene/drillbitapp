import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import theme from '@/assets/themes'

export default createVuetify({
  components,
  directives,
  theme,
  icons: {
    iconfont: 'mdi', // default - only for display purposes
  },
})