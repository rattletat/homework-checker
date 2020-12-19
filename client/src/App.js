import React, { useEffect, useState } from "react";
import { Button, Container, Form, Navbar } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { Link, Redirect, Route, Switch } from "react-router-dom";

import { logIn, logOut, isLoggedIn } from "./services/AuthService";

import SignUp from "./components/SignUp";
import LogIn from "./components/LogIn";
import Dashboard from "./components/Dashboard";
import Profile from "./components/Profile";
import LectureList from "./components/LectureList";
import LectureDetail from "./components/LectureDetail";
import LessonDetail from "./components/LessonDetail";

import "./App.css";

function App() {
    const [loggedIn, setLoggedIn] = useState(false);

    useEffect(() => {
        setLoggedIn(isLoggedIn());
    });

    return (
        <>
            <Navbar bg="light" expand="sm" variant="light">
                <LinkContainer to="/">
                    <Navbar.Brand className="logo">
                        Homework Checker
                    </Navbar.Brand>
                </LinkContainer>
                <Navbar.Toggle />
                <Navbar.Collapse>
                    {loggedIn && (
                        <Form inline className="ml-auto">
                            <Link
                                id="dashboard"
                                className="btn"
                                to="/dashboard"
                            >
                                Dashboard
                            </Link>
                            <Link
                                id="profile"
                                className="btn"
                                to="/profile"
                            >
                                Profile
                            </Link>
                            <Link id="lectures" className="btn" to="/lectures">
                                Lectures
                            </Link>
                            <Button type="button" onClick={() => logOut()}>
                                Log out
                            </Button>
                        </Form>
                    )}
                </Navbar.Collapse>
            </Navbar>
            <Container className="pt-3">
                <Switch>
                    <Route
                        exact
                        path="/"
                        render={() => (
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
                        )}
                    />
                    <Route
                        path="/signup"
                        render={() =>
                            loggedIn ? <Redirect to="/" /> : <SignUp />
                        }
                    />
                    <Route
                        path="/login"
                        render={() =>
                            loggedIn ? (
                                <Redirect to="/" />
                            ) : (
                                <LogIn
                                    logIn={(email, password) =>
                                        logIn(email, password, setLoggedIn)
                                    }
                                />
                            )
                        }
                    />
                    <Route
                        path="/dashboard/"
                        render={() =>
                            loggedIn ? <Dashboard /> : <Redirect to="/" />
                        }
                    />
                    <Route
                        path="/profile/"
                        render={() =>
                            loggedIn ? <Profile /> : <Redirect to="/" />
                        }
                    />
                    <Route
                        path="/lectures/:lecture_slug/:lesson_slug/"
                        render={() =>
                            loggedIn ? <LessonDetail /> : <Redirect to="/" />
                        }
                    />
                    <Route
                        path="/lectures/:lecture_slug/"
                        render={() =>
                            loggedIn ? <LectureDetail /> : <Redirect to="/" />
                        }
                    />
                    <Route
                        path="/lectures/"
                        render={() =>
                            loggedIn ? <LectureList /> : <Redirect to="/" />
                        }
                    />
                </Switch>
            </Container>
        </>
    );
}

export default App;
