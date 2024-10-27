

const timeframe = '5Min'
const symbol = 'BTC%2FUSD'
const now = new Date();
const datetime48HoursAgo  = new Date(now.getTime() - 48 * 60 * 60 * 1000);
console.log(datetime48HoursAgo)
const convertedDateTime = datetime48HoursAgo.toISOString();
console.log(convertedDateTime)

const maxCandles = 200

const url = 'https://data.alpaca.markets/v1beta3/crypto/us/bars?symbols=' + symbol + '&start=' + convertedDateTime + '&timeframe=' + timeframe + '&limit='+ maxCandles + '&sort=asc'

const getData = {method: 'GET', headers: {accept: 'application/json'}};


function calculateEMA(data, period = 20) {
    const multiplier = 2 / (period + 1);
    let ema = [];
    
    // First EMA is SMA
    let sum = 0;
    for (let i = 0; i < period; i++) {
        sum += data[i].y[3]; // Using close price
    }
    ema.push(sum / period);
    
    // Calculate EMA for remaining points
    for (let i = period; i < data.length; i++) {
        const close = data[i].y[3];
        const currentEMA = (close - ema[ema.length - 1]) * multiplier + ema[ema.length - 1];
        ema.push(currentEMA);
    }
    
    // Format for ApexCharts
    return data.map((candle, index) => ({
        x: candle.x,
        y: index < period - 1 ? null : ema[index - (period - 1)]
    }));
}

function calculateBollingerBands(data, period = 20, stdDev = 2) {
    let middleBand = [];
    let upperBand = [];
    let lowerBand = [];
    
    for (let i = 0; i < data.length - period + 1; i++) {
        const slice = data.slice(i, i + period);
        const closes = slice.map(candle => candle.y[3]);
        
        // Calculate SMA (middle band)
        const sma = closes.reduce((a, b) => a + b) / period;
        
        // Calculate Standard Deviation
        const sqDiffs = closes.map(value => Math.pow(value - sma, 2));
        const avgSqDiff = sqDiffs.reduce((a, b) => a + b) / period;
        const standardDeviation = Math.sqrt(avgSqDiff);
        
        // Calculate bands
        middleBand.push(sma);
        upperBand.push(sma + standardDeviation * stdDev);
        lowerBand.push(sma - standardDeviation * stdDev);
    }
    
    // Format for ApexCharts
    return {
        middle: data.map((candle, index) => ({
            x: candle.x,
            y: index < period - 1 ? null : middleBand[index - (period - 1)]
        })),
        upper: data.map((candle, index) => ({
            x: candle.x,
            y: index < period - 1 ? null : upperBand[index - (period - 1)]
        })),
        lower: data.map((candle, index) => ({
            x: candle.x,
            y: index < period - 1 ? null : lowerBand[index - (period - 1)]
        }))
    };
}

function calculateRSI(data, period = 14) {
    let gains = [];
    let losses = [];
    let rsi = [];
    
    // Calculate price changes and separate gains/losses
    for (let i = 1; i < data.length; i++) {
        const change = data[i].y[3] - data[i-1].y[3];
        gains.push(change > 0 ? change : 0);
        losses.push(change < 0 ? -change : 0);
    }
    
    // Calculate initial averages
    let avgGain = gains.slice(0, period).reduce((a, b) => a + b) / period;
    let avgLoss = losses.slice(0, period).reduce((a, b) => a + b) / period;
    
    // Calculate first RSI
    let rs = avgGain / avgLoss;
    rsi.push(100 - (100 / (1 + rs)));
    
    // Calculate remaining RSI values
    for (let i = period; i < data.length - 1; i++) {
        avgGain = ((avgGain * (period - 1)) + gains[i]) / period;
        avgLoss = ((avgLoss * (period - 1)) + losses[i]) / period;
        rs = avgGain / avgLoss;
        rsi.push(100 - (100 / (1 + rs)));
    }
    
    // Format for ApexCharts
    return data.map((candle, index) => ({
        x: candle.x,
        y: index <= period ? null : rsi[index - (period + 1)]
    }));
}


