import React, { useState } from "react";
import { Button, Container, Form, Navbar } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { Link, Redirect, Route, Switch } from "react-router-dom";

import SignUp from "./components/SignUp";
import LogIn from "./components/LogIn";
import Dashboard from "./components/Dashboard";
import LectureList from "./components/LectureList";
import LectureDetail from "./components/LectureDetail";
import LessonDetail from "./components/LessonDetail";

import "./App.css";
import axios from "axios";

function App() {
    const [isLoggedIn, setLoggedIn] = useState(() => {
        return window.localStorage.getItem("homework.checker.auth") !== null;
    });
    const logIn = async (email, password) => {
        const url = "/api/accounts/login";
        try {
            const response = await axios.post(url, { email, password });
            window.localStorage.setItem(
                "homework.checker.auth",
                JSON.stringify(response.data)
            );
            setLoggedIn(true);
            return { response, isError: false };
        } catch (error) {
            console.log(error);
            return { response: error, isError: true };
        }
    };
    const logOut = () => {
        window.localStorage.removeItem("homework.checker.auth");
        setLoggedIn(false);
    };

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
                    {isLoggedIn && (
                        <Form inline className="ml-auto">
                            <Link
                                id="dashboard"
                                className="btn"
                                to="/dashboard"
                            >
                                Dashboard
                            </Link>
                            <Link id="lectures" className="btn" to="/lectures">
                                Vorlesungen
                            </Link>
                            <Button type="button" onClick={() => logOut()}>
                                Abmelden
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
                                {!isLoggedIn && (
                                    <Link
                                        id="signUp"
                                        className="btn btn-primary mx-2"
                                        to="/signup"
                                    >
                                        Registrieren
                                    </Link>
                                )}
                                {!isLoggedIn && (
                                    <Link
                                        id="logIn"
                                        className="btn btn-primary mx-2"
                                        to="/login"
                                    >
                                        Anmelden
                                    </Link>
                                )}
                            </div>
                        )}
                    />
                    <Route
                        path="/signup"
                        render={() =>
                            isLoggedIn ? <Redirect to="/" /> : <SignUp />
                        }
                    />
                    <Route
                        path="/login"
                        render={() =>
                            isLoggedIn ? (
                                <Redirect to="/" />
                            ) : (
                                <LogIn logIn={logIn} />
                            )
                        }
                    />
                    <Route
                        path="/dashboard/"
                        render={() =>
                            isLoggedIn ? <Dashboard /> : <Redirect to="/" />
                        }
                    />
                    <Route
                        path="/lectures/:lecture_slug/:lesson_slug/"
                        render={() =>
                            isLoggedIn ? <LessonDetail /> : <Redirect to="/" />
                        }
                    />
                    <Route
                        path="/lectures/:lecture_slug/"
                        render={() =>
                            isLoggedIn ? <LectureDetail /> : <Redirect to="/" />
                        }
                    />
                    <Route
                        path="/lectures/"
                        render={() =>
                            isLoggedIn ? <LectureList /> : <Redirect to="/" />
                        }
                    />
                </Switch>
            </Container>
        </>
    );
}

export default App;
