import React, {useState} from "react";
import {Button, Container, Nav, Navbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";
import {Link, Redirect, Route, Switch} from "react-router-dom";

import {logIn, logOut, isLoggedIn} from "./services/AuthService";

import SignUp from "./components/SignUp";
import LogIn from "./components/LogIn";
import Lectures from "./components/Lectures";
import Profile from "./components/Profile";
import LectureDetail from "./components/LectureDetail";
import LessonDetail from "./components/LessonDetail";
import FlatPage from "./components/FlatPage";
import Footer from "./components/Footer";

import "./css/App.css";

function App() {
    const [loggedIn, setLoggedIn] = useState(isLoggedIn());

    return (
        <>
            <Navbar bg="light" expand="sm" variant="light">
                <LinkContainer to="/">
                    <Navbar.Brand className="logo">
                        Homework Checker
        </Navbar.Brand>
                </LinkContainer>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    {loggedIn &&
                        <Nav className="ml-auto">
                            <Nav.Link
                                id="lectures"
                                className="btn"
                                as={Link}
                                to="/lectures/"
                            >
                                Lectures
            </Nav.Link>
                            <Nav.Link
                                id="profile"
                                className="btn"
                                as={Link}
                                to="/profile/"
                            >
                                Profile
            </Nav.Link>
                            <Nav.Link id="logout"
                                className="text-white"
                                variant="primary"
                                as={Button}
                                onClick={() => logOut()}>
                                Log out
            </Nav.Link>
                        </Nav>
                    }
                </Navbar.Collapse>
            </Navbar>
            <Container className="pt-3">
                <Switch>
                    <Route
                        exact
                        path="/"
                    >
                        <div className="middle-center">
                            <h1 className="landing logo">
                                Homework Checker
        </h1>
                            {!loggedIn && (
                                <Link
                                    id="signUp"
                                    className="btn btn-primary mx-2"
                                    to="/signup"
                                >
                                    Sign up
                                </Link>
                            )}
                            {!loggedIn && (
                                <Link
                                    id="logIn"
                                    className="btn btn-primary mx-2"
                                    to="/login"
                                >
                                    Log in
                                </Link>
                            )}
                        </div>
                    </Route>
                    <Route
                        path="/signup"
                    >
                        {loggedIn ? <Redirect to="/" /> : <SignUp />}
                    </Route>
                    <Route
                        path="/login"
                    >
                        {loggedIn ? (
                            <Redirect to="/" />
                        ) : (
                            <LogIn
                                logIn={(email, password) =>
                                    logIn(email, password, setLoggedIn)
                                }
                            />
                        )}
                    </Route>
                    <Route
                        path="/profile/"
                    >
                        {loggedIn ? <Profile /> : <Redirect to="/" />}
                    </Route>
                    <Route
                        path="/lectures/:lecture_slug/:lesson_slug/"
                    >
                        {loggedIn ? <LessonDetail /> : <Redirect to="/" />}
                    </Route>
                    <Route
                        path="/lectures/:lecture_slug/"
                    >
                        {loggedIn ? <LectureDetail /> : <Redirect to="/" />}
                    </Route>
                    <Route
                        path="/lectures/"
                    >
                        {loggedIn ? <Lectures /> : <Redirect to="/" />}
                    </Route>
                    <Route
                        path="/privacy/"
                    >
                        <FlatPage name={"privacy"} />
                    </Route>
                    <Route
                        path="/about/"
                    >
                        <FlatPage name={"about"} />
                    </Route>
                </Switch>
            </Container>
            <Footer />
        </>
    );
}

export default App;
