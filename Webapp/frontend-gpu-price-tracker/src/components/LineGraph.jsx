import '../App.css'
import {Line} from 'react-chartjs-2'
import {Chart as Chartjs, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend} from 'chart.js';
Chartjs.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function LineGraph({data}){
    if (!Array.isArray(data)) {
        return <div>Loading chart...</div>
    }
    const chartData = {
        labels: data.map(item => item.Date),
        datasets: [
            {
                label: "Price",
                data: data.map(item => item.AvgPrice),
                borderColor: "rgb(10, 113, 231)"
            }
        ]
    };
    return <Line data={chartData} />;
}

export default LineGraph;