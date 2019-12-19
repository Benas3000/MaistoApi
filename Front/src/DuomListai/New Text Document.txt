// eslint-disable-next-line
import React, { Component } from 'react';
// eslint-disable-next-line
import { Input, FormGroup, Label, ModalHeader, ModalBody, ModalFooter, Table, Button } from 'reactstrap';
import {HOST } from '../App'
import axios from 'axios'
import Cookies from 'js-cookie'

export const FoodItem = (props) => {
    return (
        <div className='container'>
            <div className='row'>
                <h2>{props.pavadinimas}</h2>
            </div>
            <div className='row'>
                <dt className="col-sm-3">Kalories</dt>
                <dd className="col-sm-9">{props.kcal}</dd>

                <dt className="col-sm-3">Carbs</dt>
                <dd className="col-sm-9">{props.angliavandeniai}        </dd>

                <dt className="col-sm-3">Fats</dt>
                <dd className="col-sm-9">{props.fats}</dd>

                <dt className="col-sm-3 text-truncate">Saturated fats</dt>
                <dd className="col-sm-9">{props.sotiejiRiebalai}</dd>

                <dt className="col-sm-3 text-truncate">Rating</dt>
                <dd className="col-sm-9">{props.kokybe}</dd>

                <dt className="col-sm-3 text-truncate">Baltymai</dt>
                <dd className="col-sm-9">{props.baltymai}</dd>

            </div>
            <hr  />
        </div>
    )
}
export const mapList = (Component, data) => {
    return data.map((item, index) => {
        return <Component {...item} key={index} />
    })
}

export default class Listai extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            data: false,
            showPlanai: false,
            showReceptai: false,
            showMaistai: false,

            planasid: {},
            receptasid: {},
            maistasid: {},

            planai: [],
            receptai: [],
            maistai: [],

            msg: 'Kazkas blogai!',
            modalIsOpen: false,
            success: false,
            error: false
        };
        let cur = this; 
        axios.get(HOST + "/receptas", {
            headers: { Authorization: `Bearer ${Cookies.get('jwt')}` }
        })
            .then((response) => {
                cur.setState({
                    maistai: response.data.receptas
                })
            })
            .catch(function () {
                cur.setState({ error: true });
            });
    }
    render() {
        return (
            <div>
                <div className="row d-flex align-items-center"  >
                    <h1 className=' position-absolute w-100 text-center display-1 font-bold text-white'
                        style={{ transform: 'translate(-50%, -50%)', top: '50%', left: '50%' }}>Receptai ir Dienos Mitybos Planai</h1>
                    <img className="img-fluid mx-auto" src="https://png.pngtree.com/thumb_back/fw800/back_our/20190621/ourmid/pngtree-black-meat-western-food-banner-background-image_194600.jpg" />
                </div>
                <div className="container"  >
                    <h1>Receptai</h1>
                </div>
                <div className="container"  >
                    {mapList(FoodItem, this.state.maistai)}
                </div>
            </div>
        );
    }
}

