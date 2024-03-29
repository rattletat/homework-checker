import React from "react";
import { Alert, Button, Form, Row, Col } from "react-bootstrap";
import { Formik } from "formik";
import { callAPI } from "../services/APIServices";

export default function LectureRegister({ refreshPage }) {
  const onSubmit = async (values, actions) => {
    if (values.code) {
      try {
        const response = await callAPI(
          `/api/lectures/register/${values.code}`,
          "POST"
        );
        if (response.status === 404 || response.status === 409) {
          const data = response.data;
          for (const value in data) {
            actions.setFieldError(value, data[value]);
          }
        } else {
          refreshPage();
          actions.resetForm();
        }
      } catch (error) {
        console.log(error);
      }
    } else {
      actions.setFieldError(
        "non_field_errors",
        "Please provide a registration code!"
      );
    }
  };

  return (
    <Formik
      initialValues={{
        code: "",
      }}
      onSubmit={onSubmit}
    >
      {({ errors, handleChange, handleSubmit, isSubmitting, values }) => (
        <>
          {"non_field_errors" in errors && (
            <Alert variant="danger">{errors["non_field_errors"]}</Alert>
          )}
          {"detail" in errors && (
            <Alert variant="danger">{errors["detail"]}</Alert>
          )}
          <Form noValidate onSubmit={handleSubmit}>
            <Row>
              <Col md={8}>
                <Form.Group controlId="code">
                  <Form.Control
                    className={"code" in errors ? "is-invalid" : ""}
                    name="code"
                    placeholder="Registration code"
                    value={values.code}
                    onChange={handleChange}
                    autoComplete="off"
                    required
                  />
                  {"code" in errors && (
                    <Form.Control.Feedback type="invalid">
                      {errors.code}
                    </Form.Control.Feedback>
                  )}
                </Form.Group>
              </Col>
              <Col md={4}>
                <Button
                  block
                  disabled={isSubmitting}
                  type="submit"
                  variant="primary"
                >
                  Add
                </Button>
              </Col>
            </Row>
          </Form>
        </>
      )}
    </Formik>
  );
}
