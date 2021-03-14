import React from "react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { dracula } from "react-syntax-highlighter/dist/esm/styles/prism";
import 'katex/dist/katex.min.css';
import TeX from '@matejmazur/react-katex';
import math from "remark-math";

const _renderers = {
    inlineMath: ({ value }) => <TeX math={value} />,
    math: ({ value }) => <TeX math={value} block />,
    code: ({ language, value }) => {
        return (
            <SyntaxHighlighter
                style={dracula}
                language={language}
                children={value}
            />
        );
    }
};

const _plugins = [gfm, math];

const Markdown = props => (
    <ReactMarkdown renderers={_renderers} plugins={_plugins} {...props} />
);

export default Markdown;
