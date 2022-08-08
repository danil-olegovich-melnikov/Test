import './App.css';
import logo from './static/img/logo.png';
import React from 'react';
import axios from 'axios';
import {CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis} from 'recharts';

class App extends React.Component {
    state = {
        orders: [],
        total: 0,
    }

    componentDidMount() {
        axios.get(`http://127.0.0.1:8000/order/`)
            .then(res => {
                const orders = res.data;
                this.setState({orders});
            })
    }

    findSum() {
        const result = this.state.orders.reduce((total, currentValue) => total = total + currentValue.cost_dollar, 0);
        return result
    }

    renderTable() {
        if (this.state.orders.length > 0) {
            return this.state.orders.map(order => {
                return <tr>
                    <td>{order.number}</td>
                    <td>{order.order_number}</td>
                    <td>{order.cost_dollar}</td>
                    <td>{order.delivery_date}</td>
                    <td>{order.cost_rubles}</td>
                </tr>
            })
        }
    }

    render() {
        return (
            <div className="App">
                <header>
                    <img className="logo" src={logo} alt=""/>
                    <h2>Канал сервис</h2>
                </header>
                <div className="row">
                    <div className="col">
                        <LineChart width={650} height={400} data={this.state.orders}>
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="delivery_date"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend/>
                            <Line type="monotone" dataKey="cost_dollar" stroke="#8884d8" activeDot={{r: 8}}/>
                        </LineChart>
                    </div>
                    <div className="col">
                        <div className="total">
                            <h3 className="total-h3">TOTAL</h3>
                            <p className="total-p">{this.findSum()}</p>
                        </div>
                        <div>
                            <table className="table">
                                <thead>
                                <tr>
                                    <th>№</th>
                                    <th>заказ №</th>
                                    <th>стоимость,$</th>
                                    <th>срок поставки</th>
                                    <th>стоимость в руб.</th>
                                </tr>
                                </thead>
                                <tbody>
                                {this.renderTable()}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
