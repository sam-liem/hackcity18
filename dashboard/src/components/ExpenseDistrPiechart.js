import React, { Component } from 'react';

import { PieChart, Pie, Legend } from 'recharts';


class App extends Component {
    render() {
        const { ioBoundObjArr } = this.props

        return (
            <div style={{ border: "1px solid #ccc", height: "100%" }} className="text-center">
                <PieChart width={800} height={400} style={{ marginLeft: "80px" }}>
                    <Pie data={ioBoundObjArr} cx={200} cy={200} fill="#82ca9d" label={true} />
                </PieChart>
            </div>
        );
    }
}

export default App;
