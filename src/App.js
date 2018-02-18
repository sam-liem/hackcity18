import React, { Component } from 'react';
// import logo from './logo.svg';
// import './App.css';

import UserInfoBox from './components/UserInfoBox'
import ExpenseDistrPiechart from './components/ExpenseDistrPiechart'
import TransactionTable from './components/TransactionTable'

class App extends Component {
  constructor() {
    super()

    this.state = {
      transactionTableRowsList: [],
      user: {},
    }
  }


  componentDidMount() {

    //transactionTableRowsList
    fetch("https://skm-starlingbot.herokuapp.com/dashboard?action=getAllTransactions")
      .then(res => res.json())
      .then((data) => {
        console.log("fetched", data);

        this.setState({
          transactionTableRowsList: data,
        })
      })

    fetch("https://skm-starlingbot.herokuapp.com/dashboard?action=getUserInfo")
      .then(res => res.json())
      .then((data) => {
        console.log("fetched USER", data);

        this.setState({
          user:data,
        })
      })


  }

  render() {
    const { transactionTableRowsList } = this.state
    const { user } = this.state

    return (
      <div className="container">
        <div className="row" style={{marginBottom:"30px"}}>
          <div className="col-md-6">
            <UserInfoBox user={user} />
          </div>
          <div className="col-md-6">
            <ExpenseDistrPiechart />
          </div>
        </div>
        <div className="row">
          <TransactionTable transactionTableRowsList={transactionTableRowsList} />
        </div>
      </div>
    );
  }
}

export default App;
