import React, { Component } from 'react';

import {
    Navbar,
    Nav,
    NavItem,
    NavDropdown,
    MenuItem,
} from 'react-bootstrap'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

import { BrowserRouter, Route, Link } from 'react-router-dom'

const dataX = [
    { name: 'Total Bounds', inbound: 1212, outbound: 2400 },
    { name: 'Average Bounds', inbound: 3000, outbound: 1398 },

]

class App extends Component {
    constructor() {
        super()

        this.state = {
            allBoundsObj: [],
        }
    }

    componentDidMount() {
        fetch("https://skm-starlingbot.herokuapp.com/dashboard?action=getAllAnalytics")
            .then(res => res.json())
            .then((data) => {
                console.log("fetched allBoundsObj", data);

               

                // this.setState({
                //     allBoundsObj: dataX,
                // })
            })
    }

    render() {
        return (
            <div>
                <div className="row">
                    <div className="col-md-12 text-center" style={{ border: "1px solid #ccc", padding: "15px" }} >
                        <BarChart width={600} height={300} data={dataX} style={{ marginLeft: "20%" }}
                            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                            <XAxis dataKey="name" />
                            <YAxis />
                            <CartesianGrid strokeDasharray="3 3" />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="inbound" fill="#8884d8" background={{ fill: '#eee' }} />
                            <Bar dataKey="outbound" fill="#82ca9d" />
                        </BarChart>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-12 text-center" style={{ border: "1px solid #ccc", padding: "15px" }} >
                        X
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-12 text-center" style={{ border: "1px solid #ccc", padding: "15px" }} >
                        X
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
