import React, { Component } from 'react';

import {
    Navbar,
    Nav,
    NavItem,
    NavDropdown,
    MenuItem,
} from 'react-bootstrap'

import { BrowserRouter, Route, Link } from 'react-router-dom'

import { LinkContainer } from 'react-router-bootstrap'
import { IndexLinkContainer } from 'react-router-bootstrap'

class App extends Component {
    render() {
        return (
            <Navbar>
                <Navbar.Header>

                    <Navbar.Brand>
                        <IndexLinkContainer to="/" activeClassName="active">
                            <NavItem>Home</NavItem>
                        </IndexLinkContainer>

                    </Navbar.Brand>

                </Navbar.Header>
                <Nav>
                <LinkContainer to="/visuals" activeClassName="active">
                    <NavItem eventKey={1}>
                        
                            Visuals
                           
                    </NavItem>
                     </LinkContainer>

                </Nav>
            </Navbar>
        );
    }
}

export default App;
