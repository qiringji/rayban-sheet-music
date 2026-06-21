# AGENTS.md — AI Agent Instructions

This file provides instructions for AI coding agents (e.g. Claude Code, Codex) working on this repository.

## Project Overview

**rayban-sheet-music** displays musical scores on Meta Ray-Ban smart glasses via the Display API.
It consists of:
- A Python/FastAPI backend for parsing and rendering sheet music
- An iOS companion app (SwiftUI + Tuist) for Bluetooth control
- Integration with Meta Ray-Ban Display API

Reference project: [claude-glasses](https://github.com/qiringji/claude-glasses)

## Repository Structure

```
backend/        Python FastAPI server — score parsing, rendering, display client
ios/            SwiftUI companion app managed with Tuist
scores/         Sample MusicXML files for testing
docs/           Architecture and API documentation
```

## Development Guidelines

### Backend (Python)
- Use `FastAPI` for all HTTP endpoints
- Use `music21` for MusicXML parsing
- Keep the `display/` module isolated — it should only depend on the Ray-Ban Display API client
- All endpoints must have type hints and Pydantic models
- Run `pytest` before committing

### iOS App
- Use `Tuist` to manage the Xcode project — do not commit `.xcodeproj` directly
- Follow the `claude-glasses` project structure: separate `Clients/`, `Views/`, `Stores/`
- Bluetooth communication goes in `BluetoothClient.swift`
- Display commands go in `DisplayClient.swift`

### Environment / Secrets
- Never commit secrets; use `.env` (backend) and `Secrets.swift` (iOS, gitignored)
- Copy `.env.template` and `Secrets.swift.template` to get started

## Test Plan
1. `pytest backend/` — all unit tests pass
2. `tuist generate && xcodebuild test` — iOS smoke tests pass
3. Manual test: upload a MusicXML file and confirm it renders on the glasses display

## Out of Scope
- Audio playback (handled by separate project)
- Score editing / annotation
