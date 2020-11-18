#!/usr/bin/env Rscript
library(testthat)

args = commandArgs(trailingOnly=TRUE)
separator <- args[2]

cat(separator)
test_file("tests.r", reporter=TapReporter)
cat(separator)
