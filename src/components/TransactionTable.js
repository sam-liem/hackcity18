import React, { Component } from 'react';

import { Table } from 'react-bootstrap'


class App extends Component {

    render() {
        const { transactionTableRowsList } = this.props

        return (
            <Table striped bordered condensed hover responsive>
                {/* <TableHead /> */}
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>AMOUNT</th>
                        <th>CURRENCY</th>
                        <th>DIRECTION</th>
                        <th>SOURCE</th>
                        <th>CREATED</th>
                        <th>BALANCE</th>
                    </tr>
                </thead>
                <tbody>
                    {transactionTableRowsList.map(transactionTableRow => {
                        return (
                            <tr key={transactionTableRow.id}>
                                <td>{transactionTableRow.id}</td>
                                <td>{transactionTableRow.amount}</td>
                                <td>{transactionTableRow.currency}</td>
                                <td>{transactionTableRow.direction}</td>
                                <td>{transactionTableRow.source}</td>
                                <td>{transactionTableRow.created}</td>
                                <td>{transactionTableRow.balance}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </Table>
        );
    }
}

export default App;
