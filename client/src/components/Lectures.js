import React, { useEffect, useState } from "react";
import { Col, Row, ListGroup } from "react-bootstrap";
import BreadcrumbWrapper from "./BreadcrumbWrapper";
import { callAPI } from "../services/APIServices";
import LectureEntry from "./LectureEntry";
import LectureRegister from "./LectureRegister";

export default function Lectures() {
  const breadcrumbs = [
    { name: "Home", active: false, href: "/" },
    { name: "Lectures", active: true },
  ];
  const [updated, setUpdated] = useState(true);
  const [lectures, setLectures] = useState([]);

  useEffect(() => {
    const fetchAccountStatus = async () => {
      const response = await callAPI(`/api/lectures/`, "GET");
      if (response) {
        setLectures(response.data);
      }
    };
    fetchAccountStatus();
    setUpdated(true);
  }, [updated]);

  return (
    <Row>
      <Col lg={12}>
        <BreadcrumbWrapper items={breadcrumbs} />
        <h1>Lectures</h1>
        You can find information about lectures you are enrolled in below.
        {lectures.length && (
          <>
            <br />
            <br />
            <ListGroup>
              {lectures.map((lecture, key) => (
                <LectureEntry lecture={lecture} key={key} />
              ))}
            </ListGroup>
          </>
        )}
        <br />
        <h3>Add lecture</h3>
        <LectureRegister refreshPage={() => setUpdated(false)} />
      </Col>
    </Row>
  );
}
