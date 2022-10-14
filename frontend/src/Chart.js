import React from 'react';
// import ApexCharts from 'apexcharts'
import ApexCharts from "react-apexcharts";

import data_ from './data'


var data = ()=>{
  var array = new Array(100).fill("*")
  // var item = {
  //           x: new Date().getTime(),
  //           y: [Math.random(), Math.random(), Math.random(), Math.random()],
  //         }
  var date =  1538780000000
  array =  array.map((_, index)=>{
            // console.log(_);
            date = date+2000000
            return  {
            x: new Date(date),
            y: [Math.random(), Math.random(), Math.random(), Math.random()],
            buy: Math.random() > 0.5 ? false : true
          }
  })

  return array;
}

var makeData = (candles)=>{
var len = candles.length / 3 
var candles = candles.splice(0, len).map((item)=>{
  return  {
    x: new Date(item[0]),
    // y: [item[1],item[2], item[3], item[4]], // noramal candle
    y: [item[6], item[7], item[8], item[9]], // Heiki Hashi candle
    buy: Math.random() > 0.5 ? false : true
  }
})
return {candles}
}


class ApexChart extends React.Component {
  constructor(props) {
    super(props)

// console.log(props.data.result.chart[0]);
    var {candles}  = makeData(props.data.result.chart)
    console.log(data[0]);
    this.state = {
      series: [
        // {
        //   type: "line", 
        //   name: "Guests",
        //   data: data_,
        // },
        {
          data: candles,
          type: "candlestick", 
          name: "Candle",
        },
      ],
      options: {
        chart: {
          type: 'candlestick',
          // height: 350,
          animations: {
            enabled: false, //no animations
          },
        },
        stroke: {
          curve: 'smooth',
          width: 2,
        },
        title: {
          text: 'CandleStick Chart',
          align: 'left',
        },
        xaxis: {
          type: 'datetime',
        },
        yaxis: {
          tooltip: {
            enabled: true,
          },
        },
        // dataLabels: {
        //   enabled: true,
        //   textAnchor: 'start',
        //   style: {
        //     colors: ['red']
        //   },
        //   formatter: function (val, opt) {
        //     var val = data()[opt.dataPointIndex]['y'][0].toFixed(1)
        //     return val > 0.5 ? 'YES' : null
        //   },
        //   offsetX: 0,
        //   dropShadow: {
        //     // enabled: true
        //   }
        // },

      //   markers: {
      //     size: 4,
      //     colors: '#096',
      //     strokeColors: '#fff',
      //     strokeWidth: 0,
      //     shape: "circle",
      //     onClick: ()=> alert("hi"),
      // },

      // legend: {
      //   show: true,
      //   showForSingleSeries: true,
      //   customLegendItems: ['Buy', 'Sell'],
      //   markers: {
      //     fillColors: ['#00E396', '#775DD0']
      //   }
      // },

      annotations: {
        points: [
          {
            x:  new Date(1538789400000).getTime(), 
            y: 6640,
            borderColor: "#00E396",
            label: {
              borderColor: "#00E396",
              style: {
                color: "#fff",
                background: "#00E396",
              },
              text: "Y Axis Annotation"
            }
          }
        ],
        xaxis: [
          {
            // in a datetime series, the x value should be a timestamp, just like it is generated below
            x: new Date(1538830800000).getTime(),
            strokeDashArray: 0,
            borderColor: "#775DD0",
            label: {
              borderColor: "#775DD0",
              style: {
                color: "#fff",
                background: "#775DD0"
              },
              text: "X Axis Anno Vertical"
            }
          },
          {
            x: new Date(1538803800000).getTime(),
            borderColor: "#FEB019",
            label: {
              borderColor: "#FEB019",
              style: {
                color: "#fff",
                background: "#FEB019"
              },
              orientation: "horizontal",
              text: "X Axis Anno Horizonal"
            }
          }
        ],},
        events: {
          click: function(event, chartContext, config) {
            console.log(event, chartContext, config);
            // The last parameter config contains additional information like `seriesIndex` and `dataPointIndex` for cartesian charts
          }
        }
    
      },
    }
  }


 subSeries = [
    {
      name: "Subs",
      data: [103, 105, 98, 83],
    },
  ];

 subOptions = {
    chart: {
      id: "Subs",
      // group: "social", //group name same as guestOptions
      colors: ['#096'],
    },
    stroke:{
      width: 2
    },
    xaxis: {
      categories: ["2019-05-01", "2019-05-02", "2019-05-03", "2019-05-04"],
    },
  };

  render() {
    return (<div id="chart">
        <ApexCharts
          options={this.state.options}
          series={this.state.series}
          // type="candlestick"
          height={350}
        />
         {/* <ApexCharts
          options={this.subOptions}
          series={this.subSeries}
          // type="line"
          height={150}
        /> */}
      </div>
    )
  }
}


export default ApexChart
