# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Prerequisites:** Node.js ~20.19.0 for development (any version >=20 for production)

### Build & Development
- `npm install` - Install dependencies
- `npm run build` - Build main project (packages/cli and packages/core)
- `npm run build:all` - Build main project and sandbox container
- `npm start` - Start Gemini CLI from source
- `npm run debug` - Start CLI in debug mode with --inspect-brk

### Testing
- `npm run test` - Run unit tests across all packages
- `npm run test:e2e` - Run integration tests (end-to-end)
- `npm run test:integration:all` - Run all integration tests with different sandbox configurations
- `npm run test:ci` - Run tests in CI mode

### Code Quality
- `npm run lint` - Run ESLint on TypeScript files
- `npm run lint:fix` - Auto-fix ESLint issues
- `npm run format` - Format code with Prettier
- `npm run typecheck` - Run TypeScript type checking
- `npm run preflight` - Run complete quality check (clean, format, lint, build, typecheck, test)

### Other
- `npm run clean` - Remove generated files
- `make help` - Show available Makefile commands

## Architecture Overview

This is a monorepo with a two-package architecture plus tooling:

### Core Packages
1. **`packages/cli/`** - User-facing command-line interface
   - Handles user input, display rendering, themes, history management
   - React-based UI using Ink framework
   - Contains built-in commands (auth, help, theme, etc.)
   
2. **`packages/core/`** - Backend logic and API integration
   - Gemini API client and prompt construction
   - Tool registration and execution orchestration
   - Session state management, telemetry, MCP integration

### Key Components
- **Tools System** (`packages/core/src/tools/`) - Extensible modules that allow Gemini to interact with local environment (file system, shell, web, etc.)
- **Sandboxing** - Multiple sandboxing options (macOS Seatbelt, Docker, Podman) for secure tool execution
- **MCP Integration** - Model Context Protocol support for connecting external capabilities

### Interaction Flow
1. CLI receives user input → sends to Core
2. Core constructs prompt + available tools → sends to Gemini API  
3. Gemini responds with text or tool requests
4. Tool execution (with user approval for modifying operations)
5. Results sent back to Gemini → final response to CLI → displayed to user

## Project Structure

- `packages/cli/src/ui/` - React components for terminal UI
- `packages/core/src/tools/` - Individual tool implementations
- `packages/core/src/core/` - Core Gemini API client and chat logic
- `integration-tests/` - End-to-end test suite
- `scripts/` - Build and utility scripts
- `docs/` - Comprehensive documentation

## Development Notes

- Uses ESM modules (`"type": "module"`)
- TypeScript throughout with strict configuration
- React DevTools available in development mode (`DEV=true npm start`)
- Sandboxing is configurable via environment variables (`GEMINI_SANDBOX`, `SEATBELT_PROFILE`)
- Tool execution requires user approval for write operations, read operations are auto-approved
- Follows Conventional Commits standard for commit messages