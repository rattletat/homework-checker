import React from "react";
import { useD3 } from "../hooks/useD3";
import * as d3 from "d3";

function BarChart({ all_scores, user_score, max_score }) {
  const ref = useD3(
    (svg) => {
      var area = svg;
      var margin = { top: 20, right: 20, bottom: 30, left: 40 },
        borders = area.node().getBoundingClientRect(),
        width = borders.width,
        height = borders.height,
        innerWidth = width - margin.left - margin.right,
        innerHeight = height - margin.top - margin.bottom;

      var svg = area
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g");

      var scX = d3
        .scaleLinear()
        .domain([-max_score * 0.05, max_score * 1.05])
        .range([0, innerWidth]);

      // Axis
      svg
        .append("g")
        .attr(
          "transform",
          "translate(" + margin.left + "," + (innerHeight + margin.top) + ")"
        )
        .call(d3.axisBottom(scX));

      var histogram = d3
        .histogram()
        .domain(scX.domain())
        .thresholds(Math.round(max_score / 4));

      var bins = histogram(all_scores);
      var scY = d3
        .scaleLinear()
        .domain([0, d3.max(bins, (d) => d.length)])
        .range([innerHeight, 0]);

      const yAxisTicks = scY.ticks(5).filter((tick) => Number.isInteger(tick));
      const yAxis = d3
        .axisLeft(scY)
        .tickValues(yAxisTicks)
        .tickFormat(d3.format("d"));
      svg
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .call(yAxis);

      // Bars
      if (all_scores.length > 0) {
        svg
          .selectAll("rect")
          .data(bins)
          .enter()
          .append("rect")
          .attr("x", 1)
          .attr("y", 0)
          .attr(
            "transform",
            (d) =>
              "translate(" +
              (1 + margin.left + scX(d.x0) - (scX(d.x1) - scX(d.x0)) / 2) +
              "," +
              (innerHeight + margin.top) +
              ")"
          )
          .attr("width", (d) => scX(d.x1) - scX(d.x0) - 2)
          .style("fill", "grey")
          .transition()
          .duration(3000)
          .style("fill", "#4582EC")
          .attr("height", (d) => innerHeight - scY(d.length))
          .attr(
            "transform",
            (d) =>
              "translate(" +
              (1 + margin.left + scX(d.x0) - (scX(d.x1) - scX(d.x0)) / 2) +
              "," +
              (scY(d.length) + margin.top) +
              ")"
          );
      }

      // Vertical Line
      svg
        .append("line")
        .attr("x1", margin.left + scX(user_score))
        .attr("x2", margin.left + scX(user_score))
        .attr("y1", margin.top)
        .attr("y2", margin.top + innerHeight)
        .attr("stroke", "#e37222")
        .attr("stroke-width", 2)
        .attr("stroke-dasharray", 4);

      svg
        .append("text")
        .attr("x", margin.left + scX(user_score))
        .attr("y", (2 * margin.top) / 3)
        .attr("font-family", "sans-serif")
        .attr("font-size", "12px")
        .attr("text-anchor", "middle")
        .attr("class", "score")
        .style("fill", "#e37222")
        .text("Score");

      // // Labels
      svg
        .append("text")
        .attr("x", margin.left + innerWidth / 2)
        .attr("y", height)
        .attr("font-family", "sans-serif")
        .attr("font-size", "12px")
        .attr("text-anchor", "middle")
        .attr("class", "x label")
        .text("Points");

      svg
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0)
        .attr("x", -(margin.top + innerHeight / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", "12px")
        .attr("class", "y label")
        .text("Students");
    },
    [all_scores.length, user_score, max_score]
  );

  return (
    <>
      <svg
        ref={ref}
        style={{
          height: "100%",
          width: "100%",
          marginRight: "0px",
          marginLeft: "0px",
        }}
      />
    </>
  );
}

export default BarChart;
