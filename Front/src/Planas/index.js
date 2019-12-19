// eslint-disable-next-line
import React, { Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie'
import { HOST } from "../App"
// eslint-disable-next-line
import { Input, FormGroup, Label, ModalHeader, ModalBody, ModalFooter, Table, Button } from 'reactstrap';
import Modal from 'react-modal';

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

export class PlanasCreate extends React.Component {
    constructor(props) {
        super(props);
       
        let { id } = this.props.match.params;
        this.id = id;
        this.state = {
            data: false,
            pavadinimas: {},
            Komentaras: {},
            ivertinimas: 1,
            error: false,
            msg: 'Suveskite visus laukus',
            modalIsOpen: false,
            success: false,
        };
        
        this.handleSubmit = this.handleSubmit.bind(this);
        this.closeModal=this.closeModal.bind(this);
    }
 
    render() {
        return (
            <div class="form-group" className="row d-flex align-items-center vh-100">
                <form onSubmit={this.handleSubmit} className="mx-auto w-75" noValidate autoComplete="off">
                <label for="exampleInputEmail1">Pavadinimas</label>
                    <Input className="w-100" onChange={(e) => { this.setState({ pavadinimas: e.target.value }) }} placeholder="Pavadinimas" inputProps={{ 'aria-label': 'description' }} /><br />
                    <label for="exampleInputEmail1">Ivertinimas</label>
                    <Input className="w-100" onChange={(e) => { this.setState({ ivertinimas: e.target.value }) }}
                        placeholder="ivertinimas" type="number" inputProps={{ 'aria-label': 'description' }} /><br /><br />
                        <label for="exampleInputEmail1">Ivertinimas</label>
                     <Input className="w-100" onChange={(e) => { this.setState({ Komentaras: e.target.value }) }} placeholder="Komentaras" inputProps={{ 'aria-label': 'description' }} /><br />
                    <br />
                    <Button type="submit" color="primary">Sukurti plana</Button>
                </form>
                <Modal
                    isOpen={this.state.modalIsOpen}
                    style={customStyles}
                    onRequestClose={this.closeModal}
                    contentLabel="Example Modal">
                    <h2 ref={subtitle => this.subtitle = subtitle}>{this.state.msg}</h2>
                    <button onClick={this.closeModal}>close</button>
             </Modal>
            </div>
        );
    }
    //bbs=()=>{}
    handleSubmit(event) {
        let cur = this;
        axios.post(HOST + `/planas`, JSON.stringify({

            pavadinimas: this.state.pavadinimas,
            Komentaras: this.state.Komentaras,
            ivertinimas: this.state.ivertinimas
        }), {
            headers: { Authorization: `Bearer ${Cookies.get('jwt')}`, 
        'Content-Type':'application/json' }
        })
            .then((response) => {
                cur.setState({
                    success: true,
                    msg: "Planas sekmingai idetas",
                    modalIsOpen: true
                })
            })
            .catch(function (errorData) {
                cur.setState({
                    error: true,
                    meg: errorData.response.message,
                    modalIsOpen: true
                })

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


