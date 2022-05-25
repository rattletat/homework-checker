import React from "react";

function TapText({ children }) {
  const colorize = (line) => {
    if (line.match(/# E +\+/)) {
      return "diff-positive";
    } else if (line.match(/# E +-/)) {
      return "diff-negative";
    } else if (line.match(/# >/)) {
      return "assert-statement";
    } else if (line.match(/# E.*Error/)) {
      return "error-message";
    } else if (line.match(/# E/)) {
      return "error-neutral";
    } else return "none";
  };

  return (
    <div className="submission-output">
      {children.split("\n").map((line) => (
        <div className={colorize(line)}>{line}</div>
      ))}
    </div>
  );
}

export default TapText;
