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

![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white) ![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=flat-square&logo=kotlin&logoColor=white) ![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) ![NestJS](https://img.shields.io/badge/NestJS-E0234E?style=flat-square&logo=nestjs&logoColor=white) ![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

Also working with Python, MongoDB, gRPC, GitHub Actions, Prometheus, Grafana, Terraform, Kubernetes and Cloudflare. Still trying to find excuses to build things in Go.

*Small tools, disproportionate joy: jq, regex and automating the repetitive bits.*

## Featured projects

- **[Adaptive Admission Controller](https://github.com/jfrz38/adaptive-admission-controller)** — The Rust core for priority-aware load shedding and adaptive concurrency, controlled by a deterministic PID state machine.<br>
  `Rust` · `WebAssembly` · [crates.io](https://crates.io/crates/adaptive-admission-core) · [docs.rs](https://docs.rs/adaptive-admission-core)<br><br>
- **[NestJS OpenAPI Wrapper](https://github.com/jfrz38/nestjs-openapi-generator-wrapper)** — Opinionated NestJS structures and templates on top of OpenAPI Generator.<br>
  `TypeScript` · `NestJS` · `OpenAPI` · [npm](https://www.npmjs.com/package/@jfrz38/nestjs-open-api-generator-wrapper)<br><br>
- **[Clean Architecture Highlighter](https://github.com/jfrz38/clean-architecture-highlighter)** — Architecture dependency rules in the editor, linter and command line.<br>
  `TypeScript` · `VS Code` · `ESLint` · [Marketplace](https://marketplace.visualstudio.com/items?itemName=jfrz38.clean-architecture-highlighter)<br><br>
- **[cocommit](https://github.com/jfrz38/cocommit)** — A keyboard-driven terminal UI for building Conventional Commits.<br>
  `Rust` · `ratatui` · `Git` · [crates.io](https://crates.io/crates/cocommit)<br><br>
- **[OpenCode Copy Last](https://github.com/jfrz38/opencode-copy-last)** — Copies the latest response or exchange without leaving the terminal.<br>
  `TypeScript` · `OpenCode` · [npm](https://www.npmjs.com/package/@jfrz38/opencode-copy-last)

## More projects

<details>
<summary><strong>🧱 Backend libraries & adapters</strong></summary>

- **[PID Rate Limiter](https://github.com/jfrz38/rate-limit-pid-controller)** — Node.js adapter for Adaptive Admission Controller, with Express and NestJS integrations. [npm packages](https://www.npmjs.com/search?q=%40jfrz38%2Fpid-controller)
- **[NestJS Cache Proxy](https://github.com/jfrz38/nestjs-cache-proxy)** — Transparent, declarative caching for NestJS providers. [npm](https://www.npmjs.com/package/@jfrz38/nestjs-cache-proxy)
- **[mockguard](https://github.com/jfrz38/mockguard)** — Strict Mockito validation that detects interactions left unverified. [Maven Central](https://central.sonatype.com/artifact/io.github.jfrz38/mockguard)

</details>

<details>
<summary><strong>☁️ Systems & cloud</strong></summary>

- **[EdgeFlags](https://github.com/jfrz38/edgeflags)** — An experimental edge-native feature flag service with authentication, scoped authorization and automated delivery.

</details>

<details>
<summary><strong>🛠️ Developer tooling & automation</strong></summary>

- **[check-version-change](https://github.com/jfrz38/check-version-change)** — Detects version changes across npm, PyPI, Maven, crates.io, Go modules and Git refs. [Marketplace](https://github.com/marketplace/actions/check-version-change)
- **[verify-release-tag](https://github.com/jfrz38/verify-release-tag)** — Validates that a release tag matches a manifest version and expected commit. [Marketplace](https://github.com/marketplace/actions/verify-release-tag)
- **[auto-version-bump-action](https://github.com/jfrz38/auto-version-bump-action)** — Reusable SemVer bumps for Gradle, npm and custom project files. [Marketplace](https://github.com/marketplace/actions/auto-version-bump-action)

</details>

<details>
<summary><strong>🤖 OpenCode workflow</strong></summary>

- **[OpenCode Wololo Notifications](https://github.com/jfrz38/opencode-wololo-notifications)** — Configurable Age of Empires II sounds for agent events. [npm](https://www.npmjs.com/package/@jfrz38/opencode-wololo-notifications)

</details>

<details>
<summary><strong>🧪 Experiments & side quests</strong></summary>

- **[smart-world-map](https://github.com/jfrz38/smart-world-map)** — A physical LED map following the ISS, nearby flights and earthquakes.
- **[worldhunt](https://github.com/jfrz38/worldhunt)** — An offline hot-and-cold country guessing game for the terminal. [crates.io](https://crates.io/crates/worldhunt)
- **[wololang](https://github.com/jfrz38/wololang)** — An esoteric language built from Age of Empires II taunts. Yes, `wololo` is valid syntax.
- **[bash-http-lab](https://github.com/jfrz38/bash-http-lab)** — An HTTP/1.1 server built in plain Bash to explore what web frameworks hide.
- **[rocket-api-test](https://github.com/jfrz38/rocket-api-test)** — A small Rust API exploring layered design, dependency inversion and value objects.

</details>

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
    <img alt="GitHub stats" src="./profile/stats-light.svg" height="165">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./profile/top-langs-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./profile/top-langs-light.svg">
    <img alt="Most used languages" src="./profile/top-langs-light.svg" height="165">
  </picture>
</p>

---

🔥 **Coding like I play AoE II:** *stressful and crying*

<img alt="Age of Empires II War Elephant" src="https://dn721502.ca.archive.org/0/items/AoE2WarElephantWalkingGif/AoE2-War-Elephant-Walking-Gif.gif" width="220">
