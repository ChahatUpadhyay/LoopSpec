# 🧠 Learnings & Corrections

<!-- 
  MODEL: This is your LONG-TERM MEMORY. Append-only — never delete entries.
-->

---

## Learning 1 — Iteration 1 — Phase: VERIFY

### What Went Wrong
Node.js is not installed on this Windows system. The `node test-node.js` command failed with `CommandNotFoundException`.

### Root Cause
The test plan assumed Node.js availability. The system only has cscript.exe (Windows Script Host) available as a JS runtime.

### Fix Applied
Created `test-verify.js` using ES5-compatible JScript syntax for cscript.exe. Ran successfully with `cscript //nologo //E:JScript test-verify.js` — all 36 tests passed.

### Prevention Rule
Always check for available JS runtimes before assuming Node.js is present. On Windows, cscript.exe with JScript is a reliable fallback. Test scripts should be created for whatever runtime is available.

---
