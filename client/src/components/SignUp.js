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
        {email, identifier, full_name, password1, password2},
        actions
    ) => {
        const url = "/api/accounts/signup";
        try {
            var form_data = {
                email,
                full_name,
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
                                full_name: "",
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
                                    {"non_field_errors" in errors && (
                                        <Alert variant="danger">
                                            {errors["non_field_errors"]}
                                        </Alert>
                                    )}
                                    <Form noValidate onSubmit={handleSubmit}>
                                        <Form.Group controlId="email">
                                            <Form.Control
                                                className={
                                                    "email" in errors
                                                        ? "is-invalid"
                                                        : ""
                                                }
                                                name="email"
                                                onChange={handleChange}
                                                values={values.email}
                                                placeholder={"Email"}
                                                required
                                            />
                                            {"email" in errors && (
                                                <Form.Control.Feedback type="invalid">
                                                    {errors.email}
                                                </Form.Control.Feedback>
                                            )}
                                        </Form.Group>
                                        <Form.Group controlId="full_name">
                                            <Form.Control
                                                className={
                                                    "full_name" in errors
                                                        ? "is-invalid"
                                                        : ""
                                                }
                                                name="full_name"
                                                onChange={handleChange}
                                                values={values.full_name}
                                                placeholder={"Full name"}
                                                required
                                            />
                                            {"full_name" in errors && (
                                                <Form.Control.Feedback type="invalid">
                                                    {errors.full_name}
                                                </Form.Control.Feedback>
                                            )}
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
                                                        onChange={handleChange}
                                                        type="password"
                                                        value={values.password1}
                                                        placeholder={"Password"}
                                                        required
                                                    />
                                                    {"password1" in errors && (
                                                        <Form.Control.Feedback type="invalid">
                                                            {errors.password1}
                                                        </Form.Control.Feedback>
                                                    )}
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
                                                        onChange={handleChange}
                                                        type="password"
                                                        value={values.password2}
                                                        placeholder={"Confirm"}
                                                        required
                                                    />
                                                    {"password2" in errors && (
                                                        <Form.Control.Feedback type="invalid">
                                                            {errors.password2}
                                                        </Form.Control.Feedback>
                                                    )}
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
                                                onChange={handleChange}
                                                value={values.identifier}
                                                placeholder={
                                                    "Optional: Student ID"
                                                }
                                            />
                                            {"identifier" in errors && (
                                                <Form.Control.Feedback type="invalid">
                                                    {errors.identifier}
                                                </Form.Control.Feedback>
                                            )}
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
