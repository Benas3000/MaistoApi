// eslint-disable-next-line
import React, { Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie'
import { HOST } from "../App"
// eslint-disable-next-line
import {  FormGroup, Label, ModalHeader, ModalBody, ModalFooter, Table } from 'reactstrap';
import Select from "react-dropdown-select"
import Modal from 'react-modal'
import Input from "@material-ui/core/Input"
import Button from "@material-ui/core/Button"
import Paper from "@material-ui/core/Paper"
import TableCell from "@material-ui/core/TableCell"
import TableRow from "@material-ui/core/TableRow"
import TableHead from "@material-ui/core/TableHead"
import TableBody from "@material-ui/core/TableBody"
import Helmet from "react-helmet"
import {  getSession } from '../Register'

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

export class ReceptasCreate extends React.Component {
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
            plano_id: {},

            planai: [],

            msg: 'Kazkas blogai!',
            modalIsOpen: false,
            success: false,
            error: false
        };
        axios.get(HOST + "/planas", { //Pakeisti i receptas kai pataisysiu baack
            headers: { Authorization: `Bearer ${Cookies.get('jwt')}` }
        })
            .then((response) => {
                cur.setState({
                    planai: response.data.planas.map(item => {return {value: item.id, label: item.pavadinimas}})
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
            <div class="form-group" className="row d-flex align-items-center ">
                <form onSubmit={this.handleSubmit} className="mx-auto w-75" noValidate autoComplete="off">
                    <Input className="w-100"  onChange={(e) => { this.setState({ pavadinimas: e.target.value }) }}
                     placeholder="Pavadinimas" inputProps={{ 'aria-label': 'description' }} /><br />
                    <label for="exampleInputEmail1">Pavadinimas</label>
                    <Input className="w-100" type="number" onChange={(e) => { this.setState({ kcal: e.target.value }) }}
                     placeholder="kcal" inputProps={{ 'aria-label': 'description' }} /><br />
<label for="exampleInputEmail1">kcal</label>
                     <Input className="w-100" type="number" onChange={(e) => { this.setState({ angliavandeniai: e.target.value }) }}
                     placeholder="angliavandeniai" inputProps={{ 'aria-label': 'description' }} /><br />
<label for="exampleInputEmail1">angliavandeniai</label>
                     <Input className="w-100" type="number" onChange={(e) => { this.setState({ riebalai: e.target.value }) }}
                     placeholder="riebalai" inputProps={{ 'aria-label': 'description' }} /><br />
<label for="exampleInputEmail1">riebalai</label>
                     <Input className="w-100" type="number" onChange={(e) => { this.setState({ sotiejiRiebalai: e.target.value }) }}
                     placeholder="sotiejiRiebalai" inputProps={{ 'aria-label': 'description' }} /><br />
<label for="exampleInputEmail1">sotiejiRiebalai</label>
                    <Input className="w-100" type="number" onChange={(e) => { this.setState({ kokybe: e.target.value }) }}
                     placeholder="kokybe" inputProps={{ 'aria-label': 'description' }} /><br />
<label for="exampleInputEmail1">kokybe</label>
                    <Input className="w-100" type="number" onChange={(e) => { this.setState({ baltymai: e.target.value }) }}
                        placeholder="baltymai" inputProps={{ 'aria-label': 'description' }} /><br /><br />
                    <br />
                    <Select options={this.state.planai} onChange={(values) => this.setState({plano_id: values})} />
                    <Button type="submit" color="primary">Sukurti nauja recepta</Button>
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
        axios.post(HOST + `/receptas`, JSON.stringify({
            pavadinimas: this.state.pavadinimas,
            kcal: this.state.kcal,
            angliavandeniai: this.state.angliavandeniai,
            riebalai: this.state.riebalai,
            sotiejiRiebalai: this.state.sotiejiRiebalai,
            baltymai: this.state.baltymai,
            kokybe: this.state.kokybe,
            plano_id: this.state.plano_id[0].value

        }), {
            headers: { Authorization: `Bearer ${Cookies.get('jwt')}`,
            'Content-Type':'application/json' }
        })
            .then((response) => {
                cur.setState({
                    success: true,
                    msg: "Receptas buvo sekmingai sukurtas",
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


export class ReceptaiList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: false,
        };
        let cur = this;
        let { id } = this.props.match.params;
        this.id = id;
        axios.get(HOST + `/planas/${id}/receptas`, {
            headers: { Authorization: "Bearer " + Cookies.get('jwt') ,
            'Content-Type':'application/json' }
        })
            .then((response) => {
                cur.setState({
                    data: response.data.planas
                    
                })
            })
            .catch(function (errorData) {
                cur.setState({ error: true});
            });
    }

    render() {
        return (<div className="row d-flex align-items-center vh-100">
            <Helmet>
                <title>Receptai</title>
                <meta name='description' content='Receptai' />
            </Helmet>
            {this.state.data && (
                <Paper className="col-12">
                    <Table aria-label="Receptas">
                        <TableHead>
                            <TableRow>
                                <TableCell>Pavadinimas</TableCell>
                                <TableCell align="right">kcal</TableCell>
                                <TableCell align="right">angliavandeniai</TableCell>
                                <TableCell align="right">riebalai</TableCell>
                                <TableCell align="right">Sotieji riebalai</TableCell>
                                <TableCell align="right">kokybe</TableCell>
                                <TableCell align="right">baltymai</TableCell>
                                {getSession().role===2 ?
                                <React.Fragment>
                                <TableCell align="right">delete</TableCell>
                                </React.Fragment>
                                :null}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {this.state.data.map(row => (
                                <TableRow key={row.pavadinimas}>
                                    <TableCell component="th" scope="row">
                                        {row.pavadinimas}
                                    </TableCell>
                                    <TableCell align="right">{row.kcal}</TableCell>
                                    <TableCell align="right">{row.angliavandeniai}</TableCell>
                                    <TableCell align="right">{row.riebalai}</TableCell>
                                    <TableCell align="right">{row.sotiejiRiebalai}</TableCell>
                                    <TableCell align="right">{row.kokybe}</TableCell>
                                    <TableCell align="right">{row.baltymai}</TableCell>
                                    {getSession().role<2 ?
                                    <React.Fragment>
                                    <TableCell align="right"><Button variant="contained" onClick={() => this.delete(row.id)}>delete</Button></TableCell>
                                    </React.Fragment>
                                    :null}
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Paper>
            )}</div>);
    }
    delete(id) {
        let cur = this;
        axios.delete(HOST + `/planas/${cur.id}/receptas/${id}`, {
            headers: { Authorization: "Bearer " + Cookies.get('jwt'),
            'Content-Type':'application/json' }
        })
            .then((response) => {
                window.location.reload();
            })
            .catch(function (errorData) {
                if (cur.state.error === false) {
                    cur.setState({ error: true });
                }
            });
    }
}

export class ViewReceptai extends React.Component {
    constructor(props) {
        super(props);
        let cur = this;
       
        let { id } = this.props.match.params;
        this.id = id;
        this.state = {
            data: false,

            planai: [],
            plano_id: {},

            msg: 'Kazkas blogai!',
            modalIsOpen: false,
            success: false,
            error: false
        };
        axios.get(HOST + "/planas", { //Pakeisti i receptas kai pataisysiu baack
            headers: { Authorization: `Bearer ${Cookies.get('jwt')}` }
        })
            .then((response) => {
                cur.setState({
                    planai: response.data.planas.map(item => {return {value: item.id, label: item.pavadinimas}})
                })
            })
            .catch(function () {
                cur.setState({ error: true });
            });

            this.rodydti = this.rodydti.bind(this);
    }
 
    render() {
        return (
            <div class="form-group" className="row d-flex align-items-center ">
                <form onSubmit={this.rodydti} className="mx-auto w-75" noValidate autoComplete="off">
                    <label for="exampleInputEmail1">Pasirinktie plana kurio receptus noreite pamatyti</label>
                    <Select options={this.state.planai} onChange={(values) => this.setState({plano_id: values})} />
                    <Button type="submit" color="blue">Žiurėti plano receptus</Button>
                </form>
            </div>
        );
    }

    rodydti(event){
        let cur = this
        window.location.href = `/planas/${cur.state.plano_id[0].value}/receptas`;
        event.preventDefault();
    }

}