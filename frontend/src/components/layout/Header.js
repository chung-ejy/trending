import React, { Component } from 'react'

export class Header extends Component {
    render() {
        return (
            <nav class="navbar navbar-expand-lg item-center navbar-dark bg-danger">
                <div class="container-fluid">
                    <a class="navbar-brand mx-auto" href="#">Youtube Trends</a>
                </div>
            </nav>
        )
    }
}

export default Header
