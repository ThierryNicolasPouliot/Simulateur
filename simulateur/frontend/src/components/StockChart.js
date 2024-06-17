import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { useParams } from 'react-router-dom';

const StockChart = () => {
    const { topic } = useParams();
    const [data, setData] = useState({});

    useEffect(() => {
        const socket = new WebSocket(`ws://localhost:8000/ws/stocks/${topic}/`);

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'ohlc') {
                const newData = message.data;
                setData(prevData => ({
                    ...prevData,
                    [newData.timestamp]: newData
                }));
            }
        };

        return () => {
            socket.close();
        };
    }, [topic]);

    const plotData = Object.values(data);

    return (
        <Plot
            data={[
                {
                    x: plotData.map(point => point.timestamp),
                    open: plotData.map(point => point.open),
                    high: plotData.map(point => point.high),
                    low: plotData.map(point => point.low),
                    close: plotData.map(point => point.close),
                    type: 'candlestick',
                    xaxis: 'x',
                    yaxis: 'y'
                }
            ]}
            layout={{ title: 'Stock OHLC Chart', xaxis: { title: 'Date' }, yaxis: { title: 'Price' } }}
        />
    );
};

export default StockChart;
