import React, { Component } from 'react';
// import logo from './logo.svg';
// import './App.css';

import UserInfoBox from './components/UserInfoBox'
import ExpenseDistrPiechart from './components/ExpenseDistrPiechart'
import TransactionTable from './components/TransactionTable'

class App extends Component {
  constructor(){
    super()

    this.state={
      transactionTableRowsList:[],
    }
  }


  componentDidMount(){
    fetch("https://skm-starlingbot.herokuapp.com/dashboard?action=getAllTransactions")
    .then(res=>res.json())
    .then((data)=>{
      console.log("fetched",data);
    })
  }

  render() {
    return (
      <div className="App">
        <UserInfoBox />
        <ExpenseDistrPiechart />
        <TransactionTable />
      </div>
    );
  }
}

export default App;
