# What this gives you

Plain-language guide for the owner who can't read the code. This explains what a passing build actually proves — and the one thing it can't, where you're still the final eye.

---

## What does a green checkmark actually prove?

When the checks pass (the green checkmark on a build), these things have been confirmed for you, automatically, without anyone reading the code:

- **The geometry is mathematically correct.** The add-ons' math is checked against the right answers worked out by hand — the bevel's corner shape, the phyllotaxis (sunflower-seed) spacing and spiral. Not "the code ran" — the actual numbers it produces are the numbers they should be.

- **The tool proved its own tests can catch broken work.** This is the part that lets you trust the green light instead of just hoping. The tool deliberately breaks copies of the add-ons and confirms its own geometry tests notice and fail. A test that passes no matter what is worthless; this proves those tests have teeth. (In the code this is the "mutation/tamper gate." It covers the core geometry math; extending it to the in-Blender checks is tracked but not yet done.)

- **Secrets, dependencies, and known-vulnerable code are scanned.** Three of GitHub's own free safety nets run on every change: one watches for passwords or keys accidentally left in the code (Secret Scanning), one watches for outside code the add-ons rely on going out of date or becoming risky (Dependabot), and one scans for known security holes (CodeQL).

- **The code is auto-checked for cleanliness.** Two tools (ruff and bandit) automatically flag sloppy or unsafe code patterns before anything merges — so what's built starts clean and stays clean.

These run on their own, the same way every time, on every build. You don't have to ask for them or stand over them.

---

## What is NOT machine-checked — where YOU are the final eye

A machine can prove the math is right. It cannot prove the result **looks** right, or that it's what you actually **meant**. That judgment is yours.

So every build renders a picture of each add-on's output and saves it for you to download and look at (the "visual-confirmation" preview). The checks above guarantee the geometry is correct; this preview is for the one question they can't answer — *is this what I wanted?* That's your call, in Blender, as the director.

Put simply: **green means the work is correct and built to standard. Whether it's the right work is still your eye.**
