import React from "react";
import ReactMarkdown from "react-markdown";

import {Prism as SyntaxHighlighter} from "react-syntax-highlighter";
import {dracula} from "react-syntax-highlighter/dist/esm/styles/prism";

import TeX from "@matejmazur/react-katex";
import "katex/dist/katex.min.css";

import gfm from "remark-gfm";
import math from "remark-math";
import remarkSmartypants from "remark-smartypants";

const _renderers = {
    inlineMath: ({value}) => <TeX math={value} />,
    math: ({value}) => <TeX math={value} block />,
    code: ({language, value}) =>
        <SyntaxHighlighter
            style={dracula}
            language={language}
            children={value}
        />
    ,
    table: (props) => {
        return <table className="table table-sm table-nonfluid">{props.children}</table>
    },
    tableHead: (props) => {
        return <thead className="thead-light">{props.children}</thead>
    }
};

const _plugins = [gfm, math, remarkSmartypants];

const Markdown = props => (
    <ReactMarkdown renderers={_renderers} plugins={_plugins} {...props} />
);

export default Markdown;
