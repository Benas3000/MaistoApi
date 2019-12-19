// eslint-disable-next-line
import React, { useState ,Component } from 'react';
import axios from 'axios';
// eslint-disable-next-line
import Cookies from 'js-cookie'
import { HOST } from "../App"
// eslint-disable-next-line
import { Input, FormGroup, Label, Table, Button } from 'reactstrap';
import Modal from 'react-modal'

const customStyles = {
    content : {
      top                   : '50%',
      left                  : '50%',
      right                 : 'auto',
      bottom                : 'auto',
      marginRight           : '-50%',
      transform             : 'translate(-50%, -50%)'
    }
  };

export class Login extends React.Component {
    
    
    constructor(props) {
        super(props);
        this.state = {
            Name: '',
            Password: '',
            modalIsOpen: false,
            errorMsg: ''
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
    }
 
    render() {
        return (
            <div class="form-group" className="row d-flex align-items-center vh-100">
                <form onSubmit={this.handleSubmit} className="mx-auto w-75" noValidate autoComplete="off">
                    <Input className="w-100" onChange={(e) => { this.setState({ Name: e.target.value }) }} placeholder="Name" inputProps={{ 'aria-label': 'description' }} /><br />
                    <Input className="w-100" onChange={(e) => { this.setState({ Password: e.target.value }) }}
                        placeholder="Password" inputProps={{ 'aria-label': 'description' }} /><br /><br />
                    <br />
                    <Button type="submit" color="primary">Login</Button>
                </form>
                <Modal
                    isOpen={this.state.modalIsOpen}
                    style={customStyles}
                    onRequestClose={this.closeModal}
                    contentLabel="Example Modal"
                >
                    <h2 ref={subtitle => this.subtitle = subtitle}>{this.state.errorMsg}</h2>
                    <button onClick={this.closeModal}>close</button>
             </Modal>
            </div>
        );
        
    }
    
    handleSubmit(event) {
        let cur = this;
        axios.post(HOST + "/login", {
            "name": this.state.Name,
            "password": this.state.Password,
        })
            .then((response) => {
                Cookies.set('jwt', response.data.access_token);
                Cookies.set('refresh-jwt', response.data.refresh_token);
                window.location.href='/planas';
            })
            .catch(function (error) {
                cur.setState({ error: true, errorMsg:error.message});
                cur.setState({modalIsOpen: true});
                
            });
        event.preventDefault();
    }

    openModal() {
        this.setState({modalIsOpen: true});
      }
    
     
      closeModal() {
        this.setState({modalIsOpen: false});
      }
}