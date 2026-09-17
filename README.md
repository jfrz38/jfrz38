# Hello, I'm JF 👋

Backend engineer and occasional software architect, building pragmatic systems.

I build things I use, or wish existed, and keep the repositories open in case they are useful to someone else.

I work with coding agents as part of my day-to-day development workflow, mainly through OpenCode, and I build tools around that workflow too.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/josef-ruiz/) [![Email](https://img.shields.io/badge/Email-FFAD00?style=flat-square)](mailto:jose.ruiz@hexacode.es) [![CV](https://img.shields.io/badge/CV-555555?style=flat-square)](https://jfrz38.github.io/cv)

- 🏜️ Based in **Almería, Spain**
- 🚀 Co-founder at [Hexacode](https://hexacode.es)
- 💻 Usually somewhere between backend systems, software architecture and developer tooling
- 🎮 Outside code: Age of Empires II and FIBA basketball

## Core stack

![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white) ![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=flat-square&logo=kotlin&logoColor=white) ![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) ![NestJS](https://img.shields.io/badge/NestJS-E0234E?style=flat-square&logo=nestjs&logoColor=white) ![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![gRPC](https://img.shields.io/badge/gRPC-244C5A?style=flat-square&logo=grpc&logoColor=white)

Also working with Python, GitHub Actions, Prometheus, Grafana, Terraform, Kubernetes and Cloudflare. Still trying to find excuses to build things in Go.

*Small tools, disproportionate joy: jq, regex and automating the repetitive bits.*

## Projects

### Backend libraries

- **[PID Rate Limiter](https://github.com/jfrz38/rate-limit-pid-controller)** · `TypeScript` `Express` `NestJS` · Adaptive rate limiting driven by a PID feedback loop, inspired by [Uber's Cinnamon](https://www.uber.com/en-ES/blog/cinnamon-using-century-old-tech-to-build-a-mean-load-shedder/). [core](https://www.npmjs.com/package/@jfrz38/pid-controller-core) · [Express](https://www.npmjs.com/package/@jfrz38/pid-controller-express) · [NestJS](https://www.npmjs.com/package/@jfrz38/pid-controller-nestjs)
- **[NestJS Cache Proxy](https://github.com/jfrz38/nestjs-cache-proxy)** · `TypeScript` `NestJS` `cache-manager` · Transparent, declarative caching for NestJS providers without changing how consumers use them. [npm](https://www.npmjs.com/package/@jfrz38/nestjs-cache-proxy)
- **[mockguard](https://github.com/jfrz38/mockguard)** · `Kotlin` `JUnit 5` `Mockito` · Strict mock validation that detects interactions left unverified. [Maven Central](https://central.sonatype.com/artifact/io.github.jfrz38/mockguard)
- **[NestJS OpenAPI Wrapper](https://github.com/jfrz38/nestjs-openapi-generator-wrapper)** · `TypeScript` `NestJS` `OpenAPI` · Opinionated NestJS structures and templates on top of OpenAPI Generator. [npm](https://www.npmjs.com/package/@jfrz38/nestjs-open-api-generator-wrapper)

### Developer tooling & automation

- **[Clean Architecture Highlighter](https://github.com/jfrz38/clean-architecture-highlighter)** · `TypeScript` `VS Code` `ESLint` · Architecture dependency rules in the editor, linter and command line. [CLI](https://www.npmjs.com/package/@jfrz38/clean-architecture-highlighter-cli) · [ESLint](https://www.npmjs.com/package/@jfrz38/eslint-plugin-clean-architecture-highlighter) · [VS Code](https://marketplace.visualstudio.com/items?itemName=jfrz38.clean-architecture-highlighter)
- **[check-version-change](https://github.com/jfrz38/check-version-change)** · `TypeScript` `GitHub Actions` · Detects version changes across npm, PyPI, Maven, crates.io, Go modules and Git refs.
- **[auto-version-bump-action](https://github.com/jfrz38/auto-version-bump-action)** · `TypeScript` `GitHub Actions` · Reusable SemVer bumps for Gradle, npm and custom project files.
- **[cocommit](https://github.com/jfrz38/cocommit)** · `Rust` `ratatui` `Git` · A keyboard-driven TUI for building Conventional Commits. [crates.io](https://crates.io/crates/cocommit)

### OpenCode workflow

- **[OpenCode Copy Last](https://github.com/jfrz38/opencode-copy-last)** · `TypeScript` `OpenCode` · Copies the latest response or exchange without leaving the terminal. [npm](https://www.npmjs.com/package/@jfrz38/opencode-copy-last)
- **[OpenCode Wololo Notifications](https://github.com/jfrz38/opencode-wololo-notifications)** · `TypeScript` `OpenCode` · Configurable Age of Empires II sounds for agent events. [npm](https://www.npmjs.com/package/@jfrz38/opencode-wololo-notifications)

### Experiments & side quests

- **[smart-world-map](https://github.com/jfrz38/smart-world-map)** · `Python` `Rust` `Arduino` · A physical LED map following the ISS, nearby flights and earthquakes.
- **[worldhunt](https://github.com/jfrz38/worldhunt)** · `Rust` `ratatui` · An offline hot-and-cold country guessing game for the terminal. [crates.io](https://crates.io/crates/worldhunt)
- **[wololang](https://github.com/jfrz38/wololang)** · `TypeScript` `esolang` · An esoteric language built from Age of Empires II taunts. Yes, `wololo` is valid syntax.
- **[rocket-api-test](https://github.com/jfrz38/rocket-api-test)** · `Rust` `Rocket` · A deliberately small API exploring layered design, dependency inversion and value objects.

[Browse all repositories →](https://github.com/jfrz38?tab=repositories)

## Packages in the wild

Registry requests are not unique users, but they are a useful pulse of where these tools travel.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./profile/distribution-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./profile/distribution-light.svg">
    <img alt="Open-source package footprint" src="./profile/distribution-light.svg" width="790">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./profile/registry-activity-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./profile/registry-activity-light.svg">
    <img alt="Monthly npm and crates.io download activity" src="./profile/registry-activity-light.svg" width="790">
  </picture>
</p>

## GitHub snapshot

*Public repositories only.*

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./profile/stats-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./profile/stats-light.svg">
    <img alt="GitHub stats" src="./profile/stats-light.svg" width="467">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./profile/top-langs-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./profile/top-langs-light.svg">
    <img alt="Most used languages" src="./profile/top-langs-light.svg" width="300">
  </picture>
</p>

---

🔥 **Coding like I play AoE II:** *stressful and crying*

<img alt="Age of Empires II War Elephant" src="https://dn721502.ca.archive.org/0/items/AoE2WarElephantWalkingGif/AoE2-War-Elephant-Walking-Gif.gif" width="220">
