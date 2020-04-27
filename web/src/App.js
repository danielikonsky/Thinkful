import React, { Component } from 'react';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {init:[]};

    this.fetchToday();
    this.fetchInit();

    this.handleChange = this.handleChange.bind(this);

    }

  async fetchToday() {
    try {
      const res = await fetch("http://localhost:4433/today");
      const json = await res.json();
      this.setState({today: json.today});
    } catch (e) {
      console.error("Failed to fetch 'today' data", e);
    }
  }

  async fetchInit() {
    try {

      const res = await fetch("http://localhost:4433/init");
      const json = await res.json();
      this.setState({init: json.init});

    } catch (e) {
      console.error("Failed to fetch 'init' data", e);
    }
  }

  async fetchBook(advisorkey) {

    var namefield = document.getElementById('namefield').value;

    if (namefield.length === 0)
      {
         alert("Please enter Student Name")
       }
    else {

        try {

          const res = await fetch("http://localhost:4433/init?advisorkey=" + advisorkey + "&namefield="+namefield);
          const json = await res.json();
          this.setState({init: json.init});

        } catch (e) {
          console.error("Failed to fetch 'book' data", e);
        }
      }
    }

  handleChange(event) {
    this.setState({namefield: event.target.value});
  }

  renderAvailabilityData() {

      return this.state.init.filter(student => student.Student === '').map((InitSpots, index) => {

         const { AdvisorKey, AdvisorId, TimeSpot } = InitSpots
         return (
            <tr key={AdvisorKey}>
              <td>{AdvisorId}</td>
              <td>{TimeSpot}</td>
              <td>
                  <input type="hidden" value={AdvisorKey} id = "advisorkey" name="advisorkey"></input>
                  <input type="hidden" value={this.state.namefield} id = "namefield" name="namefield"></input>
                  <button className="book btn-small btn-primary" onClick={() => this.fetchBook(AdvisorKey)}> Book  </button>
              </td>
            </tr>
         )
      })
   }

   renderBookData() {

     return this.state.init.filter(student => student.Student !== '').map((InitSpots, index) => {

        const { AdvisorKey, AdvisorId, TimeSpot, Student } = InitSpots
        return (
           <tr key={AdvisorKey}>
             <td>{AdvisorId}</td>
             <td>{Student}</td>
             <td>{TimeSpot}</td>
           </tr>
        )
     })
    }

  render() {

      return (
                    <div className="App container">
                    <h1>Book Time with an Advisor</h1>
                    {this.state.today && <span id="today">Today is {this.state.today}.</span>}

                    <form id="name-form" className="col-md-6">
                      <div className="form-group">
                        <label htmlFor="name-field">Your Name</label>
                        <input type="text" value={this.state.namefield} name="namefield" className="form-control" onChange={this.handleChange} />
                      </div>
                    </form>

                       <h2 id='title'>Available Times</h2>
                       <table className="advisors table">
                       <thead>
                         <tr>
                           <th>Advisor ID</th>
                           <th>Availabilities</th>
                         </tr>
                       </thead>
                          <tbody>
                             {this.renderAvailabilityData()}
                          </tbody>
                       </table>

                       <h2 id='title'>Booked Times</h2>
                        <table className="bookings table">
                        <thead>
                          <tr>
                            <th>Advisor ID</th>
                            <th>Student Name</th>
                            <th>Date/Time</th>
                          </tr>
                        </thead>
                           <tbody>
                              {this.renderBookData()}
                           </tbody>
                        </table>

                     </div>
        )
    }
}
export default App;
