import React, { Component } from 'react';

import { Table } from 'react-bootstrap'


class App extends Component {


    render() {
        const { user } = this.props
        const { accountData } = user
        console.log("USER", user)

        return (
            <div style={{ border: "1px solid #ccc" }}>
                <div className="card card-inverse card-info">
                    <div className="thumbnail">
                        <img src="http://via.placeholder.com/200x200" alt="..." />
                    </div>
                </div>


                <Table responsive>
                    <thead>
                        <tr>
                            <th>Account Number :</th>
                            <td>{accountData && accountData.accountNumber}</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>ID :</th>
                            <td>{accountData && accountData.id}</td>
                        </tr>
                        <tr>
                            <th>Created At :</th>
                            <td>{accountData && accountData.createdAt}</td>
                        </tr>
                        <tr>
                            <th>IBAN :</th>
                            <td>{accountData && accountData.iban}</td>
                        </tr>

                    </tbody>
                </Table>
            </div>
        );
    }
}

export default App;
