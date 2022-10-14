import './App.css';
import React from 'react';
import ApexChart from './Chart'

// import data from './data_.json'

class App extends React.Component {
  state = {data: null, count: 0}

  componentDidMount() {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/ami')
    ws.onmessage = this.onMessage

    // this.setState({
    //   ws: ws,
    //   // Create an interval to send echo messages to the server
    //   interval: setInterval(() => ws.send('echo'), 1000)
    // })
  }

  componentWillUnmount() {
    const {ws, interval} = this.state;
    // ws.close()
    clearInterval(interval)
  }

  onMessage = (ev) => {
    const recv = JSON.parse(ev.data)
    const {data, count} = this.state
    // let newData = [...data]
    // // Remove first data if we received more than 20 values
    // if (count > 20) {
    //   newData = newData.slice(1)
    // }

    console.log(recv);
    if(recv.result == null || recv.result == undefined){
      // console.log("no");
    }else{
    this.setState({data: recv, count: count + 1})
    }
  }

  

  render() {
    // console.log(this.state.data);
    // return null
    return <div>
      <p>PinePy</p>
      {this.state.data && <ApexChart data={this.state.data}/>}
    </div>
  }
}

export default App;
