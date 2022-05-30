import React from "react";
import ReactMarkdown from "react-markdown";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { dracula } from "react-syntax-highlighter/dist/esm/styles/prism";

import TeX from "@matejmazur/react-katex";
import "katex/dist/katex.min.css";

import gfm from "remark-gfm";
import math from "remark-math";
import smartypants from "@silvenon/remark-smartypants";
import footnotes from "remark-footnotes";

const _renderers = {
  inlineMath: ({ value }) => <TeX math={value} />,
  math: ({ value }) => <TeX math={value} block />,
  code: ({ language, value }) => (
    <SyntaxHighlighter style={dracula} language={language} children={value} />
  ),
  table: (props) => {
    return (
      <table className="table table-sm table-nonfluid">{props.children}</table>
    );
  },
  tableHead: (props) => {
    return <thead className="thead-dark">{props.children}</thead>;
  },
  footnoteReference: (props) => (
    <sup id={"ref-" + props.identifier}>
      <a href={"#def-" + props.identifier}>{props.label}</a>
    </sup>
  ),
  footnoteDefinition: (props) => (
    <div className="footnoteDefinition" id={"def-" + props.identifier}>
      <a className="backToRef" href={"#ref-" + props.identifier}>
        {props.label}
      </a>
      <div className="footnoteBody">{props.children}</div>
    </div>
  ),
  image: (props) => (
    <figure className="text-center">
      <img {...props} alt={props.alt} style={{ maxWidth: "75%" }} />
      <figcaption style={{ textAlign: "center" }}>{props.alt}</figcaption>
    </figure>
  ),
};

const _plugins = [
  [gfm, { singleTilde: false }],
  math,
  [smartypants, { dashes: "oldschool" }],
  footnotes,
];

const Markdown = (props) => (
  <ReactMarkdown renderers={_renderers} plugins={_plugins} {...props} />
);

export default Markdown;
