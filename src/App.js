import React, { Component } from 'react';
// import logo from './logo.svg';
// import './App.css';

import UserInfoBox from './components/UserInfoBox'
import ExpenseDistrPiechart from './components/ExpenseDistrPiechart'
import TransactionTable from './components/TransactionTable'

class App extends Component {
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
