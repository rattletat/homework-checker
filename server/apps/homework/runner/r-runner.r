#!/usr/bin/env Rscript
library(testthat)
library(here)

args = commandargs(trailingonly=true)
separator <- args[1]

cat(separator)
test_file("tests.r", reporter=TapReporter)
cat(separator)
