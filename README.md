# GIS
This repository contains the GIS files for environmental field reviews in Florida.

A generic geodatabase is formatted to be used for wetland delineations with a line and polygon feature class as well as wildlife surveys with a point feature class with a range domain to accept a survey date, and coded domains for species common name and observation type. Also included is a `PhotoStation` point file with attachments enabled.

A python script is designed to batch export all attachments into a specified directory in `.jpg` format and named by the values in a specified field.
