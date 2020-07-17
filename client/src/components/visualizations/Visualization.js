import React from "react";

import Plotly from "plotly.js";
import createPlotlyComponent from "react-plotly.js/factory";
import Draggable from "react-draggable";

class Visualization extends React.Component {
    render() {
        const Plot = createPlotlyComponent(Plotly);

        return (
            <div>
                <Plot
                    data={[
                        {
                            x: [1, 2, 3, 4],
                            y: [45000, 50000, 55000, 60000],
                            type: "scatter",
                            mode: "markers",
                            marker: { color: "blue" },
                        },
                    ]}
                    layout={{
                        width: 600,
                        height: 400,
                        title: "Scatter",
                    }}
                    config={{ displaylogo: false }}
                />
                <Plot
                    data={[
                        {
                            type: "pie",
                            values: [2, 3, 4, 4],
                            labels: [
                                "Wages",
                                "Operating expenses",
                                "Cost of sales",
                                "Insurance",
                            ],
                            textinfo: "label+percent",
                            insidetextorientation: "radial",
                        },
                    ]}
                    layout={{
                        width: 600,
                        height: 400,
                        title: "Pie",
                        showlegend: false,
                    }}
                    config={{ displaylogo: false }}
                />
                <Plot
                    data={[
                        {
                            x: [1, 2, 3, 4],
                            y: [10, 15, 13, 17],
                            type: "scatter",
                        },
                        {
                            x: [1, 2, 3, 4],
                            y: [16, 5, 11, 9],
                            type: "scatter",
                        },
                    ]}
                    layout={{
                        width: 600,
                        height: 400,
                        title: "Line",
                        showlegend: false,
                    }}
                    config={{ displaylogo: false }}
                />
                <Plot
                    data={[
                        {
                            x: [
                                "Jan",
                                "Feb",
                                "Mar",
                                "Apr",
                                "May",
                                "Jun",
                                "Jul",
                                "Aug",
                                "Sep",
                                "Oct",
                                "Nov",
                                "Dec",
                            ],
                            y: [20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
                            type: "bar",
                            name: "Credit Card",
                            marker: {
                                color: "rgb(49,130,189)",
                                opacity: 0.7,
                            },
                        },
                        {
                            x: [
                                "Jan",
                                "Feb",
                                "Mar",
                                "Apr",
                                "May",
                                "Jun",
                                "Jul",
                                "Aug",
                                "Sep",
                                "Oct",
                                "Nov",
                                "Dec",
                            ],
                            y: [19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
                            type: "bar",
                            name: "KiwiSaver",
                            marker: {
                                color: "rgb(204,204,204)",
                                opacity: 0.5,
                            },
                        },
                    ]}
                    layout={{
                        title: " 2019 Sales Report",
                        xaxis: {
                            tickangle: -45,
                        },
                        barmode: "group",
                    }}
                    config={{ displaylogo: false }}
                />
            </div>
        );
    }
}

export default Visualization;
