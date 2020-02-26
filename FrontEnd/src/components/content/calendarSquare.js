import React, { Component } from "react";

export default class CalendarSquare extends Component {
    constructor() {
        super()

        this.state = {
            value: "",
            postID: undefined
        }

        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    componentDidMount() {
        if (this.props.month && this.props.year) {
            this.queryAPI()
        }
    }

    componentDidUpdate(prevProps) {
        if (prevProps.month != this.props.month) {
            this.queryAPI()
        }
    }

    queryAPI() {
        fetch(`https://md-react-calendar-api.herokuapp.com/calendar-inputs/${this.props.date}/${this.props.month}/${this.props.year}`,{
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {
            // console.log(data)
            if (data.content) {
                this.setState({
                    // value: data[1],
                    // postID: data[0]
                    // marshmallow below,
                    value: data.content,
                    postID: data.id
            })
            }
            else {
                this.setState({
                    value: "", 
                    postExists: false
                })
            }
        })
        .catch(error => console.log(error))
    }

    handleChange(event) {
        this.setState({
            value: event.target.value
        })
    }

    handleSubmit() {
        let url
        let method
        let shouldRun = true

        if (this.state.value.length > 0 && this.state.postID == undefined) {
            url = "https://md-react-calendar-api.herokuapp.com/calendar-input/post"
            method = "POST"
        }
        else if (this.state.value.lenth > 0 && this.state.postID) {
            url = `https://md-react-calendar-api.herokuapp.com/calendar-inputs/update/${this.state.postID}`
            method = "PUT"
        }
        else if (this.state.value.length == 0 && this.state.postID) {
            url = `https://md-react-calendar-api.herokuapp.com/calendar-inputs/delete/${this.state.postID}`
            method = "DELETE"
        }
        else {
            shouldRun =false
        }

        if (shouldRun = true) {
            fetch(url, {
                method: method, 
                headers: {
                    "content-type": "application/json"
                },
                body: JSON.stringify({
                    content: this.state.value,
                    date: this.props.date,
                    month: this.props.month,
                    year: this.props.year
                }) 
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.log(error)) 
        }
    }

    render() {
        return(
            <div className={`calendar-square ${this.props.inactive ? "overflow-day" : ""}`}>
                <div>{this.props.date}</div>
                <div className="colorMe"></div>
                <input 
                    type="text" 
                    value={this.state.value} 
                    onChange={this.handleChange}
                    onBlur={this.handleSubmit}
                    disabled={this.props.inactive ? true : false} 
                    />
            </div>
        )
    }
}