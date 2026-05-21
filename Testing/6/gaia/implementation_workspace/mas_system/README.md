# Multi-Agent System for City 15-Minute Neighborhoods

This project implements a production-grade Multi-Agent System based on the GAIA methodology for matching local properties with businesses and residents to support the concept of "15-minute city".

## System Overview

The system consists of four main agent types:
- PropertyOwnerAgent: Represents property owners who list properties for rent or sale
- BusinessEntityAgent: Represents businesses seeking suitable premises
- ResidentAgent: Represents local residents who may express service demands
- MarketplaceAgent: Manages the marketplace, including property listings, business demands, and matching algorithms

## Features Implemented

1. Property listing and removal
2. Business-property matching based on criteria (price, location, size, activity type)
3. Business response to match proposals
4. Business demand submission
5. Matching boundary setting
6. Resident service demand submission
7. Property offer withdrawal
8. Resident demand withdrawal

## Architecture

The system follows the GAIA methodology with defined roles, protocols, and interactions. All agents communicate through the MarketplaceAgent which acts as the central coordinator.
