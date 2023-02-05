// Holds all configuration for various Chart instances

import { dark } from '@/plugins/vuetify'
import { sp500 } from './sp500.js'

CanvasRenderingContext2D.prototype.roundRect = function (x, y, w, h, r) {
  if (w < 2 * r) r = w / 2;
  if (h < 2 * r) r = h / 2;
  this.beginPath();
  this.moveTo(x+r, y);
  this.arcTo(x+w, y,   x+w, y+h, r);
  this.arcTo(x+w, y+h, x,   y+h, r);
  this.arcTo(x,   y+h, x,   y,   r);
  this.arcTo(x,   y,   x+w, y,   r);
  this.closePath();
  return this;
}

// BASE-CHART
// Handles configuration for chart displayed when `noData=true`
const baseColor = dark.colors['blue-darken-1']
export const baseChartData = {
  'labels': [...Array(sp500.length).keys()],
  'datasets': [
    {'data': sp500.reverse()}
  ]
} 
export const baseChartOptions = {
  plugins: {
    legend: {display: false}
  },
  elements: {
    point: {
      radius: 0
    }
  },
  scales: {
      x: {
        grid: {
          display: false,
          borderColor: baseColor,
        },
        ticks: { 
          display: false,
          color: baseColor,
        },
      },
      y: {
        beginAtZero: false,
        grid: {
          display: false,
          borderColor: baseColor
        },
        ticks: { 
          display: false,
          color: baseColor,
        }
      }
  }
}

// Base chart plugins


// SKELETON-CHART 
export const shimmer = {
  id: 'shimmer',
  beforeDraw(chart, args, options) {
    const { ctx, data, chartArea: { bottom, height, left, right, top, width},
      scales: {x, y} } = chart

    ctx.save()
    
    let offset = 0
    requestAnimationFrame(animate)
    function animate(time){
      ctx.clearRect(left,20,width,height)

      let leftEdge = offset > width ? left - width + offset : left
      ctx.fillStyle = 'rgba(255,255,255,0.03)'  
      ctx.fillRect(leftEdge,20,offset,height)

      offset > 2 * width ? offset = 0 : offset += 10
      requestAnimationFrame(animate)
    }
  }
}

// TIME-SERIES-CHART
export const timeSeriesChartOptions = {
  elements: {
    point: {
      radius: 0
    }
  },
  scales: {
      x: {
        grid: {
          display: false,
          borderColor: dark.colors['blue-lighten-4'],
        },
        ticks: { 
          color: dark.colors['blue-lighten-4'],
        },
        type: 'timeseries',
      },
      y: {
        beginAtZero: true,
        grid: {
          display: false,
              borderColor: dark.colors['blue-lighten-4']
        },
        ticks: { 
          color: dark.colors['blue-lighten-4'],
          callback: (value, index, ticks) => '\u20BF ' + value,
        }
      }
  }
}