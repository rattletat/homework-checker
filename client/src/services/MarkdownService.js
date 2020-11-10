import React from "react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { dracula } from "react-syntax-highlighter/dist/esm/styles/prism";
import { InlineMath, BlockMath } from "react-katex";
import math from "remark-math";
import "katex/dist/katex.min.css";

const _renderers = {
    inlineMath: ({ value }) => <InlineMath math={value} />,
    math: ({ value }) => <BlockMath math={value} />,
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
