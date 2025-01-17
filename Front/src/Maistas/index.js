// eslint-disable-next-line
import React, { Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie'
import { HOST } from "../App"
// eslint-disable-next-line
import { Input, FormGroup, Label, ModalHeader, ModalBody, ModalFooter, Table, Button } from 'reactstrap';
import Select from "react-dropdown-select";
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

export class MaistasCreate extends React.Component {
    constructor(props) {
        super(props);
        let cur = this;
       
        let { id } = this.props.match.params;
        this.id = id;
        this.state = {
            data: false,
            pavadinimas: {},
            kcal: {},
            angliavandeniai: {},
            riebalai: {},
            sotiejiRiebalai: {},
            baltymai: {},
            kokybe: {},
            receptasId: {},
            test: {},
            receptai: [],

            msg: 'Kazkas blogai!',
            modalIsOpen: false,
            success: false,
            error: false
        };
        axios.get(HOST + "/receptas", {
            headers: { Authorization: `Bearer ${Cookies.get('jwt')}` }
        })
            .then((response) => {
                cur.setState({
                    receptai: response.data.receptas.map(item => {return {value: item.id, label: item.pavadinimas}})
                })
            })
            .catch(function () {
                cur.setState({ error: true });
            });
        this.handleSubmit = this.handleSubmit.bind(this);
        this.closeModal=this.closeModal.bind(this);
    }
 
    render() {
        return (
            <div class="form-group" className="row d-flex align-items-center">
                <form onSubmit={this.handleSubmit} className="mx-auto w-75" noValidate autoComplete="off">
                <label for="exampleInputEmail1">Pavadinimas</label>
                    <Input className="w-100"  onChange={(e) => { this.setState({ pavadinimas: e.target.value }) }}
                     placeholder="Pavadinimas" inputProps={{ 'aria-label': 'description' }} /><br />
                    <label for="exampleInputEmail1">kcal</label>
                    <Input className="w-100" type="number" onChange={(e) => { this.setState({ kcal: e.target.value }) }}
                     placeholder="kcal" inputProps={{ 'aria-label': 'description' }} /><br />
                    <label for="exampleInputEmail1">angliavandeniai</label>
                     <Input className="w-100" type="number" onChange={(e) => { this.setState({ angliavandeniai: e.target.value }) }}
                     placeholder="angliavandeniai" inputProps={{ 'aria-label': 'description' }} /><br />
                    <label for="exampleInputEmail1">riebalai</label>
                     <Input className="w-100" type="number" onChange={(e) => { this.setState({ riebalai: e.target.value }) }}
                     placeholder="riebalai" inputProps={{ 'aria-label': 'description' }} /><br />
                    <label for="exampleInputEmail1">sotieji Riebalai</label>
                     <Input className="w-100" type="number" onChange={(e) => { this.setState({ sotiejiRiebalai: e.target.value }) }}
                     placeholder="sotiejiRiebalai" inputProps={{ 'aria-label': 'description' }} /><br />
                    <label for="exampleInputEmail1">kokybe</label>
                    <Input className="w-100" type="number" onChange={(e) => { this.setState({ kokybe: e.target.value }) }}
                     placeholder="kokybe" inputProps={{ 'aria-label': 'description' }} /><br />
                    <label for="exampleInputEmail1">baltymai</label>
                    <Input className="w-100" type="number" onChange={(e) => { this.setState({ baltymai: e.target.value }) }}
                        placeholder="baltymai" inputProps={{ 'aria-label': 'description' }} /><br /><br />
                    <br />
                    <Select options={this.state.receptai} onChange={(values) => this.setState({receptasId: values})} />
                    <Button type="submit" color="primary">Sukurti nauja Maista</Button>
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
        let body =  {
            pavadinimas: this.state.pavadinimas,
            kcal: this.state.kcal,
            angliavandeniai: this.state.angliavandeniai,
            riebalai: this.state.riebalai,
            sotiejiRiebalai: this.state.sotiejiRiebalai,
            baltymai: this.state.baltymai,
            kokybe: this.state.kokybe,
            recepto_id: this.state.receptasId[0].value
        }
        
        axios.post(HOST + `/maistas`,JSON.stringify(body), {
            headers: { Authorization: `Bearer ${Cookies.get('jwt')}`,
            'Content-Type':'application/json' }
        })
            .then((response) => {
                cur.setState({
                    success: true,
                    msg: "Mistas buvo sekmingai sukurtas",
                    modalIsOpen: true
                })
            })
            .catch(function (errorData) {
                cur.setState({
                    error: true,
                    msg: errorData.response.message,
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