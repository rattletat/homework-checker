import React from "react";
import * as d3 from "d3";
// import d3 from "https://d3js.org/d3.v7.min.js";
export const useD3 = (renderChartFn, dependencies) => {
  const ref = React.useRef();

  React.useEffect(() => {
    renderChartFn(d3.select(ref.current));
    return () => undefined;
  }, dependencies);
  return ref;
};
