# Security Policy

## Supported version
The latest release on the default branch receives security fixes.

## Data safety model
CSV Cleaner Studio processes files locally, does not execute CSV cells, and does not use the network. It refuses in-place source overwrite. Treat output as untrusted data when opening it in spreadsheet software: formula-like cells are preserved and are not neutralized.

## Reporting a vulnerability
Please use GitHub's private security reporting feature when available. Do not open a public issue containing exploit details, credentials, personal data, or sensitive datasets. Include the affected version, minimal synthetic reproduction, impact, and suggested mitigation if known.

## Scope
Parser crashes, unintended file writes, path handling issues, or code execution caused by crafted CSV input are security-relevant. General spreadsheet behavior outside this program, including formula execution after opening an output file, is a documented limitation unless the program itself unexpectedly executes content.