fetch(url, getData)
  .then(res => res.json())
  .then(res => {
    console.log(res)
    const transformedData = res.bars["BTC/USD"].map(item => ({
        x: new Date(item.t).getTime(),                 // Timestamp
        y: [item.o, item.h, item.l, item.c]  // [O, H, L, C]
    }));

    console.log(transformedData)
    const ema = calculateEMA(transformedData);
    console.log(ema)
    const bollingerBands = calculateBollingerBands(transformedData);
    console.log(bollingerBands)
    const rsi = calculateRSI(transformedData);
    console.log(rsi)

    const options = {
        series: [
            {
                name: 'EMA 20',
                type: 'line',
                data: ema,
                color: '#FF69B4'
            },
            {
                name: 'BB Upper',
                type: 'line',
                data: bollingerBands.upper,
                color: '#7E57C2',
                dashArray: 5
            },
            {
                name: 'BB Middle',
                type: 'line',
                data: bollingerBands.middle,
                color: '#7E57C2'
            },
            {
                name: 'BB Lower',
                type: 'line',
                data: bollingerBands.lower,
                color: '#7E57C2',
                dashArray: 5
            },
            {
                name: 'Candles',
                type: 'candlestick',
                data: transformedData
            }
        ],
        chart: {
            type: 'line',
            height: '100%',
            foreColor: '#787b86',
            animations: {
                enabled: false
            },
            toolbar: {
                show: true,
                tools: {
                    download: false,
                    selection: true,
                    zoom: true,
                    zoomin: true,
                    zoomout: true,
                    pan: true,
                    reset: true
                },
                autoSelected: 'pan'
            },
            background: '#131722'
        },
        stroke: {
            width: 1
        },
        grid: {
            borderColor: '#2a2e39',
            strokeDashArray: 2,
            yaxis: {
                lines: {
                    show: true
                }
            }
        },
        legend: {
            show: true,
            labels: {
                colors: '#787b86'
            }
        },
        plotOptions: {
            candlestick: {
                colors: {
                    upward: '#089981',
                    downward: '#f23645'
                },
                wick: {
                    useFillColor: true
                }
            }
        },
        xaxis: {
            type: 'datetime',
            labels: {
                style: {
                    colors: '#787b86',
                    fontSize: '11px'
                },
                datetimeFormatter: {
                    hour: 'HH:mm'
                }
            },
            axisBorder: {
                color: '#2a2e39'
            },
            axisTicks: {
                color: '#2a2e39'
            }
        },
        yaxis: [
            {
                seriesName: 'Candles',
                title: {
                    text: 'Price',
                    style: {
                        color: '#787b86'
                    }
                },
                labels: {
                    style: {
                        colors: '#787b86'
                    },
                    formatter: (value) => value.toFixed(2)
                }
            }
        ],
        tooltip: {
            theme: 'dark',
            shared: true,
            x: {
                format: 'HH:mm'
            }
        }
    };

    // Create RSI chart in separate div
    const rsiOptions = {
        series: [{
            name: 'RSI',
            data: rsi
        }],
        chart: {
            type: 'line',
            height: 150,
            toolbar: {
                show: false
            },
            background: '#131722'
        },
        grid: {
            borderColor: '#2a2e39'
        },
        xaxis: {
            type: 'datetime',
            labels: {
                style: {
                    colors: '#787b86'
                }
            }
        },
        yaxis: {
            min: 0,
            max: 100,
            labels: {
                style: {
                    colors: '#787b86'
                }
            }
        },
        annotations: {
            yaxis: [
                {
                    y: 70,
                    borderColor: '#ff9800',
                    label: {
                        text: 'Overbought',
                        style: {
                            color: '#787b86'
                        }
                    }
                },
                {
                    y: 30,
                    borderColor: '#ff9800',
                    label: {
                        text: 'Oversold',
                        style: {
                            color: '#787b86'
                        }
                    }
                }
            ]
        },
        tooltip: {
            theme: 'dark'
        }
    };

    // Create main chart
    const chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();

    // Create RSI chart
    const rsiChart = new ApexCharts(document.querySelector("#rsi-chart"), rsiOptions);
    rsiChart.render();

    })
  .catch(err => console.error(err));


