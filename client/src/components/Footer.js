import React from "react";
import {Link} from "react-router-dom";


export default function Footer() {
    return <footer className="row text-light bg-light">
        <div className="col col-4 text-center">
            <Link
                id="about"
                title="contact information"
                className="btn"
                to="/about/"
            >
                <small>about</small>
            </Link>
        </div>

        <div className="col col-4 text-center">
            <Link to={{pathname: "https://github.com/rattletat/homework-checker"}}
                id="source"
                className="btn"
                title="source repository"
                target="_blank"
            >
                <small>source</small>
            </Link>
        </div>

        <div className="col col-4 text-center">
            <Link
                id="profile"
                title="privacy statement"
                className="btn"
                to="/privacy/"
            >
                <small>privacy</small>
            </Link>
        </div>
    </footer>
}
