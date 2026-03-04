import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { Spin, Radio, Card, Checkbox, Space } from 'antd';
import type { RadioChangeEvent } from 'antd';
import { get } from '../services/api';

interface StockChartProps {
  stockCode: string;
  stockName?: string;
}

interface PriceData {
  trade_date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface Indicators {
  ma?: {
    ma5: (number | null)[];
    ma10: (number | null)[];
    ma20: (number | null)[];
    ma60: (number | null)[];
  };
  macd?: {
    dif: (number | null)[];
    dea: (number | null)[];
    macd: (number | null)[];
  };
  rsi?: {
    rsi: (number | null)[];
  };
  kdj?: {
    k: (number | null)[];
    d: (number | null)[];
    j: (number | null)[];
  };
  boll?: {
    upper: (number | null)[];
    middle: (number | null)[];
    lower: (number | null)[];
  };
}

const StockChart: React.FC<StockChartProps> = ({ stockCode, stockName }) => {
  const [loading, setLoading] = useState(false);
  const [period, setPeriod] = useState('1m');
  const [priceData, setPriceData] = useState<PriceData[]>([]);
  const [indicators, setIndicators] = useState<Indicators>({});
  const [showMA, setShowMA] = useState(true);
  const [showBOLL, setShowBOLL] = useState(false);
  const [showMACD, setShowMACD] = useState(false);
  const [showRSI, setShowRSI] = useState(false);
  const [showKDJ, setShowKDJ] = useState(false);

  useEffect(() => {
    if (stockCode) {
      fetchPriceData();
    }
  }, [stockCode, period, showMA, showBOLL, showMACD, showRSI, showKDJ]);

  const fetchPriceData = async () => {
    setLoading(true);
    try {
      // Build indicator list
      const indicatorList = [];
      if (showMA) indicatorList.push('ma');
      if (showBOLL) indicatorList.push('boll');
      if (showMACD) indicatorList.push('macd');
      if (showRSI) indicatorList.push('rsi');
      if (showKDJ) indicatorList.push('kdj');

      const indicatorParams = indicatorList.length > 0 ? `&indicators=${indicatorList.join(',')}` : '';
      const response = await get(`/api/stocks/${stockCode}/prices?period=${period}${indicatorParams}`);
      setPriceData(response.data || []);
      setIndicators(response.indicators || {});
    } catch (error) {
      console.error('获取行情数据失败:', error);
      setPriceData([]);
      setIndicators({});
    } finally {
      setLoading(false);
    }
  };

  const handlePeriodChange = (e: RadioChangeEvent) => {
    setPeriod(e.target.value);
  };

  const getOption = () => {
    if (!priceData || priceData.length === 0) {
      return {};
    }

    // Prepare data for ECharts
    const dates = priceData.map(item => item.trade_date);
    const candlestickData = priceData.map(item => [
      item.open,
      item.close,
      item.low,
      item.high
    ]);
    const volumes = priceData.map(item => item.volume);

    // Calculate dynamic grid layout
    const subplots = [];
    if (showMACD) subplots.push('MACD');
    if (showRSI) subplots.push('RSI');
    if (showKDJ) subplots.push('KDJ');

    const numSubplots = subplots.length;
    const mainChartHeight = numSubplots === 0 ? 50 : numSubplots === 1 ? 40 : numSubplots === 2 ? 35 : 30;
    const volumeTop = 10 + mainChartHeight + 5;
    const volumeHeight = 12;

    return {
      backgroundColor: 'transparent',
      title: {
        text: `${stockName || stockCode} - K线图`,
        left: 'center',
        top: '5px',
        textStyle: {
          color: '#e8eaed',
          fontSize: 18,
          fontWeight: 'bold'
        }
      },
      legend: {
        top: '35px',
        textStyle: {
          color: '#e8eaed',
          fontSize: 13
        },
        itemGap: 15,
        itemWidth: 25,
        itemHeight: 14,
        data: [
          'K线',
          ...(showMA ? ['MA5', 'MA10', 'MA20', 'MA60'] : []),
          ...(showBOLL ? ['BOLL上轨', 'BOLL中轨', 'BOLL下轨'] : []),
          '成交量',
          ...(showMACD ? ['MACD', 'DIF', 'DEA'] : []),
          ...(showRSI ? ['RSI'] : []),
          ...(showKDJ ? ['KDJ-K', 'KDJ-D', 'KDJ-J'] : [])
        ]
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          crossStyle: {
            color: '#1890ff',
            width: 1,
            type: 'dashed'
          },
          lineStyle: {
            color: '#1890ff',
            width: 1,
            type: 'dashed'
          }
        },
        backgroundColor: 'rgba(26, 31, 58, 0.95)',
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderWidth: 1,
        textStyle: {
          color: '#e8eaed',
          fontSize: 13
        },
        formatter: function (params: any) {
          const dataIndex = params[0].dataIndex;
          const data = priceData[dataIndex];
          let result = `<div style="font-weight: bold; margin-bottom: 8px; color: #1890ff;">📅 ${data.trade_date}</div>`;
          result += `<div style="margin-bottom: 4px;">开盘: <span style="color: #fac858">${data.open.toFixed(2)}</span></div>`;
          result += `<div style="margin-bottom: 4px;">收盘: <span style="color: ${data.close >= data.open ? '#ef5350' : '#26a69a'}">${data.close.toFixed(2)}</span></div>`;
          result += `<div style="margin-bottom: 4px;">最高: <span style="color: #ef5350">${data.high.toFixed(2)}</span></div>`;
          result += `<div style="margin-bottom: 4px;">最低: <span style="color: #26a69a">${data.low.toFixed(2)}</span></div>`;
          result += `<div style="margin-bottom: 8px;">成交量: <span style="color: #9aa0a6">${(data.volume / 10000).toFixed(2)}万手</span></div>`;

          // Add MA indicators
          if (indicators.ma && showMA) {
            result += `<div style="font-weight: bold; margin-top: 8px; margin-bottom: 4px; color: #66bb6a;">📊 均线指标</div>`;
            if (indicators.ma.ma5[dataIndex]) result += `<div>MA5: <span style="color: #40a9ff">${indicators.ma.ma5[dataIndex]?.toFixed(2)}</span></div>`;
            if (indicators.ma.ma10[dataIndex]) result += `<div>MA10: <span style="color: #fac858">${indicators.ma.ma10[dataIndex]?.toFixed(2)}</span></div>`;
            if (indicators.ma.ma20[dataIndex]) result += `<div>MA20: <span style="color: #f06292">${indicators.ma.ma20[dataIndex]?.toFixed(2)}</span></div>`;
            if (indicators.ma.ma60[dataIndex]) result += `<div>MA60: <span style="color: #66bb6a">${indicators.ma.ma60[dataIndex]?.toFixed(2)}</span></div>`;
          }

          // Add BOLL indicators
          if (indicators.boll && showBOLL) {
            result += `<div style="font-weight: bold; margin-top: 8px; margin-bottom: 4px; color: #5470c6;">📈 布林带</div>`;
            if (indicators.boll.upper[dataIndex]) result += `<div>上轨: <span style="color: #ee6666">${indicators.boll.upper[dataIndex]?.toFixed(2)}</span></div>`;
            if (indicators.boll.middle[dataIndex]) result += `<div>中轨: <span style="color: #5470c6">${indicators.boll.middle[dataIndex]?.toFixed(2)}</span></div>`;
            if (indicators.boll.lower[dataIndex]) result += `<div>下轨: <span style="color: #91cc75">${indicators.boll.lower[dataIndex]?.toFixed(2)}</span></div>`;
          }

          // Add MACD indicators
          if (indicators.macd && showMACD) {
            result += `<div style="font-weight: bold; margin-top: 8px; margin-bottom: 4px; color: #f9d900;">⚡ MACD</div>`;
            if (indicators.macd.dif[dataIndex]) result += `<div>DIF: <span style="color: #f9d900">${indicators.macd.dif[dataIndex]?.toFixed(4)}</span></div>`;
            if (indicators.macd.dea[dataIndex]) result += `<div>DEA: <span style="color: #40a9ff">${indicators.macd.dea[dataIndex]?.toFixed(4)}</span></div>`;
            if (indicators.macd.macd[dataIndex]) result += `<div>MACD: <span style="color: ${(indicators.macd.macd[dataIndex] || 0) >= 0 ? '#ef5350' : '#26a69a'}">${indicators.macd.macd[dataIndex]?.toFixed(4)}</span></div>`;
          }

          // Add RSI indicators
          if (indicators.rsi && showRSI) {
            const rsiValue = indicators.rsi.rsi[dataIndex];
            const rsiColor = !rsiValue ? '#9aa0a6' : rsiValue > 70 ? '#ef5350' : rsiValue < 30 ? '#26a69a' : '#fac858';
            result += `<div style="font-weight: bold; margin-top: 8px; margin-bottom: 4px; color: #fac858;">💹 RSI</div>`;
            if (rsiValue) result += `<div>RSI: <span style="color: ${rsiColor}">${rsiValue.toFixed(2)}</span> ${rsiValue > 70 ? '(超买)' : rsiValue < 30 ? '(超卖)' : ''}</div>`;
          }

          // Add KDJ indicators
          if (indicators.kdj && showKDJ) {
            result += `<div style="font-weight: bold; margin-top: 8px; margin-bottom: 4px; color: #5470c6;">🎯 KDJ</div>`;
            if (indicators.kdj.k[dataIndex]) result += `<div>K: <span style="color: #5470c6">${indicators.kdj.k[dataIndex]?.toFixed(2)}</span></div>`;
            if (indicators.kdj.d[dataIndex]) result += `<div>D: <span style="color: #fac858">${indicators.kdj.d[dataIndex]?.toFixed(2)}</span></div>`;
            if (indicators.kdj.j[dataIndex]) result += `<div>J: <span style="color: #ee6666">${indicators.kdj.j[dataIndex]?.toFixed(2)}</span></div>`;
          }

          return result;
        }
      },
      grid: [
        // Main chart (K-line + MA + BOLL)
        {
          left: '8%',
          right: '4%',
          top: '12%',
          height: `${mainChartHeight}%`,
          backgroundColor: 'rgba(255, 255, 255, 0.01)',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          show: true
        },
        // Volume
        {
          left: '8%',
          right: '4%',
          top: `${volumeTop}%`,
          height: `${volumeHeight}%`,
          backgroundColor: 'rgba(255, 255, 255, 0.01)',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          show: true
        },
        // Subplots (MACD, RSI, KDJ)
        ...subplots.map((_, index) => {
          const subplotHeight = numSubplots === 1 ? 20 : numSubplots === 2 ? 18 : 15;
          const baseTop = volumeTop + volumeHeight + 4;
          return {
            left: '8%',
            right: '4%',
            top: `${baseTop + index * (subplotHeight + 3)}%`,
            height: `${subplotHeight}%`,
            backgroundColor: 'rgba(255, 255, 255, 0.01)',
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderWidth: 1,
            show: true
          };
        })
      ],
      xAxis: [
        // Main chart x-axis
        {
          type: 'category',
          data: dates,
          gridIndex: 0,
          axisLine: {
            lineStyle: { color: 'rgba(255, 255, 255, 0.2)' }
          },
          axisLabel: {
            color: '#9aa0a6',
            fontSize: 12,
            formatter: (value: string) => {
              return value.substring(4, 6) + '/' + value.substring(6, 8);
            }
          },
          axisTick: {
            show: false
          }
        },
        // Volume x-axis
        {
          type: 'category',
          data: dates,
          gridIndex: 1,
          axisLine: {
            lineStyle: { color: 'rgba(255, 255, 255, 0.2)' }
          },
          axisLabel: { show: false },
          axisTick: { show: false }
        },
        // Subplot x-axes
        ...subplots.map((_, index) => ({
          type: 'category',
          data: dates,
          gridIndex: 2 + index,
          axisLine: {
            lineStyle: { color: 'rgba(255, 255, 255, 0.2)' }
          },
          axisLabel: {
            show: index === subplots.length - 1,
            color: '#9aa0a6',
            fontSize: 11,
            formatter: (value: string) => {
              return value.substring(4, 6) + '/' + value.substring(6, 8);
            }
          },
          axisTick: { show: false }
        }))
      ],
      yAxis: [
        // Main chart y-axis
        {
          scale: true,
          gridIndex: 0,
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            color: '#9aa0a6',
            fontSize: 12,
            formatter: (value: number) => value.toFixed(2)
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.08)',
              type: 'dashed'
            }
          }
        },
        // Volume y-axis
        {
          scale: true,
          gridIndex: 1,
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            color: '#9aa0a6',
            fontSize: 11,
            formatter: (value: number) => {
              return (value / 10000).toFixed(0) + '万';
            }
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.05)',
              type: 'dashed'
            }
          }
        },
        // Subplot y-axes
        ...subplots.map((name, index) => ({
          scale: true,
          gridIndex: 2 + index,
          name: name,
          nameTextStyle: {
            color: '#1890ff',
            fontSize: 13,
            fontWeight: 'bold',
            padding: [0, 0, 0, -50]
          },
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            color: '#9aa0a6',
            fontSize: 11,
            formatter: (value: number) => value.toFixed(name === 'MACD' ? 4 : 2)
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.08)',
              type: 'dashed'
            }
          }
        }))
      ],
      dataZoom: [
        {
          type: 'inside',
          xAxisIndex: Array.from({ length: 2 + numSubplots }, (_, i) => i),
          start: 0,
          end: 100
        },
        {
          show: true,
          xAxisIndex: Array.from({ length: 2 + numSubplots }, (_, i) => i),
          type: 'slider',
          bottom: '5%',
          start: 0,
          end: 100
        }
      ],
      series: [
        {
          name: 'K线',
          type: 'candlestick',
          data: candlestickData,
          xAxisIndex: 0,
          yAxisIndex: 0,
          itemStyle: {
            color: '#ef5350',
            color0: '#26a69a',
            borderColor: '#ef5350',
            borderColor0: '#26a69a'
          }
        },
        // MA Lines
        ...(indicators.ma && showMA ? [
          {
            name: 'MA5',
            type: 'line',
            data: indicators.ma.ma5,
            smooth: true,
            lineStyle: { width: 2, color: '#40a9ff' },
            xAxisIndex: 0,
            yAxisIndex: 0,
            showSymbol: false,
            emphasis: {
              lineStyle: { width: 3 }
            }
          },
          {
            name: 'MA10',
            type: 'line',
            data: indicators.ma.ma10,
            smooth: true,
            lineStyle: { width: 2, color: '#fac858' },
            xAxisIndex: 0,
            yAxisIndex: 0,
            showSymbol: false,
            emphasis: {
              lineStyle: { width: 3 }
            }
          },
          {
            name: 'MA20',
            type: 'line',
            data: indicators.ma.ma20,
            smooth: true,
            lineStyle: { width: 2, color: '#f06292' },
            xAxisIndex: 0,
            yAxisIndex: 0,
            showSymbol: false,
            emphasis: {
              lineStyle: { width: 3 }
            }
          },
          {
            name: 'MA60',
            type: 'line',
            data: indicators.ma.ma60,
            smooth: true,
            lineStyle: { width: 2, color: '#66bb6a' },
            xAxisIndex: 0,
            yAxisIndex: 0,
            showSymbol: false,
            emphasis: {
              lineStyle: { width: 3 }
            }
          }
        ] : []),
        // BOLL Bands
        ...(indicators.boll && showBOLL ? [
          {
            name: 'BOLL上轨',
            type: 'line',
            data: indicators.boll.upper,
            smooth: true,
            lineStyle: { width: 1.5, color: '#ee6666', type: 'dashed' },
            xAxisIndex: 0,
            yAxisIndex: 0,
            showSymbol: false,
            emphasis: {
              lineStyle: { width: 2.5 }
            }
          },
          {
            name: 'BOLL中轨',
            type: 'line',
            data: indicators.boll.middle,
            smooth: true,
            lineStyle: { width: 2, color: '#5470c6' },
            xAxisIndex: 0,
            yAxisIndex: 0,
            showSymbol: false,
            emphasis: {
              lineStyle: { width: 3 }
            }
          },
          {
            name: 'BOLL下轨',
            type: 'line',
            data: indicators.boll.lower,
            smooth: true,
            lineStyle: { width: 1.5, color: '#91cc75', type: 'dashed' },
            xAxisIndex: 0,
            yAxisIndex: 0,
            showSymbol: false,
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(145, 204, 117, 0.15)' },
                  { offset: 1, color: 'rgba(238, 102, 102, 0.15)' }
                ]
              },
              origin: 'start'
            },
            emphasis: {
              lineStyle: { width: 2.5 }
            }
          }
        ] : []),
        {
          name: '成交量',
          type: 'bar',
          data: volumes,
          xAxisIndex: 1,
          yAxisIndex: 1,
          itemStyle: {
            color: function (params: any) {
              const dataIndex = params.dataIndex;
              const current = priceData[dataIndex];
              return current.close >= current.open ? '#ef5350' : '#26a69a';
            }
          }
        },
        // MACD Indicator
        ...(indicators.macd && showMACD ? (() => {
          const macdGridIndex = 2 + subplots.indexOf('MACD');
          return [
            {
              name: 'MACD',
              type: 'bar',
              data: indicators.macd.macd,
              xAxisIndex: macdGridIndex,
              yAxisIndex: macdGridIndex,
              itemStyle: {
                color: function (params: any) {
                  const value = params.data;
                  if (value >= 0) {
                    return {
                      type: 'linear',
                      x: 0,
                      y: 0,
                      x2: 0,
                      y2: 1,
                      colorStops: [
                        { offset: 0, color: '#ef5350' },
                        { offset: 1, color: 'rgba(239, 83, 80, 0.3)' }
                      ]
                    };
                  } else {
                    return {
                      type: 'linear',
                      x: 0,
                      y: 1,
                      x2: 0,
                      y2: 0,
                      colorStops: [
                        { offset: 0, color: '#26a69a' },
                        { offset: 1, color: 'rgba(38, 166, 154, 0.3)' }
                      ]
                    };
                  }
                }
              },
              emphasis: {
                itemStyle: {
                  borderWidth: 1,
                  borderColor: '#1890ff'
                }
              }
            },
            {
              name: 'DIF',
              type: 'line',
              data: indicators.macd.dif,
              xAxisIndex: macdGridIndex,
              yAxisIndex: macdGridIndex,
              lineStyle: { width: 2, color: '#f9d900' },
              showSymbol: false,
              emphasis: {
                lineStyle: { width: 3 }
              }
            },
            {
              name: 'DEA',
              type: 'line',
              data: indicators.macd.dea,
              xAxisIndex: macdGridIndex,
              yAxisIndex: macdGridIndex,
              lineStyle: { width: 2, color: '#40a9ff' },
              showSymbol: false,
              emphasis: {
                lineStyle: { width: 3 }
              }
            }
          ];
        })() : []),
        // RSI Indicator
        ...(indicators.rsi && showRSI ? (() => {
          const rsiGridIndex = 2 + subplots.indexOf('RSI');
          return [
            {
              name: 'RSI',
              type: 'line',
              data: indicators.rsi.rsi,
              smooth: true,
              xAxisIndex: rsiGridIndex,
              yAxisIndex: rsiGridIndex,
              lineStyle: { width: 2.5, color: '#fac858' },
              showSymbol: false,
              markLine: {
                silent: true,
                symbol: 'none',
                lineStyle: {
                  type: 'dashed',
                  color: '#ef5350',
                  width: 1.5
                },
                label: {
                  color: '#e8eaed',
                  fontSize: 11,
                  formatter: (params: any) => {
                    return params.value === 70 ? '超买 70' : '超卖 30';
                  }
                },
                data: [
                  {
                    yAxis: 70,
                    lineStyle: { color: '#ef5350' }
                  },
                  {
                    yAxis: 30,
                    lineStyle: { color: '#26a69a' }
                  }
                ]
              },
              markArea: {
                silent: true,
                data: [
                  [
                    { yAxis: 70, itemStyle: { color: 'rgba(239, 83, 80, 0.1)' } },
                    { yAxis: 100, itemStyle: { color: 'rgba(239, 83, 80, 0.1)' } }
                  ],
                  [
                    { yAxis: 0, itemStyle: { color: 'rgba(38, 166, 154, 0.1)' } },
                    { yAxis: 30, itemStyle: { color: 'rgba(38, 166, 154, 0.1)' } }
                  ]
                ]
              },
              areaStyle: {
                color: {
                  type: 'linear',
                  x: 0,
                  y: 0,
                  x2: 0,
                  y2: 1,
                  colorStops: [
                    { offset: 0, color: 'rgba(250, 200, 88, 0.4)' },
                    { offset: 0.5, color: 'rgba(250, 200, 88, 0.15)' },
                    { offset: 1, color: 'rgba(250, 200, 88, 0.4)' }
                  ]
                }
              },
              emphasis: {
                lineStyle: { width: 3.5 }
              }
            }
          ];
        })() : []),
        // KDJ Indicator
        ...(indicators.kdj && showKDJ ? (() => {
          const kdjGridIndex = 2 + subplots.indexOf('KDJ');
          return [
            {
              name: 'KDJ-K',
              type: 'line',
              data: indicators.kdj.k,
              smooth: true,
              xAxisIndex: kdjGridIndex,
              yAxisIndex: kdjGridIndex,
              lineStyle: { width: 2.5, color: '#5470c6' },
              showSymbol: false,
              emphasis: {
                lineStyle: { width: 3.5 }
              }
            },
            {
              name: 'KDJ-D',
              type: 'line',
              data: indicators.kdj.d,
              smooth: true,
              xAxisIndex: kdjGridIndex,
              yAxisIndex: kdjGridIndex,
              lineStyle: { width: 2.5, color: '#fac858' },
              showSymbol: false,
              emphasis: {
                lineStyle: { width: 3.5 }
              }
            },
            {
              name: 'KDJ-J',
              type: 'line',
              data: indicators.kdj.j,
              smooth: true,
              xAxisIndex: kdjGridIndex,
              yAxisIndex: kdjGridIndex,
              lineStyle: { width: 2.5, color: '#ee6666' },
              showSymbol: false,
              markLine: {
                silent: true,
                symbol: 'none',
                lineStyle: {
                  type: 'dashed',
                  color: '#ef5350',
                  width: 1.5
                },
                label: {
                  color: '#e8eaed',
                  fontSize: 11,
                  formatter: (params: any) => {
                    return params.value === 80 ? '超买 80' : '超卖 20';
                  }
                },
                data: [
                  {
                    yAxis: 80,
                    lineStyle: { color: '#ef5350' }
                  },
                  {
                    yAxis: 20,
                    lineStyle: { color: '#26a69a' }
                  }
                ]
              },
              markArea: {
                silent: true,
                data: [
                  [
                    { yAxis: 80, itemStyle: { color: 'rgba(239, 83, 80, 0.08)' } },
                    { yAxis: 100, itemStyle: { color: 'rgba(239, 83, 80, 0.08)' } }
                  ],
                  [
                    { yAxis: 0, itemStyle: { color: 'rgba(38, 166, 154, 0.08)' } },
                    { yAxis: 20, itemStyle: { color: 'rgba(38, 166, 154, 0.08)' } }
                  ]
                ]
              },
              emphasis: {
                lineStyle: { width: 3.5 }
              }
            }
          ];
        })() : [])
      ],
      animation: true,
      animationDuration: 800,
      animationEasing: 'cubicOut'
    };
  };

  return (
    <Card
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
          <span>行情走势</span>
          <Space wrap>
            <Checkbox checked={showMA} onChange={(e) => setShowMA(e.target.checked)}>
              MA均线
            </Checkbox>
            <Checkbox checked={showBOLL} onChange={(e) => setShowBOLL(e.target.checked)}>
              布林带
            </Checkbox>
            <Checkbox checked={showMACD} onChange={(e) => setShowMACD(e.target.checked)}>
              MACD
            </Checkbox>
            <Checkbox checked={showRSI} onChange={(e) => setShowRSI(e.target.checked)}>
              RSI
            </Checkbox>
            <Checkbox checked={showKDJ} onChange={(e) => setShowKDJ(e.target.checked)}>
              KDJ
            </Checkbox>
            <Radio.Group value={period} onChange={handlePeriodChange} size="small">
              <Radio.Button value="1m">1个月</Radio.Button>
              <Radio.Button value="3m">3个月</Radio.Button>
              <Radio.Button value="6m">6个月</Radio.Button>
              <Radio.Button value="1y">1年</Radio.Button>
            </Radio.Group>
          </Space>
        </div>
      }
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: '100px 0' }}>
          <Spin size="large" />
          <div style={{ marginTop: '20px' }}>加载行情数据中...</div>
        </div>
      ) : priceData.length > 0 ? (
        <ReactECharts
          option={getOption()}
          style={{
            height: (() => {
              let numSubplots = 0;
              if (showMACD) numSubplots++;
              if (showRSI) numSubplots++;
              if (showKDJ) numSubplots++;

              // Base height: 500px
              // Each subplot adds: 150px
              return `${500 + numSubplots * 150}px`;
            })()
          }}
          notMerge={true}
          lazyUpdate={true}
          opts={{ renderer: 'canvas' }}
        />
      ) : (
        <div style={{ textAlign: 'center', padding: '100px 0', color: '#999' }}>
          暂无行情数据
        </div>
      )}
    </Card>
  );
};

export default StockChart;
