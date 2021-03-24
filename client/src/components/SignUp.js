import React, {useState} from "react";
import axios from "axios";
import {Formik} from "formik";
import {Button, Card, Col, Form, Row, Alert} from "react-bootstrap";
import {Link, Redirect} from "react-router-dom";
import BreadcrumbWrapper from "./BreadcrumbWrapper";

export default function Signup() {
    const [isSubmitted, setSubmitted] = useState(false);
    const breadcrumbs = [
        {name: "Home", active: false, href: "/"},
        {name: "Sign up", active: true}
    ];

    const onSubmit = async (
        {email, identifier, name, password1, password2},
        actions
    ) => {
        const url = "/api/accounts/signup";
        try {
            var form_data = {
                email,
                name,
                password1: password1,
                password2: password2
            }
            if (identifier !== "") {
                form_data.identifier = identifier
            }
            await axios.post(url, form_data);
            setSubmitted(true);
        } catch (response) {
            const data = response.response.data;
            for (const value in data) {
                actions.setFieldError(value, data[value].join(" "));
            }
        }
    };

    if (isSubmitted) {
        return <Redirect to="/login" />;
    }

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper items={breadcrumbs} />
                <Card className="mb-3">
                    <Card.Header>Sign up</Card.Header>
                    <Card.Body>
                        <Formik
                            initialValues={{
                                email: "",
                                name: "",
                                password1: "",
                                password2: "",
                                identifier: ""
                            }}
                            onSubmit={onSubmit}
                        >
                            {({
                                errors,
                                handleChange,
                                handleSubmit,
                                isSubmitting,
                                setFieldValue,
                                values
                            }) => (
                                <>
                                    {"non_field_errors" in errors &&
                                        <Alert variant="danger">
                                            {errors["non_field_errors"]}
                                        </Alert>
                                    }
                                    <Form noValidate onSubmit={handleSubmit}>
                                        <Form.Group controlId="email">
                                            <Form.Control
                                                className={
                                                    "email" in errors
                                                        ? "is-invalid"
                                                        : ""
                                                }
                                                name="email"
                                                placeholder="Email"
                                                value={values.email}
                                                onChange={handleChange}
                                                autoComplete="email"
                                                required
                                            />
                                            {"email" in errors &&
                                                <Form.Control.Feedback type="invalid">
                                                    {errors.email}
                                                </Form.Control.Feedback>
                                            }
                                        </Form.Group>
                                        <Form.Group controlId="name">
                                            <Form.Control
                                                className={
                                                    "name" in errors
                                                        ? "is-invalid"
                                                        : ""
                                                }
                                                name="name"
                                                placeholder="Full name"
                                                value={values.name}
                                                onChange={handleChange}
                                                autoComplete="name"
                                                required
                                            />
                                            {"name" in errors &&
                                                <Form.Control.Feedback type="invalid">
                                                    {errors.name}
                                                </Form.Control.Feedback>
                                            }
                                        </Form.Group>
                                        <Row>
                                            <Col>
                                                <Form.Group controlId="password1">
                                                    <Form.Control
                                                        className={
                                                            "password1" in errors
                                                                ? "is-invalid"
                                                                : ""
                                                        }
                                                        name="password1"
                                                        type="password"
                                                        placeholder="Password"
                                                        value={values.password1}
                                                        onChange={handleChange}
                                                        autoComplete="new-password"
                                                        required
                                                    />
                                                    {"password1" in errors &&
                                                        <Form.Control.Feedback type="invalid">
                                                            {errors.password1}
                                                        </Form.Control.Feedback>
                                                    }
                                                </Form.Group>
                                            </Col>
                                            <Col>
                                                <Form.Group controlId="password2">
                                                    <Form.Control
                                                        className={
                                                            "password2" in errors
                                                                ? "is-invalid"
                                                                : ""
                                                        }
                                                        name="password2"
                                                        type="password"
                                                        placeholder="Confirm"
                                                        value={values.password2}
                                                        onChange={handleChange}
                                                        autoComplete="new-password"
                                                        required
                                                    />
                                                    {"password2" in errors &&
                                                        <Form.Control.Feedback type="invalid">
                                                            {errors.password2}
                                                        </Form.Control.Feedback>
                                                    }
                                                </Form.Group>
                                            </Col>
                                        </Row>
                                        <Form.Group controlId="identifier">
                                            <Form.Control
                                                className={
                                                    "identifier" in errors
                                                        ? "is-invalid"
                                                        : ""
                                                }
                                                name="identifier"
                                                placeholder="Optional: Student ID"
                                                value={values.identifier}
                                                onChange={handleChange}
                                            />
                                            {"identifier" in errors &&
                                                <Form.Control.Feedback type="invalid">
                                                    {errors.identifier}
                                                </Form.Control.Feedback>
                                            }
                                        </Form.Group>
                                        <Button
                                            block
                                            type="submit"
                                            variant="primary"
                                        >
                                            Sign Up
                                </Button>
                                    </Form>
                                </>
                            )}
                        </Formik>
                    </Card.Body>
                    <p className="mt-3 text-center">
                        Already signed up? <Link to="/login">Log in.</Link>
                    </p>
                </Card>
            </Col>
        </Row>
    );
}
