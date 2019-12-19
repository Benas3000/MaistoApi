// eslint-disable-next-line
import React, { Component } from 'react';
// eslint-disable-next-line
import axios from 'axios';
import Cookies from 'js-cookie'
// eslint-disable-next-line
import { Input, Label, Modal, ModalHeader, ModalBody, ModalFooter, Table, Button } from 'reactstrap';
// eslint-disable-next-line
import { Navbar, Nav, Form, FormGroup, img } from "react-bootstrap"
import { PlanasCreate } from './Planas'
import { Login } from './login'
import { MaistasCreate } from './Maistas'
import { ReceptasCreate, ReceptaiList, ViewReceptai } from './Receptas'
import { Register, getSession } from './Register'
import Lists from './DuomListai'
// eslint-disable-next-line
import Listai from './DuomListai'
// eslint-disable-next-line
import { Collapse, NavbarToggler, NavbarBrand, NavItem, NavLink, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem, NavbarText } from 'reactstrap';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import logo from './logo.svg'

const HOST = "http://127.0.0.1:5000"
export { HOST };

function App() {
  return (
    <div className="container-fluid px-0" style={{ background: "orange" }}>
      <NavBar />
      <br />
      <FormGroup>
        <Router>
          <Switch>
            <Route path="/logout" exact render={() => {
              Cookies.remove('jwt');
              window.location.href = "/login";
            }} />
            <Route path="/" exact component={Lists} />
            <Route path="/login" exact component={Login} />
            <Route path="/register" exact component={Register} />
            <Route path="/planas/:id/receptas" exact render={({ match }) => (<ReceptaiList match={match} />)} />
            {getSession() ?
              <React.Fragment>
                {getSession().role === 1 &&
                  <React.Fragment>
                    <Route path="/planas" exact component={PlanasCreate} />
                    <Route path="/planasView" exact component={ViewReceptai} />
                    <Route path="/receptas" exact component={ReceptasCreate} />
                    <Route path="/maistas" exact component={MaistasCreate} />
                  </React.Fragment>
                }
              </React.Fragment>
              : null}
          </Switch>
        </Router>

      </FormGroup>
      <Footer />
    </div>
  );

}

function Footer() {
  return <footer className="page-footer font-small blue">

    <div className="footer-copyright text-center py-3 bg-dark">© 2019 Copyright:
      <a href="https://www.facebook.com/"> Suratorius 30000</a>
    </div>

  </footer>
}

function NavBar() {
  return <React.Fragment>
    <Navbar sticky="top" className="w-100" bg="dark" variant="dark" expand="lg">
      <Navbar.Brand href="/">
        <img
          alt=""
          src={logo}
          width="40"
          height="40"
          className="d-inline-block align-top"
        />{' '}
        FoOd
    </Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="/">Home</Nav.Link>

          {getSession() ?
            <React.Fragment>
              {getSession().role === 1 &&
                <React.Fragment>
                  <Nav.Link href="/planas">Add Planas</Nav.Link>
                  <Nav.Link href="/planasView">View Planai</Nav.Link>
                  <Nav.Link href="/receptas">Add receptas</Nav.Link>
                  <Nav.Link href="/maistas">Add Maistas</Nav.Link>
                  <Nav.Link href="/logout">Logout</Nav.Link>
                </React.Fragment>
              }
            </React.Fragment>
            :
            <React.Fragment>
              <Nav.Link href="/login">Login</Nav.Link>
              <Nav.Link href="/register">Register</Nav.Link></React.Fragment>
          }

        </Nav>
      </Navbar.Collapse>
    </Navbar>
  </React.Fragment>
}



export default App;
